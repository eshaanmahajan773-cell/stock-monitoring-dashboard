from flask import Flask, jsonify
from flask_cors import CORS
import json
import time
from datetime import datetime, timedelta
import pytz
import threading

app = Flask(__name__)
CORS(app)

# Load holdings config
with open('/tmp/holdings_config.json') as f:
    CONFIG = json.load(f)

SYMBOLS = CONFIG['symbols']
THRESHOLDS = CONFIG['thresholds']

# Cache for performance
data_cache = {'stocks': [], 'timestamp': None, 'last_fetch': None}
cache_ttl = 60  # 60 seconds

def parse_price(price_str):
    """Parse price from string like 'USD123.45' to float."""
    if isinstance(price_str, (int, float)):
        return float(price_str)
    if isinstance(price_str, str):
        clean = price_str.replace('USD', '').replace('$', '').strip()
        return float(clean)
    return 0.0

def fetch_stock_data(symbol):
    """Fetch real-time data for a single stock."""
    try:
        result, error = run_composio_tool("COMPOSIO_SEARCH_FINANCE", {
            "query": symbol,
            "window": "1Y",
            "hl": "en"
        })
        
        if error:
            return None
        
        data = result.get('data', {}).get('results', {})
        if not data or not data.get('summary'):
            return None
        
        summary = data['summary']
        ticker = symbol.split(':')[0]
        
        # Extract prices
        current_price = parse_price(summary.get('extracted_price') or 0)
        open_price = parse_price(summary.get('opening_price') or current_price)
        
        # Calculate intraday change
        intraday_change = 0
        if open_price > 0:
            intraday_change = ((current_price - open_price) / open_price) * 100
        
        # Detect abnormal movement
        is_alert = abs(intraday_change) >= THRESHOLDS['price_break_percent']
        signal = "STRONG" if intraday_change > 0 else ("WEAK" if intraday_change < 0 else "NEUTRAL")
        
        # Generate mock RSI (in production, fetch from FINAGE_GET_TECHNICAL_INDICATORS)
        mock_rsi = 50 + (intraday_change * 2)  # Simplified for demo
        mock_rsi = max(0, min(100, mock_rsi))  # Clamp 0-100
        
        return {
            'ticker': ticker,
            'symbol': symbol,
            'price': round(current_price, 2),
            'change': round(intraday_change, 2),
            'rsi': round(mock_rsi, 1),
            'macd': round(intraday_change * 0.5, 2),  # Simplified MACD
            'volume': 'N/A',
            'alerts': 1 if is_alert else 0,
            'signal': signal,
            'is_alert': is_alert
        }
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None

def fetch_all_stocks():
    """Fetch data for all holdings with rate limiting."""
    stocks = []
    print(f"[{datetime.now().isoformat()}] Fetching real-time data for {len(SYMBOLS)} stocks...")
    
    for i, symbol in enumerate(SYMBOLS, 1):
        stock = fetch_stock_data(symbol)
        if stock:
            stocks.append(stock)
            print(f"  ✅ [{i:2d}/18] {stock['ticker']} | ${stock['price']:.2f} | {stock['change']:+.2f}%")
        else:
            print(f"  ❌ [{i:2d}/18] {symbol}")
        
        # Rate limit: 0.2s between requests
        if i < len(SYMBOLS):
            time.sleep(0.2)
    
    cst = pytz.timezone('America/Chicago')
    timestamp = datetime.now(cst).strftime('%Y-%m-%d %H:%M:%S %Z')
    
    # Update cache
    global data_cache
    data_cache = {
        'stocks': sorted(stocks, key=lambda x: x['change'], reverse=True),
        'timestamp': timestamp,
        'last_fetch': time.time(),
        'total_holdings': len(SYMBOLS),
        'successful': len(stocks),
        'alerts': len([s for s in stocks if s['alerts'] > 0])
    }
    
    return data_cache

@app.route('/api/stocks', methods=['GET'])
def get_stocks():
    """Get all stocks data with caching."""
    if data_cache['last_fetch'] and time.time() - data_cache['last_fetch'] < cache_ttl:
        return jsonify(data_cache)
    
    # Fetch fresh data
    return jsonify(fetch_all_stocks())

@app.route('/api/stocks/<ticker>', methods=['GET'])
def get_stock(ticker):
    """Get single stock data."""
    # Fetch fresh for single stock
    symbol = f"{ticker.upper()}:NASDAQ"  # Default to NASDAQ, could be smarter
    stock = fetch_stock_data(symbol)
    
    if not stock:
        # Try NYSE
        symbol = f"{ticker.upper()}:NYSE"
        stock = fetch_stock_data(symbol)
    
    if stock:
        return jsonify(stock)
    return jsonify({'error': 'Stock not found'}), 404

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get system status and market info."""
    cst = pytz.timezone('America/Chicago')
    now = datetime.now(cst)
    
    # Determine market status
    hour = now.hour
    minute = now.minute
    is_open = 9 <= hour <= 16 or (hour == 8 and minute >= 30)
    
    return jsonify({
        'timestamp': now.isoformat(),
        'market_status': 'OPEN' if is_open else 'CLOSED',
        'cache_status': {
            'last_update': data_cache['timestamp'],
            'last_fetch_age': time.time() - data_cache['last_fetch'] if data_cache['last_fetch'] else None,
            'holdings_scanned': data_cache['successful'],
            'alerts_active': data_cache['alerts']
        }
    })

@app.route('/', methods=['GET'])
def index():
    """Serve the dashboard HTML."""
    with open('dashboard.html', 'r') as f:
        return f.read()

if __name__ == '__main__':
    # Initial data fetch
    fetch_all_stocks()
    
    # Background thread to refresh data every 60 seconds
    def background_refresh():
        while True:
            time.sleep(60)
            fetch_all_stocks()
    
    refresh_thread = threading.Thread(target=background_refresh, daemon=True)
    refresh_thread.start()
    
    # Start Flask server
    print("\n" + "="*60)
    print("🚀 FLASK SERVER STARTING")
    print("="*60)
    print("📊 Dashboard: http://localhost:5000")
    print("📡 API: http://localhost:5000/api/stocks")
    print("="*60 + "\n")
    
    app.run(debug=False, host='0.0.0.0', port=5000)
