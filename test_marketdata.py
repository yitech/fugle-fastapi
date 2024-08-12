from fugle_marketdata import RestClient

client = RestClient(api_key="ZjZjOTU1ZjctYjdlZC00OWUzLThiOGQtZjg1MDcwMThhYzBkIDU3NWNjOGQ1LWY3NGUtNDJmOS05MDdjLTRiOTViMjM1ZTIwZg==")
stock = client.stock
print(stock.intraday.quote(symbol="2330"))
print(stock.historical.candles(symbol="2330", resolution="D", limit=10))