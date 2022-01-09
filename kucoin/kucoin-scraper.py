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

LOG_DIR = "logs/kucoin"
DATA_DIR = "data/kucoin"
REST_URL = 'https://api.kucoin.com/api/v1/market/candles?type={}&symbol={}&startAt={}&endAt={}'

OHLCV_DATA = []

def convert_candle_to_dict_entry(candle):
    entry = {
        "timestamp" : int(DT.datetime.utcfromtimestamp(int(candle[0])).replace(tzinfo=DT.timezone.utc).timestamp() * 1000),
        "open" : float(candle[1]),
        "high" : float(candle[3]),
        "low" : float(candle[4]),
        "close" : float(candle[2]),
        "volume" : float(candle[5])
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
    deltaTimeObj = datetime.timedelta(minutes=1500) # Set at a max of 1500 candles / call 
    granularity = '1min'
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
        granularity,
        symbol,
        int(startDateObj.timestamp()),
        int(endDateObjTemp.timestamp())
    )

    logging.info("Fetching OHLCV Data: " + url)
    response = requests.get(url)
    logging.info("Response Headers: {}".format(response.headers))
    logging.info("Number of Candles: {}".format(len(response.json()['data'])))

    # if len(response.json()) < 100:
        # logging.warn("Less than 100 candles returned for time interval beginning at {}".format(startDateObj))
    
    for candle in response.json()['data']:
        OHLCV_DATA.append(convert_candle_to_dict_entry(candle))

    time.sleep(10) # TODO: Add proper rate handling
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