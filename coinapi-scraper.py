import requests
import os
import argparse
import json
import logging
import datetime
from datetime import timezone
import csv
import time

#2018-01-01T01:39:00.0000001Z -> 2018-01-01T01:39:00.000000Z -> 1514770740000 (UTC)
def coinapi_timestamp_to_epoch_milliseconds(timestamp):
    #Truncate the (10^-7)th 0...
    truncated = timestamp[:26] + timestamp[27:]
    truncated = datetime.datetime.strptime(truncated, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=datetime.timezone.utc)
    return (int)(truncated.timestamp() * 1000)
    
def convert_candle_to_csv_entry(candle):
    entry = [coinapi_timestamp_to_epoch_milliseconds(candle.get('time_period_start')),
             candle.get('price_open'), 
             candle.get('price_high'), 
             candle.get('price_low'), 
             candle.get('price_close'), 
             candle.get('volume_traded'), 
             candle.get('trades_count')]
    return entry

if not os.path.exists('data/coinapi/'):
    os.makedirs('data/coinapi/')

if not os.path.exists('logs/coinapi/'):
    os.makedirs('logs/coinapi')

req_headers = {'X-CoinAPI-Key' : os.environ.get('COINAPI_KEY')}
# Discord Webhook
discord_webhook = os.environ.get('DISCORD_WEBHOOK_URL')

# Parse Arguments
parser = argparse.ArgumentParser()
parser.add_argument('--symbol', type=str, help='see CoinAPI symbols, e.g. BITSTAMP_SPOT_BTC_USD')
parser.add_argument('--startDate', type=str, help='ISO8601 Timestamp (e.g. 2018-01-01T00:00:00')
parser.add_argument('--endDate', type=str, help='ISO8601 Timestamp (e.g. 2018-01-01T00:00:00)')
parser.add_argument('--resolution', type=str, help='see CoinAPI periods (e.g. 1MIN, only 1MIN is supported as of now)')
args = parser.parse_args()

# Setup Logger
logfile="logs/coinapi/{}.{}.{}.{}".format(args.startDate, args.endDate, args.symbol, args.resolution)
logging.basicConfig(filename=logfile, 
format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

symbol = args.symbol
startDate = args.startDate
endDate = args.endDate
resolution = args.resolution

# Convert to UTC time
startDateObj = datetime.datetime.strptime(args.startDate, '%Y-%m-%dT%H:%M:%S')
endDateObj = datetime.datetime.strptime(args.endDate, '%Y-%m-%dT%H:%M:%S')

if args.resolution == '1MIN':
    deltaTimeObj = datetime.timedelta(minutes=100)
else:
    logging.error("Unsupported resolution.")
    sys.exit(1)

header = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'trades_count']
filename = "data/coinapi/{}.{}.{}.{}.csv".format(args.startDate, args.endDate, args.symbol, args.resolution)
logging.info("Saving OHLCV data to: %s", filename)

with open(filename, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(header)

    #with open("../../output/test", "r") as read_file:
    #    data = json.load(read_file)
    #    print(len(data))
    #    for candle in data:
    #        convert_candle_to_csv_entry(candle)

    while startDateObj <= endDateObj:
        endDateObjTemp = startDateObj + deltaTimeObj
        url = "https://rest.coinapi.io/v1/ohlcv/{}/history?period_id={}&time_start={}&time_end={}".format(
            symbol,
            resolution,
            startDateObj.strftime('%Y-%m-%dT%H:%M:%S'),
            endDateObjTemp.strftime('%Y-%m-%dT%H:%M:%S')
        )
        logging.info("Fetching OHLCV Data: " + url)
        response = requests.get(url, headers=req_headers)
        logging.info("Response Headers: {}".format(response.headers))
        if len(response.json()) < 100:
            logging.warn("Less than 100 candles returned for time interval beginning at {}".format(startDateObj))
        for candle in response.json():
            writer.writerow(convert_candle_to_csv_entry(candle))

        time.sleep(1)
        startDateObj += deltaTimeObj

if discord_webhook :
    r = requests.post(discord_webhook,
    json={"content": "Scraped data to: {}".format(filename)})