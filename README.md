# 📊 Stock Monitoring Dashboard with Real-Time Alerts

A professional stock monitoring system that tracks 18 holdings with real-time price updates, abnormal movement detection, and automated email alerts.

## Features

✅ **Real-Time Monitoring**
- Live price updates for 18 holdings (MSTR, TSM, LMT, AAPL, MSFT, GOOGL, AMZN, NVDA, META, TSLA, JPM, HOOD, AVGO, MU, UAL, COIN, IBIT, QQQ)
- 60-second refresh interval with 0.2s rate limiting
- Technical indicators: RSI (14-period), MACD, intraday % change

✅ **Abnormal Movement Detection**
- Alerts trigger when 2%+ intraday price breaks detected
- RSI extremes (>70 overbought, <30 oversold)
- Volume spikes (2x average volume)
- Emergency alerts when 3+ holdings show abnormal activity

✅ **Interactive Web Dashboard**
- Professional dark theme UI with gradient headers
- Grid and table view options
- Live statistics: top gainers, top losers, average change
- Auto-refreshing every 60 seconds
- Mobile-responsive design

✅ **Automated Email Alerts**
- Hourly market update emails (10:30 AM CST start, every hour)
- Emergency abnormal activity alerts (when 3+ holdings affected)
- Professional HTML emails with color-coded tables
- Sent to: eshaanmahajan773@gmail.com

✅ **Production Ready**
- Flask backend with CORS enabled
- Docker support for containerization
- Gunicorn WSGI server
- Ready for Render.com / Railway deployment
- 60-second performance cache

## Quick Start

### Local Testing
```bash
python app.py
# Open http://localhost:5000
```

### Docker
```bash
docker-compose up
# Open http://localhost:5000
```

## Cloud Deployment

### Railway.app
1. Push to GitHub
2. Connect Railway.app to GitHub repo
3. Add env var: `COMPOSIO_API_KEY`
4. Deploy!

### Render.com
1. Push to GitHub
2. Connect Render to GitHub repo
3. Set start command: `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`
4. Add env var: `COMPOSIO_API_KEY`

## API Endpoints

- `GET /` - Dashboard HTML
- `GET /api/stocks` - All stocks data (cached 60s)
- `GET /api/stocks/<ticker>` - Single stock data
- `GET /api/status` - System status and market info

## Files

- `app.py` - Flask backend server with real-time data fetching
- `dashboard.html` - Interactive web dashboard UI
- `requirements.txt` - Python dependencies
- `holdings_config.json` - Portfolio configuration (18 tickers)
- `Dockerfile` - Docker image definition
- `Procfile` - Render/Heroku deployment config
- `docker-compose.yml` - Local Docker Compose setup

## Configuration

Edit `holdings_config.json` to customize:
- Holdings list (tickers and exchanges)
- Alert thresholds (price break %, RSI zones, etc.)
- Email settings
- Timezone

## Next Steps

1. ✅ System fully built and tested
2. ✅ Dashboard with real-time data ready
3. ✅ Deployment files ready
4. Deploy to Railway or Render
5. Monitor dashboard for live stock data
6. Receive automated alerts in Gmail

---

**Status:** Production Ready ✅
**Created by:** Composio Agent 🔥
