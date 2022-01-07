import requests
import os
import argparse
import json
import logging
import datetime
from datetime import timezone
import datetime as DT
import time
import pandas as pd
import sys
import boto3

LOG_DIR = "logs/bitstamp"
DATA_DIR = "data/bitstamp"
REST_URL = "https://www.bitstamp.net/api/v2/ohlc/{}/?step={}&start={}&end={}&limit=1000"

OHLCV_DATA = []

def convert_candle_to_dict_entry(candle):
    entry = {
        "timestamp" : int(DT.datetime.utcfromtimestamp(int(candle['timestamp'])).replace(tzinfo=DT.timezone.utc).timestamp() * 1000),
        "open" : float(candle['open']),
        "high" : float(candle['high']),
        "low" : float(candle['low']),
        "close" : float(candle['close']),
        "volume" : float(candle['volume'])
    }
    return entry

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Discord Webhook
discord_webhook = os.environ.get('DISCORD_WEBHOOK_URL')

# S3 Bucket Name
s3_bucket_name = os.environ.get('S3_BUCKET_NAME')

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
startDateSeconds = startDate / 1000.0
endDateSeconds = endDate / 1000.0

startDateObj = DT.datetime.utcfromtimestamp(startDateSeconds).replace(tzinfo=datetime.timezone.utc)
endDateObj = DT.datetime.utcfromtimestamp(endDateSeconds).replace(tzinfo=datetime.timezone.utc)

if args.resolution == '1m':
    deltaTimeObj = datetime.timedelta(minutes=1000) 
    startDateOffset = datetime.timedelta(minutes=1) # Bitstamp OHLCV intervals are open bounded at their start
    granularity=60
else:
    logging.error("Unsupported resolution.")
    sys.exit(1)

filename = DATA_DIR + "/{}.{}.{}.{}.csv".format(args.market, args.resolution, args.startDate, args.endDate)
logging.info("Saving OHLCV data to: %s", filename)

while startDateObj < endDateObj:
    endDateObjTemp = startDateObj + deltaTimeObj
    if (endDateObjTemp > endDateObj):
        endDateObjTemp = endDateObj

    url = REST_URL.format(
        symbol,
        granularity,
        int((startDateObj - startDateOffset).timestamp()),
        int(endDateObjTemp.timestamp())
    )

    logging.info("Fetching OHLCV Data: " + url)
    response = requests.get(url)
    logging.info("Response Headers: {}".format(response.headers))
    logging.info("Number of Candles: {}".format(len(response.json()['data']['ohlc'])))

    for candle in response.json()['data']['ohlc']:
        OHLCV_DATA.append(convert_candle_to_dict_entry(candle))

    time.sleep(0.25) # TODO: Add proper rate handling
    startDateObj += deltaTimeObj

# Output to CSV
df = pd.DataFrame(OHLCV_DATA)
df = df.set_index('timestamp')
df = df.sort_index(ascending=True)
df = df.drop_duplicates()
df = df.truncate(after=endDate)

df.to_csv(filename, index=True)

if discord_webhook:
    r = requests.post(discord_webhook,
    json={"content": "Finished scraping data to: {}".format(filename)})

if s3_bucket_name:
    s3 = boto3.resource('s3')
    s3.Bucket(s3_bucket_name).upload_file(filename, filename)