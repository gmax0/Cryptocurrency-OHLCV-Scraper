import requests
import os
import argparse
import json
import logging
import datetime
import datetime as DT
import time
import pandas as pd
import sys
import boto3

LOG_DIR = "logs/ftx"
DATA_DIR = "data/ftx"
REST_URL = 'https://ftx.com/api/markets/{}/candles?resolution={}&start_time={}&end_time={}'

OHLCV_DATA = []

def convert_candle_to_dict_entry(candle):
    entry = {
        "timestamp" : int(DT.datetime.strptime(candle['startTime'], "%Y-%m-%dT%H:%M:%S+00:00").replace(tzinfo=DT.timezone.utc).timestamp() * 1000),
        "open" : candle['open'],
        "high" : candle['high'],
        "low" : candle['low'],
        "close" : candle['close'],
        "volume" : candle['volume']

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
logfile= LOG_DIR + "/{}.{}.{}.{}".format(args.market.replace('/', '-'), args.resolution, args.startDate, args.endDate)
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
    deltaTimeObj = datetime.timedelta(minutes=300) # TODO: Check FTX's max interval size
    granularity = 60
elif args.resolution == '1s':
    deltaTimeObj = datetime.timedelta(minutes=20)
    granularity = 15
else:
    logging.error("Unsupported resolution.")
    sys.exit(1)

header = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'trades_count']
filename = DATA_DIR + "/{}.{}.{}.{}.csv".format(args.market.replace('/', '-'), args.resolution, args.startDate, args.endDate)
logging.info("Saving OHLCV data to: %s", filename)

while startDateObj < endDateObj:
    endDateObjTemp = startDateObj + deltaTimeObj
    if (endDateObjTemp > endDateObj):
        endDateObjTemp = endDateObj
        
    url = REST_URL.format(
        symbol,
        granularity,
        startDateObj.timestamp(),
        endDateObjTemp.timestamp()
    )

    logging.info("Fetching OHLCV Data: " + url)
    response = requests.get(url)
    logging.info("Response Headers: {}".format(response.headers))
    logging.info("Response Candle Count: {}".format(len(response.json()['result'])))

    # if len(response.json()) < 100:
        # logging.warn("Less than 100 candles returned for time interval beginning at {}".format(startDateObj))
    
    for candle in response.json()['result']:
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

if discord_webhook :
    r = requests.post(discord_webhook,
    json={"content": "Finished scraping data to: {}".format(filename)})

if s3_bucket_name:
    s3 = boto3.resource('s3')
    s3.Bucket(s3_bucket_name).upload_file(filename, filename)