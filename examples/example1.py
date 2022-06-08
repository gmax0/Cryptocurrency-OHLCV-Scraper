from py_cc_ohlcv import scraper, exchanges
from datetime import datetime, timezone, timedelta
import logging

# Set Logger
logging.basicConfig(level = logging.INFO)
# logging.basicConfig(level = logging.DEBUG)

# Set a start and end date
start_date = datetime(2022, 1, 1)
start_date = start_date.replace(tzinfo=timezone.utc)
end_date = start_date + timedelta(hours=24)

# Initialize Scraper
# cb_scraper = scraper.Scraper(exchanges.COINBASE_PRO, "BTC_USD", "1m", start_date, end_date)
#cb_scraper = scraper.Scraper(exchanges.BINANCE, "BTC_USDT", "1m", start_date, end_date)
# cb_scraper = scraper.Scraper(exchanges.BINANCE_US, "BTC_USDT", "1m", start_date, end_date)
# cb_scraper = scraper.Scraper(exchanges.FTX, "BTC_USD", "1m", start_date, end_date)
cb_scraper = scraper.Scraper(exchanges.KUCOIN, "BTC_USDT", "1m", start_date, end_date)
# cb_scraper = scraper.Scraper(exchanges.GEMINI, "BTC_USD", "1m", datetime.now(timezone.utc) - timedelta(hours=24), datetime.now(timezone.utc)) 

proxies = {
    "http": "http://0.0.0.0:8000",
    "https": "https://0.0.0.0:8000",
}
#cb_scraper.set_proxies(proxies)

# Begin scrapping
candles_df = cb_scraper.run()
print(candles_df)
