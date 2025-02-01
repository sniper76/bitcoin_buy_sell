import time
from datetime import datetime, timedelta
import json
from price_util import cutting_unit_price
from bitthumb.order_chance import get_balance_and_locked_and_fee
from bitthumb.bar_chart_data import BarChartData
from bitthumb.get_buy_signal import BuySignalData
from bitthumb.log_appendar import PrintLogger
from bitthumb.buy import buy_btc
from bitthumb.sell import sell_btc

def wait_until_next_day():
    """
    Waits until the next day at 00:00 to resume the process.
    """
    now = datetime.now()
    next_day = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    wait_seconds = (next_day - now).total_seconds()
    print(f"대기중... {next_day}")
    time.sleep(wait_seconds)

def main():
    try:
        obj = PrintLogger("BitTb")
        barChart = BarChartData()
        buySingal = BuySignalData()
        obj.info_method("daybar매수 배치 작업 시작")

        while True:
            # 잔액과 수수료 가져오기
            response = get_balance_and_locked_and_fee()
            data = json.loads(response)  # JSON 문자열을 딕셔너리로 변환

            #bar_char_data = barChart.get_price_day()
            #bar_char_data = barChart.get_price_minute3()
            bar_char_data = barChart.get_price_minute10()
            buy_signal_data = buySingal.get_price_day_bar_body_size(bar_char_data)

            if data["bid_balance"] > 9990 and data["bid_locked"] == 0 and data["ask_balance"] == 0 and data["ask_locked"] == 0 and buy_signal_data["buy_signal"]:
                obj.info_method("daybar매수 프로세스 시작!!")

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

                if buy_result["is_completed"]:
                    sell_result = sell_btc(sell_price, quantity)
                    #last_sell_order_uuid = sell_result["uuid"]
                    # Pause until the next day
                    #wait_until_next_day()

            time.sleep(60)  # Wait for 600 is 10 minutes

        obj.info_method("daybar매수 배치 작업 종료")
    except KeyboardInterrupt:
        print("프로그램이 종료되었습니다.")

if __name__ == "__main__":
    main()
