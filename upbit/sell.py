import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv
import requests
load_dotenv ()
import pyupbit
from upbit.order_chance import get_balance_and_locked_and_fee


upbit = pyupbit.Upbit(os.getenv("UPBIT_ACCESS_KEY"), os.getenv("UPBIT_SECRET_KEY"))

def sell_btc(current_price=int, quantity=float):
    # Simulate a sell operation
    try:
        # 잔액과 수수료 가져오기
        response = get_balance_and_locked_and_fee()
        data = json.loads(response)  # JSON 문자열을 딕셔너리로 변환

        # 매도 잔고가 있고 매도 주문이 없으면서 매수 주문도 없는 상태만 매도 한다.
        if data["ask_balance"] > 0 and data["ask_locked"] == 0 and data["bid_locked"] == 0:
            order_info = upbit.sell_limit_order("KRW-BTC", current_price, quantity)

            return order_info

    except requests.exceptions.HTTPError as e:
        obj.debug_method(e.response.text)  # 에러 응답 내용 확인

# Example usage
if __name__ == "__main__":
    print(sell_btc(50000, 0.0001))
