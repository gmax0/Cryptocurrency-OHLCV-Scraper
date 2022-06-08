### Installation

```
pip install py-cc-ohlcv
```

### Example

Instantiate a scraper with your desired exchange, instrument, resolution, start and end dates:

```
from py_cc_ohlcv import scraper, exchanges
from datetime import datetime, timezone, timedelta
import logging

logging.basicConfig(level = logging.INFO)

# Set a start and end date
start_date = datetime(2022, 1, 1)
start_date = start_date.replace(tzinfo=timezone.utc)
end_date = start_date + timedelta(hours=24)

# Initialize Scraper
#cb_scraper = scraper.Scraper(exchanges.COINBASE_PRO, "BTC_USD", "1m", start_date, end_date)

# Set Proxies if desired
proxies = {
    "http": "http://0.0.0.0:8000",
    "https": "https://0.0.0.0:8000",
}
cb_scraper.set_proxies(proxies)

# Begin scrapping
candles_df = cb_scraper.run()
print(candles_df)

```

### Extensibility

The original purpose of these adhoc scripts was to scrape and ingest historical OHLCV data stemming from 2018 for hundreds of markets. 

Parallelism can be implemented with this library by simply running multiple Python processes, each tasked with scraping a set window for a given market by sending requests through a separate http proxy to avoid IP-based ratelimiting by exchange APIs.
