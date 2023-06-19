from pykrx import stock

data = stock.get_market_ohlcv_by_date("20200615","20230615","005930")

print(data)