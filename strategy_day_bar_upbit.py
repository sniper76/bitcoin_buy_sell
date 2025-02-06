import time
from datetime import datetime, timedelta
import json
import pyupbit
from price_util import cutting_unit_price
from upbit.order_chance import get_balance_and_locked_and_fee
from upbit.bar_chart_data import BarChartData
from upbit.log_appendar import PrintLogger
from upbit.buy import buy_btc
from upbit.sell import sell_btc

def wait_until_next_day():
    """
    Waits until the next day at 00:00 to resume the process.
    """
    now = datetime.now()
    next_day = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    wait_seconds = (next_day - now).total_seconds()
    print(f"대기중... {next_day}")
    time.sleep(wait_seconds)

def buy_signal(data):
    """
    1일봉 조회 후 현재가 -3% 이면 매수 하고 매수가에 +2% 로 매도 주문 생성
    """
    DF_LENGTH = 10
    second_to_last_row_close_price = float(data["close"].iloc[DF_LENGTH - 2])
    #last_row_close_price = float(data["close"].iloc[DF_LENGTH - 1])
    current_price = pyupbit.get_current_price("KRW-BTC", False, False)
    result = {
        "buy_signal": check_price(second_to_last_row_close_price, current_price),
        "buy_price": current_price,
        "sell_price": current_price * 1.03
    }
    return result

def check_price(yesterday_close_price: float, current_price: float) -> bool:
    return current_price * 1.03 <= yesterday_close_price

def main():
    try:
        obj = PrintLogger("Upbit")
        barChart = BarChartData()
        obj.info_method("daybar매수 배치 작업 시작")

        while True:
            # 잔액과 수수료 가져오기
            response = get_balance_and_locked_and_fee()
            data = json.loads(response)  # JSON 문자열을 딕셔너리로 변환

            bar_char_data = barChart.get_price_day()
            buy_signal_data = buy_signal(bar_char_data)
            obj.debug_method(f"buy_signal_data: {buy_signal_data}")

            if data["bid_balance"] > 9990 and data["bid_locked"] == 0 and data["ask_balance"] == 0 and data["ask_locked"] == 0 and buy_signal_data["buy_signal"]:
                obj.info_method("daybar매수 프로세스 시작!!")

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

                if buy_result["is_completed"]:
                    sell_result = sell_btc(sell_price, quantity)

            time.sleep(60)  # Wait for 600 is 10 minutes

        obj.info_method("daybar매수 배치 작업 종료")
    except KeyboardInterrupt:
        print("프로그램이 종료되었습니다.")

if __name__ == "__main__":
    main()
