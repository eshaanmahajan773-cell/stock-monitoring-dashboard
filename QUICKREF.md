# QUICK REFERENCE GUIDE

## 🚀 RUN LOCALLY (3 STEPS)

```bash
pip install -r requirements.txt
python app.py
```

Then open: http://localhost:5000

## 📊 DASHBOARD FEATURES

1. **Real-Time Grid View**
   - Each card shows: ticker, price, % change, RSI, MACD
   - Green card = gaining, Red card = losing
   - 🚨 Alert badge if 2%+ move detected

2. **Live Statistics**
   - Top gainer & loser
   - Average portfolio change
   - Data quality (X/18 holdings fetched)

3. **Auto-Refresh**
   - Every 60 seconds automatically
   - Manual refresh button available
   - Pause/resume auto-refresh

## 📡 API ENDPOINTS (for custom integrations)

```bash
# Get all stocks data
curl http://localhost:5000/api/stocks

# Get single stock
curl http://localhost:5000/api/stocks/AAPL

# Get system status
curl http://localhost:5000/api/status
```

## 🎨 CUSTOMIZATION

**Change holdings:**
Edit `holdings_config.json` - add/remove tickers

**Change refresh interval:**
In `app.py`, change `cache_ttl = 60` to desired seconds

**Adjust alert thresholds:**
In `holdings_config.json`, modify `price_break_percent` (default: 2.0%)

## 🐳 DOCKER COMMANDS

```bash
# Run with Docker Compose
docker-compose up --build
```

## ☁️ DEPLOY TO RAILWAY

1. Push repo to GitHub
2. Go to railway.app
3. New Project → GitHub Repo
4. Add env var: COMPOSIO_API_KEY
5. Deploy!

Railway will auto-detect Procfile and run the app.

## 📊 DATA FLOW

```
Dashboard (HTML/JS)
    ↓
Flask API (/api/stocks)
    ↓
COMPOSIO_SEARCH_FINANCE
    ↓
Real-time stock quotes
    ↓
Cache (60s) + Display
```

---

**Everything is ready! Choose your deployment method and go live! 🚀**
