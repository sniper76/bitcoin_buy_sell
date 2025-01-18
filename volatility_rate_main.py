# main.py
import time
import json
import python_bithumb
from datetime import datetime
from bitthumb.order_chance import get_balance_and_locked_and_fee
from bitthumb.buy import buy_btc
from bitthumb.sell import sell_btc
from bitthumb.sell_market_price import sell_market_btc
from bitthumb.buy_market_price import buy_market_btc
from price_util import cutting_unit_price
from bitthumb.bar_chart_data import BarChartData
from upbit.log_appendar import PrintLogger
from bitthumb.get_buy_signal import BuySignalData

def main():
    try:
        """
        배치 작업: 0시 0분 0초부터 6시 0분 0초까지 실행
        volatility 변동폭 high - low
        volatility_rate 변동비율
        바로 직전 1분봉의 변동비율이 0.05 보다 클때 종가로 매수한다.
        """
        obj = PrintLogger("BitTb")
        barChart = BarChartData()
        buySingal = BuySignalData()
        obj.info_method("매수 배치 작업 시작")
        start_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = start_time.replace(hour=6)

        #while datetime.now() < end_time:
        while True:
            # 잔액과 수수료 가져오기
            response = get_balance_and_locked_and_fee()
            data = json.loads(response)  # JSON 문자열을 딕셔너리로 변환

            yield_rate = 0.001   # 수익율 (0.1%)

            bar_char_data = barChart.get_price_minute3()
            buy_signal_data = buySingal.get_price_difference_volatility_calculate_with_fee_sell_rate(bar_char_data, yield_rate)

            if data["bid_balance"] > 9990 and data["bid_locked"] == 0 and data["ask_balance"] == 0 and data["ask_locked"] == 0 and buy_signal_data["buy_signal"]:
                obj.info_method("매수 프로세스 시작!!")

                # 매수가 계산: 잔액 - (잔액 * 수수료 + 0.02)
                balance = data["bid_balance"]
                fee_rate = data["bid_fee_rate"]
                total_balance = balance - (balance * (fee_rate + 0.02))

                buy_price = float(buy_signal_data["buy_price"])
                sell_price = float(buy_signal_data["sell_price"])
                buy_price = cutting_unit_price(1000, buy_price)
                sell_price = cutting_unit_price(1000, sell_price)

                # 수량 계산
                quantity = round(total_balance / buy_price, 7)
                buy_result = buy_btc(buy_price, quantity)
                obj.info_method(f"buy_price: {buy_price}, quantity: {quantity}, sell_price: {sell_price}")

                if buy_result["is_completed"]:
                    sell_result = sell_btc(sell_price, quantity)

            # 90초 대기
            time.sleep(90)

        obj.info_method("매수 배치 작업 종료")
    except KeyboardInterrupt:
        print("프로그램이 종료되었습니다.")

if __name__ == "__main__":
    main()
