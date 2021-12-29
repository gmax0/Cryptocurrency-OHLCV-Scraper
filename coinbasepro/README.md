## Dependencies
- python3

## Setup
Optional if you'd like to enable a Discord alert for when a job completes: 

```export DISCORD_WEBHOOK_URL=https://discordapp.com/api/webhooks/{your webhook uid}```

## Usage

```
python3 coinbasepro-scraper.py \
--startDate 1609459200000 \
--endDate 1609545600000 \
--resolution 1m \
--market ETH-USD
```

Option | Description
--- | ---
--startDate | Unix timestamp (ms) of the start interval
--endDate | Unix timestamp (ms) of the end interval
--resolution | Supported resolutions: ```1m```
--market | Supported markets: ```SPOT```

For a list of market symbols, see 
https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getproducts




## Outputs
A .csv will be output to your present working directory under the name: 
```data/coinbasepro/{market}.{resolution}.{startDate}.{endDate}```

