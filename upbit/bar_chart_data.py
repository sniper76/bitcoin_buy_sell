
import os
import pyupbit
from dotenv import load_dotenv
load_dotenv ()
from upbit.log_appendar import PrintLogger


class BarChartData:

    def __init__(self):
        self.loggerObj = PrintLogger("Upbit")

    def get_price_minute3(self):
        # 1. 업비트 차트 데이터 가져오기 (3분봉)
        df = pyupbit.get_ohlcv("KRW-BTC", interval="minute3", count=10)
        #self.loggerObj.debug_method(f"chart data: {df}")
        return df

    def get_price_day(self):
        # 1. 업비트 차트 데이터 가져오기 (1일봉)
        df = pyupbit.get_ohlcv("KRW-BTC", interval="day", count=10)
        #self.loggerObj.debug_method(df[["open", "close", "volume", "value"]])
        return df

# Example usage
if __name__ == "__main__":
    bar = BarChartData()
    bar.get_price_difference_volatility_calculate_with_fee_by_minute3()