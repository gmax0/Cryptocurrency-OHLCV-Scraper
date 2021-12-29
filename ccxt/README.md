## ccxt-scraper.py
The [ccxt](https://github.com/ccxt/ccxt) package is used to query exchange APIs. See ccxt's [manual](https://github.com/ccxt/ccxt/wiki/Manual#ohlcv-candlestick-charts) for OHLCV implementation details and supported exchanges.

Note that some exchange APIs do not offer comprehensive OHLC data through their historical data endpoints and only return data for the last X number of hours.

### Dependencies
- python3
- [ccxt](https://github.com/ccxt/ccxt#install)

### Setup
Optional if you'd like to enable a Discord alert for when a job completes: 

```export DISCORD_WEBHOOK_URL=https://discordapp.com/api/webhooks/{your webhook uid}```

### Execution 
All times are in UTC.

```python3 ccxt-scraper.py --startDate 2018-01-01 --endDate 2020-01-01 --resolution 1m --exchange coinbasepro --pricepair ETH/USD```

## Outputs
A .csv will be output to your present working directory under the name: data/{ccxt or coinapi}/{start date}.{end date}.{exchange}.{pricepair}.{resolution}

