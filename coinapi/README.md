## coinapi-scraper.py
This script integrates with CoinAPI, a 3rd party service that catalogues cryptocurrency price data across exchanges. An API key is required to use this script. 

### Dependencies
- python3

### Setup
Required:

```export COINAPI_KEY={your api key}```

Optional if you'd like to enable a Discord alert for when a job completes: 

```export DISCORD_WEBHOOK_URL=https://discordapp.com/api/webhooks/{your webhook uid}```

### Execution 
All times are in UTC.

```python3 coinapi-scraper.py --symbol COINBASE_SPOT_ETH_USD --startDate 2018-01-01T00:00:00 --endDate 2018-01-02T00:00:00 --resolution 1MIN```

The full range of resolutions supported by CoinAPI is NOT supported by this script. Anything besides 1MIN will fail.

## Outputs
A .csv will be output to your present working directory under the name: data/{ccxt or coinapi}/{start date}.{end date}.{exchange}.{pricepair}.{resolution}

