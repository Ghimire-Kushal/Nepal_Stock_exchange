# NEPSE IQ

NEPSE IQ is a demo-ready Nepal Stock Exchange analytics application with a
Django REST API and React/Vite frontend. It is designed around seeded and CSV
data, so it does not require a paid market-data provider.

## Features

- Market dashboard with index, breadth, gainers, losers, turnover, and volume
- Stock search, detail pages, historical price charts, volume charts, and indicators
- Broker directory, broker activity, period filters, and net accumulation labels
- JWT registration, login, profile, and protected user features
- Portfolios, holdings, profit/loss, returns, and sector allocation
- Watchlists and simulated paper trading with wallet and trade history
- Admin statistics and company CSV import; Django admin supports all data models

## Run locally

```bash
cd backend
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend defaults to `http://127.0.0.1:8000/api`. Set
`VITE_API_BASE_URL` in `frontend/.env` to use another API URL. The seeded demo
login is `demo` / `demo12345`.

## API areas

`/api/auth/`, `/api/stocks/`, `/api/brokers/`, `/api/floorsheet/`,
`/api/portfolio/`, `/api/watchlist/`, `/api/paper-trading/`, and
`/api/analytics/`.

All market values are demo or imported data. Technical signals are educational
and are not financial advice.
