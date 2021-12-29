import requests
import os
import argparse
import json
import logging
import datetime
from datetime import timezone
import datetime as DT
import csv
import time
import pandas as pd

LOG_DIR = "logs/coinbasepro"
DATA_DIR = "data/coinbasepro"
REST_URL = 'https://api.exchange.coinbase.com/products/{}/candles?granularity={}&start={}&end={}'
# REST_URL = "https://api.exchange.coinbase.com/products/{}/candles"

OHLCV_DATA = []

#2018-01-01T01:39:00.0000001Z -> 2018-01-01T01:39:00.000000Z -> 1514770740000 (UTC)
def coinapi_timestamp_to_epoch_milliseconds(timestamp):
    #Truncate the (10^-7)th 0...
    truncated = timestamp[:26] + timestamp[27:]
    truncated = datetime.datetime.strptime(truncated, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=datetime.timezone.utc)
    return (int)(truncated.timestamp() * 1000)
    
def convert_candle_to_dict_entry(candle):
    entry = {
        "timestamp" : int(candle[0]),
        "open" : candle[3],
        "high" : candle[2],
        "low" : candle[1],
        "close" : candle[4],
        "volume" : candle[5]

    }
    return entry

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Discord Webhook
discord_webhook = os.environ.get('DISCORD_WEBHOOK_URL')

# Parse Arguments
parser = argparse.ArgumentParser()
parser.add_argument('--market', type=str)
parser.add_argument('--startDate', type=int)
parser.add_argument('--endDate', type=int)
parser.add_argument('--resolution', type=str)
args = parser.parse_args()

# Setup Logger
logfile= LOG_DIR + "/{}.{}.{}.{}".format(args.market, args.resolution, args.startDate, args.endDate)
logging.basicConfig(filename=logfile, 
format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

symbol = args.market
startDate = args.startDate
endDate = args.endDate
resolution = args.resolution

# Convert to UTC time
startDateObj = DT.datetime.utcfromtimestamp(startDate / 1000.0).replace(tzinfo=datetime.timezone.utc)
endDateObj = DT.datetime.utcfromtimestamp(endDate / 1000.0).replace(tzinfo=datetime.timezone.utc)

if args.resolution == '1m':
    deltaTimeObj = datetime.timedelta(minutes=300) # CoinbasePro limits the number of candles per request to 300
    granularity = 60
else:
    logging.error("Unsupported resolution.")
    sys.exit(1)

header = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'trades_count']
filename = DATA_DIR + "/{}.{}.{}.{}.csv".format(args.market, args.resolution, args.startDate, args.endDate)
logging.info("Saving OHLCV data to: %s", filename)

while startDateObj <= endDateObj:
    endDateObjTemp = startDateObj + deltaTimeObj
    url = REST_URL.format(
        symbol,
        granularity,
        startDateObj.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        endDateObjTemp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    )

    logging.info("Fetching OHLCV Data: " + url)
    response = requests.get(url)
    logging.info("Response Headers: {}".format(response.headers))

    if len(response.json()) < 100:
        logging.warn("Less than 100 candles returned for time interval beginning at {}".format(startDateObj))
    for candle in response.json():
        OHLCV_DATA.append(convert_candle_to_dict_entry(candle))

    time.sleep(0.25) # TODO: Add proper rate handling
    startDateObj += deltaTimeObj

# Output to CSV
df = pd.DataFrame(OHLCV_DATA)
df = df.set_index('timestamp')
df = df.sort_index(ascending=True)
df.to_csv(filename, index=True)

if discord_webhook :
    r = requests.post(discord_webhook,
    json={"content": "Finished scraping data to: {}".format(filename)})