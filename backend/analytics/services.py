"""Indicator calculations over stored data; no third-party market scraping."""
import pandas as pd
from django.db.models import Sum
from stocks.models import Stock
from brokers.models import FloorSheet

def indicators(stock):
    closes = list(stock.history.order_by("date").values_list("close", flat=True))
    if not closes: return {"symbol": stock.symbol, "error": "No historical prices available."}
    s = pd.Series([float(x) for x in closes]); ema20=s.ewm(span=20,adjust=False).mean(); ema50=s.ewm(span=50,adjust=False).mean(); delta=s.diff(); gain=delta.clip(lower=0).rolling(14).mean(); loss=(-delta.clip(upper=0)).rolling(14).mean(); rsi=100-(100/(1+gain/loss))
    macd=s.ewm(span=12,adjust=False).mean()-s.ewm(span=26,adjust=False).mean(); signal=macd.ewm(span=9,adjust=False).mean(); price=float(s.iloc[-1]); r=float(rsi.iloc[-1]) if pd.notna(rsi.iloc[-1]) else 50
    score=(1 if price>ema20.iloc[-1] else -1)+(1 if price>ema50.iloc[-1] else -1)+(1 if r<70 and r>50 else -1 if r>70 else 0)+(1 if macd.iloc[-1]>signal.iloc[-1] else -1)
    label="Strong Buy" if score>=3 else "Buy" if score>=1 else "Strong Sell" if score<=-3 else "Sell" if score<=-1 else "Neutral"
    def val(x): return round(float(x),2) if pd.notna(x) else None
    return {"symbol":stock.symbol,"sma_20":val(s.rolling(20).mean().iloc[-1]),"sma_50":val(s.rolling(50).mean().iloc[-1]),"ema_20":val(ema20.iloc[-1]),"ema_50":val(ema50.iloc[-1]),"rsi":val(rsi.iloc[-1]),"macd":val(macd.iloc[-1]),"signal":val(signal.iloc[-1]),"technical_signal":label,"disclaimer":"This educational signal uses technical indicators and is not financial advice."}

class MarketDataProvider:
    def get_market_summary(self): raise NotImplementedError
    def get_stock_price(self, symbol): raise NotImplementedError
    def get_historical_prices(self, symbol): raise NotImplementedError
    def get_floorsheet(self): raise NotImplementedError
class DemoDataProvider(MarketDataProvider):
    def get_market_summary(self):
        stocks=Stock.objects.all(); up=stocks.filter(percentage_change__gt=0).count(); down=stocks.filter(percentage_change__lt=0).count()
        return {"nepse_index": 2084.42,"total_turnover":stocks.aggregate(x=Sum("turnover"))["x"] or 0,"total_volume":stocks.aggregate(x=Sum("volume"))["x"] or 0,"total_transactions":FloorSheet.objects.count(),"advancers":up,"decliners":down,"unchanged":stocks.count()-up-down}
class CSVDataProvider(MarketDataProvider): pass
class LiveAPIProvider(MarketDataProvider): pass
