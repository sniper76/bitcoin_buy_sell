import python_bithumb
import logging
import pandas as pd
from upbit.log_appendar import PrintLogger

class BuySignalData:
    DF_LENGTH = 10

    def __init__(self):
        self.loggerObj = PrintLogger("Upbit")

    def get_price_preview_row_rises_jumping(self, data):
        """
        이전 종가 보다 현재 시가가 점프하면 매수
        """
        data["volatility"] = data["close"] - data["open"]

        second_to_last_row_volatility_price = float(data["volatility"].iloc[self.DF_LENGTH - 2])
        last_row_volatility_price = float(data["volatility"].iloc[self.DF_LENGTH - 1])
        
        second_to_last_close_price = float(data["close"].iloc[self.DF_LENGTH - 2])
        last_row_open_price = float(data["open"].iloc[self.DF_LENGTH - 1])

        buy_price = float(data["open"].iloc[self.DF_LENGTH - 1])
        sell_price = buy_price + round(buy_price * 0.002)

        self.loggerObj.debug_method(data[["open", "high", "close", "volatility"]])
        self.loggerObj.info_method(f"buy_price: {buy_price}, sell_price: {sell_price}")
        if (
            second_to_last_close_price < last_row_open_price
            and second_to_last_row_volatility_price > 0
            and last_row_volatility_price > 0
        ):
            result = {
                "buy_signal": True,
                "buy_price": buy_price,
                "sell_price": sell_price
            }
            return result

        result = {
            "buy_signal": False
        }
        return result

    def get_price_difference_volatility_calculate_with_fee(self, data, yield_rate=float):
        """
        고가와 저가의 차이로 변동율을 계산하다.volatility
        현재 row 와 바로 이전 row 의 종가로 차이를 계산한다.c_prev_row_close_price
        """
        # 2: 이전 열과 종가 차이
        data["c_prev_row_close_price"] = data["close"].diff()
        
        # 변동폭 계산
        data["volatility"] = data["close"] - data["open"]

        # 변동 비율 계산
        data["volatility_rate"] = ((data["volatility"] / data["low"]) * 100).round(2)

        # 변동 비율 마지막에서 두번째 열
        second_to_last_row_volatility_rate = float(data["volatility_rate"].iloc[self.DF_LENGTH - 2])
        
        second_to_last_row_close_price = float(data["close"].iloc[self.DF_LENGTH - 2])
        last_row_close_price = float(data["close"].iloc[self.DF_LENGTH - 1])

        second_to_last_row_diff_price = float(data["c_prev_row_close_price"].iloc[self.DF_LENGTH - 2])
        last_row_diff_price = float(data["c_prev_row_close_price"].iloc[self.DF_LENGTH - 1])
        
        # 수익율과 수수료율 동일하게 (0.05%)

        # 수수료 계산 (매도 수수료와 매수 수수료를 합산)
        sell_fee = last_row_close_price * yield_rate
        buy_fee = second_to_last_row_close_price * yield_rate
        total_fee = round(sell_fee + buy_fee)
        difference_price = last_row_close_price - second_to_last_row_close_price
        
        #"volume" 거래량
        #self.loggerObj.debug_method(data[["open", "close", "volatility", "volatility_rate"]])
        self.loggerObj.debug_method(f"second_to_last_row_volatility_rate: {second_to_last_row_volatility_rate}")
        self.loggerObj.debug_method(f"second_to_last_row_close_price: {second_to_last_row_close_price}")
        self.loggerObj.debug_method(f"last_row_close_price: {last_row_close_price}, total_fee: {total_fee}")
        self.loggerObj.debug_method(f"second_to_last_row_diff_price: {second_to_last_row_diff_price}, difference_price: {difference_price}")
        self.loggerObj.debug_method(f"last_row_diff_price: {last_row_diff_price}")
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
            result = {
                "buy_signal": True,
                "buy_price": second_to_last_row_close_price,
                "sell_price": last_row_close_price
            }
            return result

        result = {
            "buy_signal": False
        }
        return result

# Example usage
if __name__ == "__main__":
    bar = BuySignalData()
    data = {
        "open": [133388000, 135579000, 135579000, 135579000, 135579000, 135579000, 135579000, 135579000, 135579000, 135579000],
        "low": [132581000, 133534000, 135579000, 135579000, 135579000, 135579000, 135579000, 135579000, 135579000, 135579000],
        "high": [135590000, 136400000, 135579000, 135579000, 135579000, 135579000, 135579000, 135579000, 135579000, 135579000],
        "close": [135564000, 133946000, 135579000, 135579000, 135579000, 135579000, 135579000, 135579000, 135579000, 135579000],
    }
    df = pd.DataFrame(data)
    print(bar.get_price_difference_volatility_calculate_with_fee(df, 0.01))