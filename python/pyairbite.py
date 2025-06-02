import airbyte as ab

# Retrieve the source
source = ab.get_source(
   "source-yahoo-finance-price",
   install_if_missing=True,
   config={
       "tickers": "AAPL, MSFT, GOOGL",
       "interval": "1d",
       "range": "1y"
   }
)

source.check()

source.select_all_streams()
read_result: ab.ReadResult = source.read()

products_df = read_result["price"].to_pandas()
print(products_df)