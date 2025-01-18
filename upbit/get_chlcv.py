import os
import pyupbit


upbit = pyupbit.Upbit(os.getenv("UPBIT_ACCESS_KEY"), os.getenv("UPBIT_SECRET_KEY"))

df = pyupbit.get_ohlcv("KRW-BTC", interval="minute3", count=10)
print(df)

orderbook = pyupbit.get_orderbook(ticker="KRW-BTC")

btc = upbit.get_balance("KRW")

result = upbit.buy_market_order("KRW-BTC", btc*0.9995)

result = upbit.sell_market_order("KRW-BTC", btc)