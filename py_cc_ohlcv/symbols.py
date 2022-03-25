from py_cc_ohlcv import exchanges, instruments

symbols_by_exchange = {
    exchanges.COINBASE_PRO: {
        instruments.BTC_USD : "BTC-USD",
        instruments.ETH_USD : "ETH-USD",
        instruments.LTC_USD : "LTC-USD"
    },
    exchanges.FTX: {
        instruments.BTC_USD : "BTC/USD",
        instruments.ETH_USD : "ETH/USD",
        instruments.LTC_USD : "LTC/USD"
    },
    exchanges.GEMINI: {

    }
}