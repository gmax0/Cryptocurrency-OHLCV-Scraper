### Installation

```
pip install py-cc-ohlcv
```

### Supported Exchanges

Supported exchanges are located in `py_cc_ohlcv/exchanges.py`

Currently supported spot exchanges and resolutions (instruments formatted as "SPOT_COUNTER"):

- BINANCE
    - `1m`, `5m`, `15m`, `1h`, `6h`, `1d`
- BINANCE_US
    - `1m`, `5m`, `15m`, `1h`, `6h`, `1d`
- COINBASE_PRO
    - `1m`, `5m`, `15m`, `1h`, `6h`, `1d`
- FTX
    - `1m`
- GEMINI (limited to previous 24 hours worth of data, set start and end date accordingly)
    - `1m`, `5m`, `15m`, `1h`, `6h`, `1d`
- KUCOIN
    - `1m`

Currently supported derivative exchanges and resolutions:

- In progress

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
cb_scraper = scraper.Scraper(exchanges.COINBASE_PRO, "BTC_USD", "1m", start_date, end_date) # See supported exchanges

# Set Proxies if desired
proxies = {
    "http": "http://0.0.0.0:8000",
    "https": "https://0.0.0.0:8000",
}
cb_scraper.set_proxies(proxies)

# Begin scrapping
candles_df = cb_scraper.run() # Returns a pandas DataFrame
print(candles_df)

### Example candles_df output 

                   open     high      low    close     volume
open_timestamp                                               
1640995200000   46216.4  46271.5  46210.4  46245.4   4.786154
1640995260000   46245.4  46326.9  46230.9  46293.4  17.923909
1640995320000   46302.3  46370.5  46280.2  46359.8  17.375017
1640995380000   46359.7  46382.9  46309.8  46322.8   5.070697
1640995440000   46322.7  46329.2  46289.9  46316.8   3.413937
...                 ...      ...      ...      ...        ...
1641081300000   47691.4  47768.0  47658.1  47744.0  20.075448
1641081360000   47743.9  47762.2  47715.6  47751.1   6.398773
1641081420000   47751.9  47807.7  47719.2  47772.3   5.682060
1641081480000   47779.9  47779.9  47732.8  47732.8   5.560245
1641081540000   47732.8  47752.9  47715.6  47728.6   5.781858

###
```

### Extensibility

The original purpose of these adhoc scripts was to scrape and ingest historical OHLCV data stemming from 2018 for hundreds of markets. 

Parallelism can be implemented with this library by simply running multiple Python processes, each tasked with scraping a set window for a given market by sending requests through a separate http proxy to avoid IP-based ratelimiting by exchange APIs.

### Known Issues

- Kucoin occasionally responds with a 429 error code when rate limit has not been reached.
- Gemini limits historical OHLCV retrieval to the past 24 hours