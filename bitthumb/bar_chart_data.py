import python_bithumb
import logging
from bitthumb.log_appendar import PrintLogger

class BarChartData:
    DF_LENGTH = 10
    
    def __init__(self):
        # Use PrintLogger for logging
        self.example_logger = PrintLogger("BitTb")

    def get_price_minute3(self):
        # 1. 빗썸 차트 데이터 가져오기 (3분봉)
        return python_bithumb.get_ohlcv("KRW-BTC", interval="minute3", count=10)

    def get_price_minute1(self):
        # 1. 빗썸 차트 데이터 가져오기 (1분봉)
        return python_bithumb.get_ohlcv("KRW-BTC", interval="minute1", count=10)

    def get_price_difference_volatility_calculate_with_fee_by_minute3(self):
        """
        고가와 저가의 차이로 변동율을 계산하다.volatility
        현재 row 와 바로 이전 row 의 종가로 차이를 계산한다.compare_prev_row_close_price
        """
        # 1. 빗썸 차트 데이터 가져오기 (1분봉)
        df = python_bithumb.get_ohlcv("KRW-BTC", interval="minute3", count=10)

        # 2: 이전 열과 종가 차이
        df["compare_prev_row_close_price"] = df["close"].diff()
        
        # 변동폭 계산
        #df["volatility"] = df["high"] - df["low"]
        df["volatility"] = df["close"] - df["open"]

        # 변동 비율 계산
        df["volatility_rate"] = ((df["volatility"] / df["low"]) * 100).round(2)

        # 변동 비율 마지막에서 두번째 열
        second_to_last_row_volatility_rate = float(df["volatility_rate"].iloc[self.DF_LENGTH - 2])
        
        second_to_last_row_close_price = float(df["close"].iloc[self.DF_LENGTH - 2])
        last_row_close_price = float(df["close"].iloc[self.DF_LENGTH - 1])

        second_to_last_row_diff_price = float(df["compare_prev_row_close_price"].iloc[self.DF_LENGTH - 2])
        last_row_diff_price = float(df["compare_prev_row_close_price"].iloc[self.DF_LENGTH - 1])
        
        fee_rate = 0.0004   # 수수료율 (0.04%)

        # 수수료 계산 (매도 수수료와 매수 수수료를 합산)
        sell_fee = last_row_close_price * fee_rate
        buy_fee = second_to_last_row_close_price * fee_rate
        total_fee = round(sell_fee + buy_fee)

        self.example_logger.debug_method(df[["open", "high", "close", "volatility", "volatility_rate", "compare_prev_row_close_price"]])
        # 50100 - 50000 = 100 fee 20
        self.example_logger.info_method(f"second_to_last_row_volatility_rate: {second_to_last_row_volatility_rate}, total_fee: {total_fee}")
        self.example_logger.info_method(f"second_to_last_row_close_price: {second_to_last_row_close_price}, last_row_close_price: {last_row_close_price}")
        self.example_logger.info_method(f"second_to_last_row_diff_price: {second_to_last_row_diff_price}, last_row_diff_price: {last_row_diff_price}")
        """
        바로 이전 변동율이 0.08 보다 크고
        현재 row 보다 바로 이전 row 의 종가가 작고
        현재 row 와 바로 이전 row 가 양수 이고
        차액이 매수 + 매도 수수료 보다 큰 경우
        """
        if (
            second_to_last_row_volatility_rate > 0.08 
            and second_to_last_row_close_price < last_row_close_price 
            and second_to_last_row_diff_price > 0 
            and last_row_diff_price > 0 
            and last_row_diff_price > total_fee
        ):
            data = {
                "buy_signal": True,
                "buy_price": second_to_last_row_close_price,
                "sell_price": last_row_close_price
            }
            return data

        data = {
            "buy_signal": False
        }
        return data

    def get_price_difference_volatility_calculate_with_fee_by_minute1(self):
        """
        고가와 저가의 차이로 변동율을 계산하다.volatility
        현재 row 와 바로 이전 row 의 종가로 차이를 계산한다.compare_prev_row_close_price
        """
        # 1. 빗썸 차트 데이터 가져오기 (1분봉)
        df = python_bithumb.get_ohlcv("KRW-BTC", interval="minute1", count=10)

        # 2: 이전 열과 종가 차이
        df["compare_prev_row_close_price"] = df["close"].diff()
        
        # 변동폭 계산
        #df["volatility"] = df["high"] - df["low"]
        df["volatility"] = df["close"] - df["open"]

        # 변동 비율 계산
        df["volatility_rate"] = ((df["volatility"] / df["low"]) * 100).round(2)

        # 변동 비율 마지막에서 두번째 열
        second_to_last_row_volatility_rate = float(df["volatility_rate"].iloc[self.DF_LENGTH - 2])
        
        second_to_last_row_close_price = float(df["close"].iloc[self.DF_LENGTH - 2])
        last_row_close_price = float(df["close"].iloc[self.DF_LENGTH - 1])

        second_to_last_row_diff_price = float(df["compare_prev_row_close_price"].iloc[self.DF_LENGTH - 2])
        last_row_diff_price = float(df["compare_prev_row_close_price"].iloc[self.DF_LENGTH - 1])
        
        fee_rate = 0.0004   # 수수료율 (0.04%)

        # 수수료 계산 (매도 수수료와 매수 수수료를 합산)
        sell_fee = last_row_close_price * fee_rate
        buy_fee = second_to_last_row_close_price * fee_rate
        total_fee = round(sell_fee + buy_fee)

        self.example_logger.debug_method(df[["open", "high", "close", "volatility", "volatility_rate", "compare_prev_row_close_price"]])
        # 50100 - 50000 = 100 fee 20
        self.example_logger.info_method(f"second_to_last_row_volatility_rate: {second_to_last_row_volatility_rate}, total_fee: {total_fee}")
        self.example_logger.info_method(f"second_to_last_row_close_price: {second_to_last_row_close_price}, last_row_close_price: {last_row_close_price}")
        self.example_logger.info_method(f"second_to_last_row_diff_price: {second_to_last_row_diff_price}, last_row_diff_price: {last_row_diff_price}")
        """
        바로 이전 변동율이 0.08 보다 크고
        현재 row 보다 바로 이전 row 의 종가가 작고
        현재 row 와 바로 이전 row 가 양수 이고
        차액이 매수 + 매도 수수료 보다 큰 경우
        """
        if (
            second_to_last_row_volatility_rate > 0.08 
            and second_to_last_row_close_price < last_row_close_price 
            and second_to_last_row_diff_price > 0 
            and last_row_diff_price > 0 
            and last_row_diff_price > total_fee
        ):
            data = {
                "buy_signal": True,
                "buy_price": second_to_last_row_close_price,
                "sell_price": last_row_close_price
            }
            return data

        data = {
            "buy_signal": False
        }
        return data

# Example usage
if __name__ == "__main__":
    bar = BarChartData()
    bar.get_price_difference_volatility_calculate_with_fee_by_minute3()