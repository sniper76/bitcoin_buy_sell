# main.py
import time as t
import json
import python_bithumb
from datetime import datetime, time
from bitthumb.order_chance import get_balance_and_locked_and_fee
from bitthumb.buy import buy_btc
from bitthumb.sell import sell_btc
from bitthumb.sell_market_price import sell_market_btc
from bitthumb.buy_market_price import buy_market_btc
from price_util import cutting_unit_price
from bitthumb.bar_chart_data import BarChartData
from bitthumb.log_appendar import PrintLogger
from bitthumb.get_buy_signal import BuySignalData
from bitthumb.order_cancel import cancel_order
from bitthumb.get_order_check import get_order

def main():
    try:
        """
        배치 작업: 0시 0분 0초부터 6시 0분 0초까지 실행
        3분봉 5연속 상승시 매수하고 0.5% 더해서 매도
        """
        obj = PrintLogger("BitTb")
        barChart = BarChartData()
        buySingal = BuySignalData()
        obj.info_method("rises매수 배치 작업 시작")
        last_sell_order_uuid = None

        while True:
            now_time = datetime.now().time()
            obj.info_method(f"rises now_time {now_time}")
            #if time(20, 0, 0) < now_time or now_time < time(6, 0, 0):
            # 잔액과 수수료 가져오기
            response = get_balance_and_locked_and_fee()
            data = json.loads(response)  # JSON 문자열을 딕셔너리로 변환

            bar_char_data = barChart.get_price_minute3()
            buy_signal_data = buySingal.get_price_five_consecutive_risesed(bar_char_data)

            if data["bid_balance"] > 9990 and data["bid_locked"] == 0 and data["ask_balance"] == 0 and data["ask_locked"] == 0 and buy_signal_data["buy_signal"]:
                obj.info_method("rises매수 프로세스 시작!!")

                # 매수가 계산: 잔액 - (수수료 * 2)
                balance = data["bid_balance"]
                fee_rate = data["bid_fee_rate"]
                total_balance = balance - (balance * fee_rate * 2)

                buy_price = float(buy_signal_data["buy_price"])
                sell_price = float(buy_signal_data["sell_price"])
                buy_price = cutting_unit_price(1000, buy_price)
                sell_price = cutting_unit_price(1000, sell_price)

                # 수량 계산
                quantity = round(total_balance / buy_price, 8)
                buy_result = buy_btc(buy_price, quantity, 10)
                obj.info_method(f"rises buy_price: {buy_price}, quantity: {quantity}, sell_price: {sell_price}")

                if buy_result["is_completed"]:
                    sell_result = sell_btc(sell_price, quantity)
                    last_sell_order_uuid = sell_result["uuid"]
                    obj.info_method(f"rises 매도 주문 uuid: {last_sell_order_uuid}")
            """
            else:
                obj.info_method("rises stand by")
                if last_sell_order_uuid is not None:
                    obj.info_method("마지막 주문 취소")
                    final_result = get_order(last_sell_order_uuid)
                    if final_result["remaining_volume"] > 0:
                        obj.info_method(f"rises final_result: {final_result}")
                        cancel_order(last_sell_order_uuid)
                        last_sell_order_uuid = None
            """

            # 60초 대기
            t.sleep(60)


        obj.info_method("rises매수 배치 작업 종료")
    except KeyboardInterrupt:
        print("프로그램이 종료되었습니다.")

if __name__ == "__main__":
    main()
