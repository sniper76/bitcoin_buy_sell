# main.py
import time
import json
import python_bithumb
from datetime import datetime
from order_chance import get_balance_and_locked_and_fee
from buy import buy_btc
from sell import sell_btc
from sell_market_price import sell_market_btc
from buy_market_price import buy_market_btc
from price_util import cutting_unit_price
from bar_chart_data import BarChartData
from log_appendar import PrintLogger

def main():
    try:
        """
        배치 작업: 0시 0분 0초부터 6시 0분 0초까지 실행
        volatility 변동폭 high - low
        volatility_rate 변동비율
        바로 직전 1분봉의 변동비율이 0.05 보다 클때 종가로 매수한다.

        """
        obj = PrintLogger()
        barChart = BarChartData()
        obj.info_method("매수 배치 작업 시작")
        start_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = start_time.replace(hour=6)

        #while datetime.now() < end_time:
        while True:
            # 잔액과 수수료 가져오기
            response = get_balance_and_locked_and_fee()
            data = json.loads(response)  # JSON 문자열을 딕셔너리로 변환

            bar_char_data = barChart.get_price_difference_volatility_calculate_with_fee_by_minute1()

            if data["bid_balance"] > 9990 and data["bid_locked"] == 0 and data["ask_balance"] == 0 and data["ask_locked"] == 0 and bar_char_data["buy_signal"]:
                obj.info_method("매수 프로세스 시작!!")

                # 매수가 계산: 잔액 - (수수료 * 2)
                balance = data["bid_balance"]
                fee_rate = data["bid_fee_rate"]
                total_balance = balance - (balance * fee_rate * 2)

                buy_price = float(bar_char_data["buy_price"])
                sell_price = float(bar_char_data["sell_price"])
                buy_price = cutting_unit_price(1000, buy_price)

                # 수량 계산
                quantity = round(total_balance / buy_price, 7)
                buy_result = buy_btc(buy_price, quantity)
                obj.info_method(f"buy_price: {buy_price}, quantity: {quantity}, sell_price: {sell_price}")

                if buy_result["is_completed"]:
                    sell_result = sell_btc(sell_price, quantity)

            # 60초 대기
            time.sleep(60)

        obj.info_method("매수 배치 작업 종료")
    except KeyboardInterrupt:
        print("프로그램이 종료되었습니다.")

if __name__ == "__main__":
    main()
