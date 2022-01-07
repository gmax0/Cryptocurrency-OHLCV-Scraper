## Dependencies
- python3
- pandas

## Setup
Optional if you'd like to enable a Discord alert for when a job completes: 

```export DISCORD_WEBHOOK_URL=https://discordapp.com/api/webhooks/{your webhook uid}```

## Usage

```
python3 kucoin-scraper.py \
--startDate 1609459200000 \
--endDate 1609545600000 \
--resolution 1m \
--market BTC-USDT
```

Execution of the above command will scrape ```1m``` OHLCV data for ```BTC-USDT``` for the time range: ```[1609459200000, 1609459200000]```

Option | Description
--- | ---
--startDate | Unix timestamp (ms) of the start interval
--endDate | Unix timestamp (ms) of the end interval
--resolution | Supported resolutions: ```1m```
--market | Supported markets: ```SPOT```

For a list of market symbols, see 
https://api.kucoin.com/api/v1/symbols

## Outputs
A .csv will be output to your present working directory under the name: 
```data/kucoin/{market}.{resolution}.{startDate}.{endDate}```

A sample file is included in 
```data/kucoin```

