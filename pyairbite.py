import airbyte as ab

source = ab.get_source(
   source-yahoo-finance-price,
   install_if_missing=True,
   config={
       "tickers": "AAPL, MSFT, GOOGL",
       "interval": "1d",
       "range": "1y"
   }
)