# main.py
import time as t
import json
from upbit.order_chance import get_balance_and_locked_and_fee
from upbit.buy import buy_btc
from upbit.sell import sell_btc
from price_util import cutting_unit_price
from upbit.bar_chart_data import BarChartData
from upbit.log_appendar import PrintLogger
from upbit.buy_signal import BuySignalData
from upbit.order_cancel import cancel_order
from upbit.get_order_check import get_order

def main():
    try:
        """
        3분봉 바로 직전 봉의 종가 보다 현재 봉의 시가가 큰 경우
        """
        obj = PrintLogger("Upbit")
        barChart = BarChartData()
        buySingal = BuySignalData()
        obj.info_method("jumping매수 배치 작업 시작")

        while True:
            # 잔액과 수수료 가져오기
            response = get_balance_and_locked_and_fee()
            data = json.loads(response)  # JSON 문자열을 딕셔너리로 변환

            bar_char_data = barChart.get_price_minute3()
            buy_signal_data = buySingal.get_price_preview_row_rises_jumping(bar_char_data)

            if data["bid_balance"] > 9990 and data["bid_locked"] == 0 and data["ask_balance"] == 0 and data["ask_locked"] == 0 and buy_signal_data["buy_signal"]:
                obj.info_method("jumping매수 프로세스 시작!!")

                # 매수가 계산: 잔액 - (수수료 * 2)
                balance = data["bid_balance"]
                fee_rate = data["bid_fee_rate"]
                total_balance = balance - (balance * (fee_rate + 0.0001))

                buy_price = float(buy_signal_data["buy_price"])
                sell_price = float(buy_signal_data["sell_price"])
                buy_price = cutting_unit_price(1000, buy_price)
                sell_price = cutting_unit_price(1000, sell_price)

                # 수량 계산
                quantity = round(total_balance / buy_price, 8)
                buy_result = buy_btc(buy_price, quantity, 10)
                obj.info_method(f"jumping buy_price: {buy_price}, quantity: {quantity}, sell_price: {sell_price}")

                if buy_result["is_completed"]:
                    sell_result = sell_btc(sell_price, quantity, 10)
                    last_sell_order_uuid = sell_result["uuid"]
                    obj.info_method(f"jumping 매도 주문 uuid: {last_sell_order_uuid}")

            # 60초 대기
            t.sleep(60)


        obj.info_method("jumping매수 배치 작업 종료")
    except KeyboardInterrupt:
        print("프로그램이 종료되었습니다.")

if __name__ == "__main__":
    main()
