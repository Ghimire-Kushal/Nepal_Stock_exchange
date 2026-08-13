import random
from datetime import timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from stocks.models import Stock, HistoricalStockPrice
from brokers.models import Broker, FloorSheet
from portfolio.models import Portfolio, Holding
from watchlist.models import Watchlist
from trading.models import PaperWallet, PaperHolding, PaperTrade

class Command(BaseCommand):
    help="Seed clearly demo-generated NEPSE market, broker, portfolio, and paper-trading data."
    def handle(self,*args,**opts):
        random.seed(42); today=timezone.localdate()
        data=[("NABIL","Nabil Bank Limited","Commercial Bank",523), ("NICA","NIC Asia Bank","Commercial Bank",812), ("ADBL","Agricultural Development Bank","Commercial Bank",303), ("SHIVM","Shivam Cements","Manufacturing",547), ("HDL","Himalayan Distillery","Manufacturing",2150), ("NRIC","Nepal Reinsurance","Insurance",894), ("CHCL","Chilime Hydropower","Hydropower",562), ("UPPER","Upper Tamakoshi","Hydropower",207), ("NTC","Nepal Telecom","Others",943), ("CIT","Citizen Investment Trust","Investment",2150), ("NIFRA","Nepal Infrastructure Bank","Finance",216), ("GBIME","Global IME Bank","Commercial Bank",274), ("PRVU","Prabhu Bank","Commercial Bank",201), ("SANIMA","Sanima Bank","Commercial Bank",387), ("HIDCL","Hydro Investment","Investment",185), ("API","API Power","Hydropower",287), ("MEN","Mountain Energy","Hydropower",652), ("CGH","Chandragiri Hills","Hotels",1042), ("BNT","Bottlers Nepal","Manufacturing",14780), ("NICL","Nepal Insurance","Insurance",802)]
        stocks=[]
        for sym,name,sector,price in data:
            change=Decimal(str(round(random.uniform(-4.5,5.5),2))); prev=Decimal(str(price))-change
            stock,_=Stock.objects.update_or_create(symbol=sym,defaults={"company_name":name,"sector":sector,"current_price":price,"previous_close":prev,"open_price":price-3,"high_price":price+8,"low_price":price-10,"volume":random.randint(80000,900000),"turnover":price*random.randint(80000,900000),"percentage_change":change,"listed_shares":random.randint(10,100)*1000000,"market_cap":price*random.randint(10,100)*1000000}); stocks.append(stock)
            base=price
            for offset in range(90,0,-1):
                base=round(base*(1+random.uniform(-.025,.025)),2); date=today-timedelta(days=offset)
                HistoricalStockPrice.objects.update_or_create(stock=stock,date=date,defaults={"open":base-2,"high":base+5,"low":base-6,"close":base,"volume":random.randint(10000,250000),"turnover":Decimal(str(base*random.randint(10000,250000)))})
        broker_data = [
            (1, "Kumari Securities Private Limited"),
            (3, "Arun Securities (PVT) Ltd."),
            (4, "Opal Securities Investment (PVT) Ltd."),
            (5, "Market Securities & Exchange (PVT) Ltd."),
            (6, "Agrawal Securities (PVT) Ltd."),
            (7, "J.F. Securites (PVT) Ltd."),
            (8, "Ashutosh Brokerage & Securities (PVT) Ltd."),
            (10, "Pragyan Securities (PVT) Ltd."),
            (11, "Malla & Malla Stock Broking Company Pvt. Limited"),
            (13, "Thrive Brokerage House Pvt. Ltd"),
            (14, "Nepal Stock House (PVT) Ltd."),
            (16, "Primo Securities (PVT) Ltd."),
            (17, "ABC Securities Private Limited"),
            (18, "Sagarmatha Securities Private Limited"),
            (19, "Nepal Investment And Securities Trading Private Limited"),
            (20, "Sipla Securities Private Limited"),
            (21, "Midas Stock Broking Company Private Limited"),
            (22, "Siprabi Securities Pvt. Ltd."),
            (25, "Sweta Securities Private Limited"),
            (26, "Asian Securities Private Ltd."),
        ]
        brokers = [Broker.objects.update_or_create(
            broker_number=number,
            defaults={"broker_name": name, "address": "Kathmandu, Nepal", "phone": "01-5550000"},
        )[0] for number, name in broker_data]
        for i in range(600):
            st=random.choice(stocks); qty=random.choice([10,20,50,100,250,500,1000]); rate=st.current_price+Decimal(str(random.randint(-10,10))); date=today-timedelta(days=random.randint(0,89)); FloorSheet.objects.get_or_create(contract_number=f"DEMO{today:%Y%m%d}{i:05d}",defaults={"stock":st,"buyer_broker":random.choice(brokers),"seller_broker":random.choice(brokers),"quantity":qty,"rate":rate,"amount":qty*rate,"trade_date":date})
        user,_=get_user_model().objects.get_or_create(username="demo",defaults={"email":"demo@example.com","first_name":"Demo","last_name":"Investor"}); user.set_password("demo12345"); user.save()
        portfolio,_=Portfolio.objects.get_or_create(user=user,name="Demo Portfolio")
        for st in stocks[:4]: Holding.objects.update_or_create(portfolio=portfolio,stock=st,defaults={"quantity":100,"average_buy_price":st.current_price*Decimal("0.92")})
        for st in stocks[:5]: Watchlist.objects.get_or_create(user=user,stock=st)
        wallet,_=PaperWallet.objects.get_or_create(user=user)
        holding,_=PaperHolding.objects.get_or_create(user=user,stock=stocks[0],defaults={"quantity":50,"average_buy_price":stocks[0].current_price})
        PaperTrade.objects.get_or_create(user=user,stock=stocks[0],trade_type="BUY",quantity=50,price=stocks[0].current_price,total_amount=stocks[0].current_price*50)
        self.stdout.write(self.style.SUCCESS("Seeded 20 stocks, 20 brokers, 90-day histories, and 600 demo floorsheet transactions. Demo login: demo / demo12345"))
