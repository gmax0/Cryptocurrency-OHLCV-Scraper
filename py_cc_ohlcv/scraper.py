from py_cc_ohlcv import exchanges, exchange_metadata, exchange_functions
import datetime
import logging
import requests
import time

import pandas as pd

logger = logging.getLogger()

class Scraper:
    exchange = None
    metadata = None

    instrument = None
    symbol = None
    resolution = None
    resolution_val = None

    url = None
    proxies = None
    window_start = None
    window_end = None

    def __init__(self, exchange, instrument, resolution, start_time: datetime, end_time: datetime):
        self.exchange = exchange
        self.instrument = instrument

        self.metadata = exchange_metadata.exchange_metadata[self.exchange]
        self.exchange_functions = exchange_functions.exchange_functions
        self.symbol = exchange_metadata.exchange_metadata[self.exchange]['instrument_mapping'](instrument)
        self.url = exchange_metadata.exchange_metadata[self.exchange]['url']

        self.resolution = resolution
        self.resolution_val = exchange_metadata.exchange_metadata[self.exchange]['resolutions'][self.resolution]

        self.window_start = start_time
        self.window_end = end_time

    def set_proxies(self, proxies: dict):
        self.proxies = proxies

    def run(self):
        logger.info("""Executing job with parameters: \n 
        [EXCHANGE] {}, [INSTR] {}, [RESOLUTION] {} \n
        [START] {} ({})\n
        [END] {} ({})
        """.format(self.exchange, self.symbol, self.resolution,
        self.window_start, self.window_start.timestamp() * 1000,
        self.window_end, self.window_end.timestamp() * 1000))

        # Set time delta based on maximum candles per request and desired resolution
        delta_t = None 
        if self.resolution == '1m':
            delta_t = datetime.timedelta(minutes=self.metadata['max_candles_per_req'])
        else:
            logger.error("Resolution not supported!")
            return
        
        start = self.window_start
        end = self.window_end
        timestamp_format = self.metadata['timestamp_format']
        parsed_candles = []

        # Exception for coinbase
        if self.exchange == exchanges.COINBASE_PRO:
            start = start - delta_t / self.metadata['max_candles_per_req']

        while start < self.window_end:
            end = start + delta_t
            if (end > self.window_end):
                end = self.window_end

            url = self.url.format(
                self.symbol,
                self.resolution_val,
                start.strftime(timestamp_format) if type(timestamp_format) is str else int(start.timestamp()) * timestamp_format,
                end.strftime(timestamp_format) if type(timestamp_format) is str else int(end.timestamp()) * timestamp_format
            )

            logger.debug(url)
            response = requests.get(url=url, proxies=self.proxies)
            logger.debug(response.headers)

            candles_response = response.json()
            for key in self.metadata['response_keys']:
                candles_response = candles_response[key]

            logger.debug("Received {} candles".format(len(candles_response))))

            for candle in candles_response:
                parsed_candles.append(self.exchange_functions[self.exchange +'_candle_mapping'](candle))

            time.sleep(0.25) # TODO: Use an actual rate limiter
            start = end
        
        df = pd.DataFrame(parsed_candles)
        df = df.set_index('open_timestamp')
        df = df.sort_index(ascending=True)
        df = df[~df.index.duplicated(keep='first')] # Drop duplicate timestamps
        df = df.truncate(after=int(self.window_end.timestamp() * 1000))

        return df