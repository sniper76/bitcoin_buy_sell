import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv
import requests
load_dotenv ()
import pyupbit
from upbit.order_chance import get_balance_and_locked_and_fee
from upbit.log_appendar import PrintLogger
from upbit.order_check import order_state_check


upbit = pyupbit.Upbit(os.getenv("UPBIT_ACCESS_KEY"), os.getenv("UPBIT_SECRET_KEY"))

def sell_btc(current_price=int, quantity=float, sleepSecond=int):
    # Simulate a sell operation
    loggerObj = PrintLogger("Upbit")
    try:
        # 잔액과 수수료 가져오기
        response = get_balance_and_locked_and_fee()
        data = json.loads(response)  # JSON 문자열을 딕셔너리로 변환

        # 매도 잔고가 있고 매도 주문이 없으면서 매수 주문도 없는 상태만 매도 한다.
        if data["ask_balance"] > 0 and data["ask_locked"] == 0 and data["bid_locked"] == 0:
            loggerObj.info_method(f"매도 가격: {current_price} {quantity}")
            order_info = upbit.sell_limit_order("KRW-BTC", current_price, quantity)

            sell_uuid = order_info["uuid"]

            #result = order_state_check(sell_uuid, "매도", sleepSecond)
            #if result["is_completed"] == False:
            #    market_result = upbit.sell_market_order("KRW-BTC", quantity)
            #    loggerObj.info_method(f"시장가 매도: {market_result}")

            return order_info

    except requests.exceptions.HTTPError as e:
        loggerObj.debug_method(e.response.text)  # 에러 응답 내용 확인

# Example usage
if __name__ == "__main__":
    print(sell_btc(50000, 0.0001))
