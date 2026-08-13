# NEPSE Broker Activity, Portfolio & Stock Analysis System

A full-stack Nepal share-market analytics platform. It starts with demo/imported data and is designed for a future licensed market-data provider.

## Current status

The project scaffold and Phase 2 authentication are complete: Django REST Framework, JWT registration/login/refresh/profile APIs, CORS, React + Vite, Tailwind, Axios, and a browser sign-in flow.

## Structure

```text
backend/             Django REST API
  config/            Project settings and API routes
  users/             Authentication (Phase 2)
  stocks/            Stocks and historical data (Phase 3)
  brokers/           Brokers and floorsheets (Phase 4)
  portfolio/         Portfolios and holdings (Phase 6)
  trading/           Paper trading (Phase 8)
  watchlist/         Watchlists (Phase 7)
  analytics/         Technical and broker analytics
frontend/            React + Vite application
  src/components/    Shared UI components
  src/context/       Shared application state
  src/hooks/         Custom hooks
  src/pages/         Route-level pages
  src/services/      Axios API client
  src/styles/        Global Tailwind styles
```

## Setup

1. Create the backend environment and install dependencies:

   ```bash
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   ```

2. The default local database is SQLite, so you can run the app straight away.
   To use PostgreSQL instead, set `DATABASE_ENGINE=postgresql` in
   `backend/.env`, create the database and role, then replace the `POSTGRES_*`
   values:

   ```sql
   CREATE USER nepse_user WITH PASSWORD 'choose-a-strong-password';
   CREATE DATABASE nepse_analysis OWNER nepse_user;
   ```

3. Run migrations and Django:

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

4. In another terminal, install and run the frontend:

   ```bash
   cd frontend
   npm install
   cp .env.example .env
   npm run dev
   ```

Open `http://localhost:5174`. The page should say `API connected: nepse-analysis-api` once Django is running.

## Health endpoint

`GET /api/health/` returns `{"status":"ok","service":"nepse-analysis-api"}`.

## Authentication endpoints

`POST /api/auth/register/`, `POST /api/auth/login/`, `POST /api/auth/token/refresh/`, and `GET`/`PUT /api/auth/profile/` are available. The profile endpoint requires a JWT access token.

## Market data

Run `python manage.py seed_demo_stocks` in `backend/` to load six demo stocks and 90 days of price history. Public APIs include `GET /api/stocks/`, `GET /api/stocks/?search=NABIL`, `GET /api/stocks/NABIL/`, and `GET /api/stocks/NABIL/history/?range=1M` (ranges: `7D`, `1M`, `3M`, `6M`, `1Y`, `ALL`).

## Next phase

Phase 4 adds broker activity and floorsheet imports.
# Nepse
# Nepal_Stock_exchange
