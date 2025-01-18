import time
import json
from upbit.log_appendar import PrintLogger
from price_util import cutting_unit_price
from datetime import datetime
from upbit.order_chance import get_balance_and_locked_and_fee
from upbit.buy import buy_btc
from upbit.sell import sell_btc
from upbit.bar_chart_data import BarChartData
from upbit.buy_signal import BuySignalData

def main():
    loggerObj = PrintLogger("Upbit")
    try:
        """
        배치 작업: 0시 0분 0초부터 6시 0분 0초까지 실행
        volatility 변동폭 high - low
        volatility_rate 변동비율
        바로 직전 1분봉의 변동비율이 0.05 보다 클때 종가로 매수한다.

        """
        barChart = BarChartData()
        buySingal = BuySignalData()
        loggerObj.info_method("매수 배치 작업 시작")
        
        while True:
            # 잔액과 수수료 가져오기
            response = get_balance_and_locked_and_fee()
            data = json.loads(response)  # JSON 문자열을 딕셔너리로 변환
            #loggerObj.debug_method(f"balance: {data}")

            yield_rate = 0.0005   # 수익율 (0.05%)

            bar_char_data = barChart.get_price_minute3()
            buy_signal_data = buySingal.get_price_difference_volatility_calculate_with_fee(bar_char_data, yield_rate)

            if data["bid_balance"] > 9990 and data["bid_locked"] == 0 and data["ask_balance"] == 0 and data["ask_locked"] == 0 and buy_signal_data["buy_signal"]:
                loggerObj.info_method("매수 프로세스 시작!!")

                # 0.01 is 1%
                # 매수가 계산: 잔액 - (잔액 * 수수료 *)
                balance = data["bid_balance"]
                fee_rate = data["bid_fee_rate"]
                total_balance = balance - (balance * fee_rate * 2)

                buy_price = float(buy_signal_data["buy_price"])
                sell_price = float(buy_signal_data["sell_price"])
                buy_price = cutting_unit_price(1000, buy_price)
                sell_price = cutting_unit_price(1000, sell_price)

                # 수량 계산
                quantity = round(total_balance / buy_price, 7)
                buy_result = buy_btc(buy_price, quantity)
                loggerObj.info_method(f"balance: {balance}, fee_rate: {fee_rate}, total_balance: {total_balance}")
                loggerObj.info_method(f"buy_price: {buy_price}, quantity: {quantity}, sell_price: {sell_price}")

                if buy_result["is_completed"]:
                    sell_result = sell_btc(sell_price, quantity)

            # 90초 대기
            time.sleep(90)

        loggerObj.info_method("매수 배치 작업 종료")
    except KeyboardInterrupt:
        loggerObj.debug_method("프로그램이 종료되었습니다.")

if __name__ == "__main__":
    main()
