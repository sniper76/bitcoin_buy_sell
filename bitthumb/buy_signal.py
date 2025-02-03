import python_bithumb
import logging
import pandas as pd
from bitthumb.log_appendar import PrintLogger

class BuySignalData:
    DF_LENGTH = 10
    
    def __init__(self):
        # Use PrintLogger for logging
        self.example_logger = PrintLogger("BitTb")

    def get_price_preview_row_rises_jumping(self, data):
        """
        이전 종가 보다 현재 시가가 점프하면 매수하고 0.2% 더해서 매도
        """
        data["volatility"] = data["close"] - data["open"]

        second_to_last_close_price = float(data["close"].iloc[self.DF_LENGTH - 2])
        last_row_open_price = float(data["open"].iloc[self.DF_LENGTH - 1])
        last_row_close_price = float(data["close"].iloc[self.DF_LENGTH - 1])
        open_close_difference_price = last_row_open_price - second_to_last_close_price
        last_difference_price = last_row_close_price - last_row_open_price

        second_to_last_row_volatility_price = float(data["volatility"].iloc[self.DF_LENGTH - 2])
        last_row_volatility_price = float(data["volatility"].iloc[self.DF_LENGTH - 1])
        
        last_row_volume = float(data["volume"].iloc[self.DF_LENGTH - 1])

        buy_price = float(data["open"].iloc[self.DF_LENGTH - 1])
        sell_price = buy_price + round(buy_price * 0.002)

        #self.example_logger.debug_method(data[["open", "close", "volatility", "volume"]])
        self.example_logger.info_method(f"last_row_close_price: {last_row_close_price}, last_difference_price: {last_difference_price}, open_close_difference_price: {open_close_difference_price}, last_row_volume: {last_row_volume}")
        if (
            second_to_last_close_price < last_row_open_price
            and second_to_last_row_volatility_price > 10000
            and last_row_volatility_price > 10000
            and open_close_difference_price > 20000
            and last_difference_price > 10000
            and last_row_volume > 0.7
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

    def get_price_five_consecutive_risesed(self, data):
        """
        분봉 5연속 상승시 현재 봉의 시가open 으로 매수하고 0.2% 더해서 매도
        """
        data["volatility"] = data["close"] - data["open"]
        
        fifth_to_last_row_volatility_price = float(data["volatility"].iloc[self.DF_LENGTH - 5])
        fourth_to_last_row_volatility_price = float(data["volatility"].iloc[self.DF_LENGTH - 4])
        third_to_last_row_volatility_price = float(data["volatility"].iloc[self.DF_LENGTH - 3])
        second_to_last_row_volatility_price = float(data["volatility"].iloc[self.DF_LENGTH - 2])
        last_row_volatility_price = float(data["volatility"].iloc[self.DF_LENGTH - 1])

        buy_price = float(data["open"].iloc[self.DF_LENGTH - 1])
        sell_price = buy_price + round(buy_price * 0.002)

        self.example_logger.debug_method(data[["open", "low", "high", "close", "volatility"]])
        self.example_logger.info_method(f"rises buy_price: {buy_price}, sell_price: {sell_price}")
        if (
            third_to_last_row_volatility_price > 10000
            and second_to_last_row_volatility_price > 10000
            and last_row_volatility_price > 10000
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

    def get_price_day_bar_body_size(self, data):
        """
        현재봉과 바로직전봉이 양봉 시가 < 종가
        현재봉 크기가 바로직전봉 크기 보다 커지는 순간 매수
        0.2% 더해서 매도
        """
        # 봉의 크기 계산 (절대값 사용)
        data["body_size"] = abs(data["close"] - data["open"])

        # 이전 봉 크기와 비교
        data["prev_body_size"] = data["body_size"].shift(1)
        data["is_double_size"] = data["body_size"] >= 2 * data["prev_body_size"]

        data["volatility"] = data["close"] - data["open"]
        
        second_to_last_row_volatility_price = float(data["volatility"].iloc[self.DF_LENGTH - 2])
        last_row_volatility_price = float(data["volatility"].iloc[self.DF_LENGTH - 1])
        last_row_is_double_size = float(data["is_double_size"].iloc[self.DF_LENGTH - 1])

        buy_price = float(data["close"].iloc[self.DF_LENGTH - 1])
        sell_price = buy_price + round(buy_price * 0.002)

        self.example_logger.debug_method(data[["open", "close", "body_size", "is_double_size"]])
        self.example_logger.info_method(f"buy_price: {buy_price}, sell_price: {sell_price}")
        if (
            second_to_last_row_volatility_price > 0
            and last_row_volatility_price > 0
            and last_row_is_double_size
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
    
    def get_price_five_consecutive_declinesed(self, data):
        """
        분봉 5연속 하락시 현재 봉의 시가open 으로 매수하고 0.2% 더해서 매도
        """
        data["volatility"] = data["close"] - data["open"]
        
        fifth_to_last_row_volatility_price = float(data["volatility"].iloc[self.DF_LENGTH - 5])
        fourth_to_last_row_volatility_price = float(data["volatility"].iloc[self.DF_LENGTH - 4])
        third_to_last_row_volatility_price = float(data["volatility"].iloc[self.DF_LENGTH - 3])
        second_to_last_row_volatility_price = float(data["volatility"].iloc[self.DF_LENGTH - 2])
        last_row_volatility_price = float(data["volatility"].iloc[self.DF_LENGTH - 1])

        buy_price = float(data["open"].iloc[self.DF_LENGTH - 1])
        sell_price = buy_price + round(buy_price * 0.002)

        self.example_logger.debug_method(data[["open", "low", "high", "close", "volatility"]])
        self.example_logger.info_method(f"declines buy_price: {buy_price}, sell_price: {sell_price}")
        if (
            fifth_to_last_row_volatility_price < -10000
            and fourth_to_last_row_volatility_price < -10000
            and third_to_last_row_volatility_price < -10000
            and second_to_last_row_volatility_price < -10000
            and last_row_volatility_price < -10000
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
        현재 row 와 바로 이전 row 의 종가로 차이를 계산한다.compare_prev_row_close_price
        """
        # 2: 이전 열과 종가 차이
        data["compare_prev_row_close_price"] = data["close"].diff()
        
        # 변동폭 계산
        #df["volatility"] = df["high"] - df["low"]
        data["volatility"] = data["close"] - data["open"]

        # 변동 비율 계산
        data["volatility_rate"] = ((data["volatility"] / data["low"]) * 100).round(2)

        # 변동 비율 마지막에서 두번째 열
        second_to_last_row_volatility_rate = float(data["volatility_rate"].iloc[self.DF_LENGTH - 2])
        
        second_to_last_row_close_price = float(data["close"].iloc[self.DF_LENGTH - 2])
        last_row_close_price = float(data["close"].iloc[self.DF_LENGTH - 1])

        second_to_last_row_diff_price = float(data["compare_prev_row_close_price"].iloc[self.DF_LENGTH - 2])
        last_row_diff_price = float(data["compare_prev_row_close_price"].iloc[self.DF_LENGTH - 1])
        
        # 수익율과 수수료율 동일하게 (0.04%)

        # 수수료 계산 (매도 수수료와 매수 수수료를 합산)
        sell_fee = last_row_close_price * yield_rate
        buy_fee = second_to_last_row_close_price * yield_rate
        total_fee = round(sell_fee + buy_fee)

        self.example_logger.debug_method(data[["open", "high", "close", "volatility", "volatility_rate", "compare_prev_row_close_price"]])
        self.example_logger.info_method(f"second_to_last_row_volatility_rate: {second_to_last_row_volatility_rate}, total_fee: {total_fee}, yield_fee: {yield_rate}")
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

    def get_price_difference_volatility_calculate_with_fee_sell_rate(self, data, yield_rate=float):
        """
        고가와 저가의 차이로 변동율을 계산하다.volatility
        현재 row 와 바로 이전 row 의 종가로 차이를 계산한다.compare_prev_row_close_price
        """
        # 2: 이전 열과 종가 차이
        data["compare_prev_row_close_price"] = data["close"].diff()
        
        # 변동폭 계산
        #df["volatility"] = df["high"] - df["low"]
        data["volatility"] = data["close"] - data["open"]

        # 변동 비율 계산
        data["volatility_rate"] = ((data["volatility"] / data["low"]) * 100).round(2)

        # 변동 비율 마지막에서 두번째 열
        second_to_last_row_volatility_rate = float(data["volatility_rate"].iloc[self.DF_LENGTH - 2])
        
        second_to_last_row_close_price = float(data["close"].iloc[self.DF_LENGTH - 2])
        last_row_close_price = float(data["close"].iloc[self.DF_LENGTH - 1])

        second_to_last_row_diff_price = float(data["compare_prev_row_close_price"].iloc[self.DF_LENGTH - 2])
        last_row_diff_price = float(data["compare_prev_row_close_price"].iloc[self.DF_LENGTH - 1])
        
        fee_rate = 0.0004   # 수수료율 (0.04%)

        # 수수료 계산 (매도 수수료와 매수 수수료를 합산)
        sell_fee = last_row_close_price * fee_rate
        buy_fee = second_to_last_row_close_price * fee_rate
        total_fee = round(sell_fee + buy_fee)

        yield_fee = round(last_row_close_price * yield_rate)
        sell_price = round(last_row_close_price + yield_fee)

        self.example_logger.debug_method(data[["open", "high", "close", "volatility", "volatility_rate", "compare_prev_row_close_price"]])
        self.example_logger.info_method(f"second_to_last_row_volatility_rate: {second_to_last_row_volatility_rate}, total_fee: {total_fee}, yield_fee: {yield_fee}")
        self.example_logger.info_method(f"second_to_last_row_close_price: {second_to_last_row_close_price}, sell_price: {sell_price}")
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
            result = {
                "buy_signal": True,
                "buy_price": second_to_last_row_close_price,
                "sell_price": sell_price
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