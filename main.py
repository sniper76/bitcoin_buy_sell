# main.py
import time
import json
import python_bithumb
from datetime import datetime
from order_chance import get_balance_and_locked_and_fee
from bar_chart import get_bar_chart_data
from buy import buy_btc
from sell import sell_btc
from sell_market_price import sell_market_btc
from buy_market_price import buy_market_btc

def main():
    try:
        """
        배치 작업: 0시 0분 0초부터 6시 0분 0초까지 실행
        """
        print("매수 배치 작업 시작")
        start_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = start_time.replace(hour=6)

        #while datetime.now() < end_time:
        while True:
            # 잔액과 수수료 가져오기
            response = get_balance_and_locked_and_fee()
            data = json.loads(response)  # JSON 문자열을 딕셔너리로 변환

            buy_signal = get_bar_chart_data()

            if data["bid_balance"] > 9990 and data["bid_locked"] == 0 and data["ask_balance"] == 0 and data["ask_locked"] == 0 and buy_signal:
                print("매수 프로세스 시작!!")

                # 매수가 계산: 잔액 - (수수료 * 2)
                balance = data["bid_balance"]
                fee_rate = data["bid_fee_rate"]
                total_balance = balance - (balance * fee_rate * 2)

                # 현재가 조회 (단일 티커)
                current_price = python_bithumb.get_current_price("KRW-BTC")

                # 수량 계산
                quantity = round(total_balance / current_price, 7)
                buy_result = buy_btc(current_price, quantity)
                #buy_market_btc(current_price) 시장가 매수로 가능한가???

                if buy_result["is_completed"]:
                    #print("Executing sell operation...")
                    sell_result = sell_btc(current_price, quantity)

                    #sell_result = sell_market_btc(quantity) 시장가로 매도 해도 될까?
                    sell_uuid = sell_result["uuid"]
                    print(f"Sell completed UUID: {sell_uuid}")

            # 3분 대기
            time.sleep(180)

        print("매수 배치 작업 종료")
    except KeyboardInterrupt:
        print("프로그램이 종료되었습니다.")

if __name__ == "__main__":
    main()
