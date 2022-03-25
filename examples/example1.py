from py_cc_ohlcv import scraper, exchanges, instruments
from datetime import datetime, timezone, timedelta

# Set a window from [present - 24 hours, present]
end_date = datetime.now(timezone.utc)
start_date = end_date - timedelta(hours=24) 

# Initialize Scraper
cb_scraper = scraper.Scraper(exchanges.COINBASE_PRO, instruments.BTC_USD, start_date, end_date)
cb_scraper.set_http_proxy('http://0.0.0.0:8000') 

