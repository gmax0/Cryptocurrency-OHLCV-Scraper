To be updated...

### AWS Setup

1. Export your credentials

``` 
export AWS_ACCESS_KEY_ID="YOUR ACCESS KEY"
export AWS_SECRET_ACCESS_KEY="YOUR SECRET ACCESS KEY"
export AWS_DEFAULT_REGION="REGION"
```

### Installation

```
pip install py-cc-ohlcv
```

### Example

Instantiate a scraper with your desired exchange, instrument, start+end dates:

```
from py-cc-ohlcv import scraper, exchanges, instruments
from datetime import datetime

end_date = datetime.now(datetime.timezone.utc)
start_date = end_date - datetime.timedelta(hours=24) # Set a window from [present - 24 hours, present]

cb_scraper = scraper(exchanges.COINBASE_PRO, instruments.BTC_USD, start_date, end_date)
cb_scraper.set_proxy('http://0.0.0.0:8000') 
cb_scraper.start()

```

### Extensibility

The original purpose of these adhoc scripts was to scrape and ingest historical OHLCV data stemming from 2018 for hundreds of markets. 

Parallelism can be implemented with this library by simply running multiple Python processes, each tasked with scraping a set window for a given market by sending requests through a separate http proxy to avoid IP-based ratelimiting by exchange APIs.