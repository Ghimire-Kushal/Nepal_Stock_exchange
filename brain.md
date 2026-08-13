# Prompt: Build a Complete NEPSE Broker Activity, Portfolio & Stock Analysis System

Build a complete full-stack web application named **“NEPSE Broker Activity, Portfolio and Stock Analysis System”** using **Django REST Framework for the backend** and **React for the frontend**.

The system should focus on Nepal Share Market analysis. It must include stock market data management, broker activity analysis, portfolio tracking, paper trading, watchlists, technical indicators, charts, user authentication, and an admin dashboard.

The project should be designed so it works even without a paid real-time NEPSE API. Use sample/demo data, CSV imports, or manually seeded data initially, but structure the backend so a live API can be connected later.

## 1. Technology Stack

Use the following technologies:

* Backend: Django
* API: Django REST Framework
* Frontend: React with Vite
* Database: PostgreSQL
* Authentication: JWT using SimpleJWT
* Charts: Recharts or Chart.js
* HTTP requests: Axios
* Styling: Tailwind CSS
* State management: React Context API or Zustand
* Data processing: Python and Pandas where useful
* Technical indicators: Pandas calculations
* Development environment: Localhost
* Version control: Git and GitHub

Use clean architecture and separate frontend and backend folders.

Suggested structure:

```text
nepse-analysis-system/
│
├── backend/
│   ├── manage.py
│   ├── config/
│   ├── users/
│   ├── stocks/
│   ├── brokers/
│   ├── portfolio/
│   ├── trading/
│   ├── watchlist/
│   └── analytics/
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   ├── hooks/
│   └── context/
│
└── README.md
```

## 2. User Roles

Create these roles:

### Normal User

A normal user can:

* Register
* Login
* Logout
* View stocks
* Search stocks
* View stock details
* View stock charts
* View broker activity
* View broker net holdings
* Create portfolio
* Add stock holdings
* Update holdings
* Delete holdings
* View portfolio profit/loss
* Create watchlist
* Add/remove stocks from watchlist
* Perform paper trading
* View trade history
* View technical indicators
* View buy/sell analysis

### Admin

Admin can:

* Manage users
* Manage stocks
* Manage brokers
* Manage market data
* Import CSV data
* Manage floorsheet data
* Manage historical prices
* View system statistics

## 3. Authentication System

Implement full JWT authentication.

Required endpoints:

```text
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/token/refresh/
GET /api/auth/profile/
PUT /api/auth/profile/
```

Registration should include:

```text
username
email
password
first_name
last_name
```

Passwords must be securely hashed.

Protect private API endpoints.

## 4. Stock Model

Create a Stock model with:

```text
id
symbol
company_name
sector
current_price
previous_close
open_price
high_price
low_price
volume
turnover
percentage_change
listed_shares
market_cap
created_at
updated_at
```

Example:

```text
symbol: NABIL
company_name: Nabil Bank Limited
sector: Commercial Bank
current_price: 523
previous_close: 515
percentage_change: 1.55
```

## 5. Historical Stock Price Model

Create historical stock price data containing:

```text
stock
date
open
high
low
close
volume
turnover
```

Create API:

```text
GET /api/stocks/NABIL/history/
```

Support:

```text
7D
1M
3M
6M
1Y
ALL
```

## 6. Stock Dashboard

Create a main dashboard similar to a professional NEPSE application.

Display:

```text
NEPSE Index
Total Turnover
Total Volume
Total Transactions
Advancers
Decliners
Unchanged
Top Gainers
Top Losers
Top Turnover
Top Volume
```

Create cards and responsive charts.

## 7. Stock Search

Add a search box.

Users should be able to search:

```text
NABIL
NICA
ADBL
SHIVM
HDL
NRIC
```

Search by:

* Stock symbol
* Company name
* Sector

## 8. Stock Detail Page

Create a route:

```text
/stocks/NABIL
```

Display:

```text
Company name
Symbol
Sector
LTP
Price change
Percentage change
Open
High
Low
Previous close
Volume
Turnover
Market cap
```

Also display a historical price chart.

Add tabs:

```text
Overview
Chart
Broker Analysis
Technical Analysis
Historical Data
```

## 9. Broker Model

Create:

```text
id
broker_number
broker_name
address
phone
website
```

Example:

```text
broker_number: 58
broker_name: Naasa Securities
```

Broker information should be editable by admin.

## 10. Floorsheet Model

Create a floorsheet transaction model:

```text
id
contract_number
stock
buyer_broker
seller_broker
quantity
rate
amount
trade_date
trade_time
```

Example:

```text
Contract: 202608130001
Stock: ADBL
Buyer Broker: 58
Seller Broker: 65
Quantity: 1000
Rate: 303.50
Amount: 303500
```

## 11. CSV Floorsheet Import

Admin should be able to upload a CSV.

Create endpoint:

```text
POST /api/admin/floorsheet/import/
```

CSV example:

```csv
contract_number,symbol,buyer_broker,seller_broker,quantity,rate,amount,trade_date
100001,ADBL,58,65,1000,303.5,303500,2026-08-13
100002,ADBL,33,56,500,304,152000,2026-08-13
```

Validate the file and prevent duplicate contract numbers.

## 12. Broker Analysis

Create broker analysis similar to professional Nepal stock market websites.

For a selected stock, calculate:

### Most Bought

Display:

```text
Broker
Quantity
Average Price
Amount
Percentage of Total
```

### Most Sold

Display:

```text
Broker
Quantity
Average Price
Amount
Percentage of Total
```

### Broker Net Holding

Calculate:

```text
Net Quantity = Total Buy Quantity - Total Sell Quantity
```

Display:

```text
Broker
Buy Quantity
Sell Quantity
Net Quantity
Average Buy Price
Average Sell Price
Net Amount
Percentage
```

Create endpoint:

```text
GET /api/stocks/ADBL/broker-analysis/
```

Support:

```text
?period=today
?period=1week
?period=1month
?period=3month
?period=6month
```

## 13. Broker Accumulation Analysis

Create a broker accumulation system.

Example:

```text
Broker 58

Today: +10,515
1 Week: +34,920
1 Month: +81,250
```

Automatically assign labels:

```text
Strong Accumulation
Moderate Accumulation
Neutral
Moderate Distribution
Strong Distribution
```

Use transparent rules based on net quantity and percentage of total trading.

Do not claim these labels guarantee price movement.

## 14. Broker Detail Page

Create:

```text
/brokers/58
```

Display:

```text
Broker name
Broker number

Most Bought Stocks
Most Sold Stocks
Net Accumulated Stocks
Net Distributed Stocks
Total Turnover
Total Buy Amount
Total Sell Amount
```

Add date filters.

## 15. Portfolio System

Create Portfolio model:

```text
id
user
name
created_at
```

Create Holding model:

```text
portfolio
stock
quantity
average_buy_price
total_investment
created_at
updated_at
```

Calculate automatically:

```text
Investment = quantity × average_buy_price

Current Value = quantity × current_price

Profit/Loss = Current Value - Investment

Return % = Profit/Loss / Investment × 100
```

Dashboard example:

```text
Total Investment: Rs. 250,000
Current Value: Rs. 278,500
Profit: Rs. 28,500
Return: 11.4%
```

## 16. Portfolio Holdings Table

Display:

```text
Stock
Quantity
Average Buy
Current Price
Investment
Current Value
Profit/Loss
Return %
```

Use positive and negative visual indicators.

## 17. Sector Allocation

Calculate portfolio allocation by sector.

Example:

```text
Commercial Bank: 35%
Hydropower: 25%
Insurance: 20%
Finance: 10%
Others: 10%
```

Display using a pie or donut chart.

## 18. Watchlist

Users can create their own watchlist.

Watchlist model:

```text
user
stock
created_at
```

Display:

```text
Symbol
LTP
Change %
Volume
Watch status
```

Allow:

```text
Add
Remove
```

## 19. Paper Trading

Implement a simulated trading system.

Do not connect directly to broker TMS for executing real money trades.

Create PaperTrade model:

```text
user
stock
trade_type
quantity
price
total_amount
status
created_at
```

Trade types:

```text
BUY
SELL
```

Example:

```text
NABIL
BUY
100 shares
Rs. 523
Total: Rs. 52,300
```

Create a virtual wallet.

Example:

```text
Starting Balance: Rs. 1,000,000
```

When user buys:

```text
wallet balance decreases
paper holding increases
```

When user sells:

```text
wallet balance increases
paper holding decreases
```

Prevent selling more shares than owned.

## 20. Paper Trading Dashboard

Display:

```text
Virtual Balance
Portfolio Value
Total Profit/Loss
Number of Trades
Win Rate
```

Show complete trade history.

## 21. Technical Analysis

Calculate:

```text
SMA 20
SMA 50
EMA 20
EMA 50
RSI 14
MACD
MACD Signal
```

Optional:

```text
Bollinger Bands
Support
Resistance
```

Create endpoint:

```text
GET /api/stocks/NABIL/technical-analysis/
```

Return:

```json
{
  "symbol": "NABIL",
  "sma_20": 510.2,
  "sma_50": 498.8,
  "rsi": 58.4,
  "macd": 5.2,
  "signal": 3.8
}
```

## 22. Technical Signal

Create a simple educational signal system.

Possible output:

```text
Strong Buy
Buy
Neutral
Sell
Strong Sell
```

Example rules can consider:

```text
Price vs SMA20
Price vs SMA50
RSI
MACD
Volume
```

Clearly show:

```text
This signal is generated using technical indicators and is for educational purposes only.
```

Do not present it as guaranteed financial advice.

## 23. Charts

Use Recharts or Chart.js.

Create:

### Stock Price Chart

```text
Candlestick if possible
otherwise line chart
```

### Volume Chart

### Portfolio Performance Chart

### Sector Allocation Chart

### Broker Buy/Sell Chart

### Broker Net Holding Chart

Support responsive layouts.

## 24. Market Data Source Architecture

Create a reusable market-data provider architecture.

Example:

```python
class MarketDataProvider:
    def get_market_summary(self):
        pass

    def get_stock_price(self, symbol):
        pass

    def get_historical_prices(self, symbol):
        pass

    def get_floorsheet(self):
        pass
```

Create:

```text
DemoDataProvider
CSVDataProvider
```

Leave support for:

```text
LiveAPIProvider
```

This will allow a real licensed NEPSE data API to be connected later without rewriting the entire system.

## 25. Do Not Scrape Unauthorized Websites

Do not hard-code scraping of third-party websites.

Do not bypass:

```text
authentication
CAPTCHA
Cloudflare
rate limits
paid APIs
broker login
TMS security
```

Use demo, imported, publicly permitted, or properly licensed data.

## 26. React Pages

Create:

```text
/
```

Dashboard

```text
/login
/register
/stocks
/stocks/:symbol
/brokers
/brokers/:brokerNumber
/portfolio
/watchlist
/paper-trading
/profile
/admin
```

## 27. Navigation Bar

Navbar:

```text
Logo

Dashboard
Stocks
Broker Analysis
Portfolio
Watchlist
Paper Trading

Search

Profile
Logout
```

## 28. UI Design

Create a professional financial dashboard.

Use:

* Responsive design
* Desktop and mobile support
* Sidebar or top navigation
* Cards
* Tables
* Charts
* Dropdown filters
* Search boxes
* Loading skeletons
* Empty states
* Error messages
* Pagination

Use a clean modern design inspired by stock-market dashboards, but do not directly copy another website's branding or layout.

## 29. Broker Analysis UI

The stock broker-analysis page should contain:

```text
Choose Ticker:
[ ADBL ▼ ]

View By:
[ Turnover Amount ▼ ]

Period:
[Today] [1 Week] [1 Month] [3 Month] [6 Month]

[Table] [Chart]
```

Below it display three sections:

```text
MOST BOUGHT

Broker | Qty | Avg Price | Amount | % Total
```

```text
MOST SOLD

Broker | Qty | Avg Price | Amount | % Total
```

```text
BROKER NET HOLDING

Broker | Qty | Avg Price | Amount | % Total
```

## 30. Database Relationships

Create correct relationships between:

```text
User
Stock
Broker
FloorSheet
Portfolio
Holding
Watchlist
PaperTrade
HistoricalPrice
```

Use foreign keys appropriately.

## 31. API Structure

Create REST APIs such as:

```text
/api/auth/
/api/stocks/
/api/brokers/
/api/floorsheet/
/api/portfolio/
/api/watchlist/
/api/paper-trading/
/api/analytics/
```

Use serializers, ViewSets, routers, permissions, filters, and pagination properly.

## 32. API Filters

Support filters such as:

```text
/api/stocks/?sector=Commercial%20Bank

/api/stocks/?search=NABIL

/api/floorsheet/?symbol=ADBL

/api/floorsheet/?broker=58

/api/stocks/ADBL/broker-analysis/?period=1month
```

## 33. Performance

Optimize large floorsheet calculations.

Use:

```text
database indexes
aggregation queries
annotate()
Sum()
Avg()
Count()
select_related()
prefetch_related()
```

Avoid N+1 queries.

## 34. Security

Implement:

* JWT authentication
* Password hashing
* Backend permission checks
* Input validation
* CORS configuration
* Environment variables
* Protected admin endpoints
* CSV validation
* File-size limits
* SQL injection protection through Django ORM
* XSS-safe frontend practices

Never expose:

```text
SECRET_KEY
database passwords
API keys
```

Use:

```text
.env
```

Provide:

```text
.env.example
```

## 35. Error Handling

Create proper backend error responses.

Example:

```json
{
  "error": "Stock not found"
}
```

Frontend should display user-friendly error messages.

## 36. Loading States

Add:

```text
Loading...
Skeleton cards
Skeleton tables
Disabled buttons during requests
```

## 37. Demo Data

Create a Django management command:

```bash
python manage.py seed_data
```

Seed at least:

```text
20 stocks
20 brokers
90 days historical prices
500+ floorsheet transactions
demo users
demo portfolio
demo watchlist
paper trades
```

Use realistic-looking but clearly demo-generated data.

## 38. Testing

Backend testing should include:

```text
Authentication tests
Stock API tests
Portfolio tests
Floorsheet tests
Broker aggregation tests
Paper trading tests
Permissions tests
```

Frontend testing should include important components and API handling where practical.

## 39. README

Create a detailed README including:

```text
Project Overview
Features
Technology Stack
Folder Structure
Installation
Backend Setup
Frontend Setup
Database Setup
Environment Variables
Seed Data
How to Run
API Endpoints
Screenshots section
Future Improvements
Disclaimer
```

## 40. Installation Commands

Backend:

```bash
cd backend

python -m venv venv

source venv/bin/activate
```

For Windows:

```bash
venv\Scripts\activate
```

Install:

```bash
pip install django
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install django-cors-headers
pip install psycopg2-binary
pip install pandas
pip install python-dotenv
```

Frontend:

```bash
npm create vite@latest frontend -- --template react

cd frontend

npm install

npm install axios
npm install react-router-dom
npm install recharts
```

Install and configure Tailwind CSS using its current recommended Vite setup.

## 41. Development Order

Build the project step by step in this order:

### Phase 1

Project setup.

```text
Django
React
PostgreSQL
CORS
REST Framework
```

### Phase 2

Authentication.

```text
Register
Login
JWT
Profile
```

### Phase 3

Stock system.

```text
Stocks
Historical data
Search
Stock details
```

### Phase 4

Floorsheet and brokers.

```text
Broker model
Floorsheet model
CSV import
```

### Phase 5

Broker analytics.

```text
Most Bought
Most Sold
Net Holding
Accumulation
Distribution
```

### Phase 6

Portfolio.

```text
Portfolio
Holdings
Profit/Loss
Sector allocation
```

### Phase 7

Watchlist.

### Phase 8

Paper trading.

### Phase 9

Technical analysis.

### Phase 10

Charts and dashboard.

### Phase 11

Admin tools.

### Phase 12

Testing, responsive design, documentation, and deployment preparation.

## 42. Coding Requirements

Generate complete working code.

Do not provide only pseudocode.

For every file:

1. Show its exact path.
2. Provide complete code.
3. Explain where it belongs.
4. Mention required dependencies.
5. Ensure imports are correct.
6. Ensure frontend and backend APIs match.
7. Do not leave essential functionality as TODO.
8. Keep components reusable.
9. Follow Django and React best practices.

## 43. Important Development Rule

Do not attempt to generate the entire codebase in one response.

Build it incrementally.

For each phase:

```text
1. Show folder structure.
2. Create backend files.
3. Create frontend files.
4. Give terminal commands.
5. Explain migrations.
6. Explain how to run.
7. Give a test checklist.
8. Wait for confirmation before proceeding to the next major phase.
```

When fixing an error, modify the existing code instead of restarting the project.

## 44. Final Goal

The completed project should allow a user to:

```text
Register
        ↓
Login
        ↓
NEPSE Dashboard
        ↓
Search Stock
        ↓
Stock Detail
        ├── Price Chart
        ├── Technical Analysis
        └── Broker Analysis
                 ↓
          Most Bought
          Most Sold
          Net Holding
          Accumulation
                 ↓
Portfolio
        ├── Holdings
        ├── Profit/Loss
        └── Sector Allocation
                 ↓
Watchlist
                 ↓
Paper Trading
                 ↓
Performance Analysis
```

The finished system should feel like a simplified Nepal stock-market analytics platform rather than a basic CRUD university project.

Start now with **Phase 1: Project Setup**.

Give me:

* Final folder structure
* Backend setup commands
* Django project creation
* Required Django apps
* PostgreSQL configuration
* REST Framework configuration
* CORS configuration
* Environment-variable setup
* React + Vite setup
* Tailwind setup
* Axios setup
* Initial frontend folder structure
* Backend and frontend run commands
* First test to verify React can successfully communicate with Django
