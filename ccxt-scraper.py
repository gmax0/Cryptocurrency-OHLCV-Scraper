import ccxt
import inspect
import argparse
import datetime
from datetime import timezone
import csv
import time
import logging
import os
import requests
import sys

def millisecondsToSeconds(candle_arr) :
    candle_arr[0] = candle_arr[0] / 1000;
    if candle_arr[0].is_integer() == False:
        logging.warn("Non-integer timestamp detected: %s", candle_arr[0])
    candle_arr[0] = int(candle_arr[0])

if not os.path.exists('data/ccxt'):
    os.makedirs('data/ccxt')

if not os.path.exists('logs/ccxt'):
    os.makedirs('logs/ccxt')

# Discord Webhook
discord_webhook = os.environ.get('DISCORD_WEBHOOK_URL')

# Parse Arguments
parser = argparse.ArgumentParser()
parser.add_argument('--exchange', type=str, help='see ccxt exchange_ids, e.g. coinbasepro')
parser.add_argument('--pricepair', type=str, help='see ccxt symbols, e.g. ETH/USD')
parser.add_argument('--startDate', type=str, help='YYYY-MM-DD')
parser.add_argument('--endDate', type=str, help='YYYY-MM-DD')
parser.add_argument('--resolution', type=str, help='1m, 1d, 1M')
args = parser.parse_args()

# Setup Logger
logfile="logs/ccxt/{}.{}.{}.{}.{}".format(args.startDate, args.endDate, args.exchange, args.pricepair.replace("/", "-"), args.resolution)
logging.basicConfig(filename=logfile, 
format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

try: 
    # Convert to epoch milliseconds
    startDateObj = datetime.datetime.strptime(args.startDate, '%Y-%m-%d').replace(tzinfo=datetime.timezone.utc)
    endDateObj = datetime.datetime.strptime(args.endDate, '%Y-%m-%d').replace(tzinfo=datetime.timezone.utc)
    currStartDateObj = startDateObj
    startDateObjMS = (int)(startDateObj.timestamp() * 1000)
    endDateObjMS = (int)(startDateObj.timestamp() * 1000)

    logging.info('Start Date in Milleseconds since Epoch: %d', startDateObjMS)
    logging.info('End Date in Milleseconds since Epoch: %d', endDateObjMS)

    # Setup Exchange
    exchange_id = args.exchange
    exchange_class = getattr(ccxt, exchange_id)
    exchange = exchange_class({
        #'apiKey': '',
        #'secret': '',
        #'passphrase': '',
        'timeout': 30000,
        'enableRateLimit': True,
    })

    logging.info('Initializing exchange class for %s', args.exchange)
    exchange.load_markets()

    # Save OHLCV data to CSV
    header = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    filename = "data/ccxt/{}.{}.{}.{}.{}.csv".format(args.startDate, args.endDate, args.exchange, args.pricepair.replace("/", "-"), args.resolution)
    logging.info("Saving OHLCV data to: %s", filename)

    if args.resolution == '1m':
        deltaTimeObj = datetime.timedelta(minutes=300)
    elif args.resolution == '1d':
        deltaTimeObj = datetime.timedelta(days=300)
    else:
        deltaTimeObj = datetime.timedelta(days=9000)

    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        #TODO: perform dynamic date calculations
        while currStartDateObj <= endDateObj:
            startMS = (int)(currStartDateObj.timestamp() * 1000)
            endMS = (int)((currStartDateObj + deltaTimeObj).timestamp() * 1000)
            logging.info("Fetching OHLCV data for - start: %s (%d) end: %s (%d)", 
                currStartDateObj.strftime('%Y-%m-%dT%H:%M:%SZ') ,startMS,
                (currStartDateObj + deltaTimeObj).strftime('%Y-%m-%dT%H:%M:%SZ'), endMS)
            ohlcv_resp = exchange.fetch_ohlcv(args.pricepair, '1m', startMS, 300)
            if (len(ohlcv_resp) < 300):
                logging.warn("OHCLV data for %d, was less than 300: %d", startMS, len(ohlcv_resp))
            
        
            #for i in ohlcv_resp:
            #    millisecondsToSeconds(i)

            writer.writerows(ohlcv_resp)
            time.sleep(exchange.rateLimit / 1000)
            currStartDateObj += datetime.timedelta(minutes=300)

    logging.info("Job Completed.")
    if discord_webhook :
        r = requests.post(discord_webhook,
        json={"content": "Scraped data to: {}".format(filename)})
except Exception as e:
    logging.error(e)
    if discord_webhook : 
        r = requests.post(discord_webhook,
        json={"content": "Exception caught while processing job. See logs."})
    sys.exit(1)