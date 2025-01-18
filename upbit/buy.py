import os
from dotenv import load_dotenv
load_dotenv ()
import time
from datetime import datetime
import json
import requests
import pyupbit
from upbit.buy_check import buy_state_check
from upbit.log_appendar import PrintLogger


upbit = pyupbit.Upbit(os.getenv("UPBIT_ACCESS_KEY"), os.getenv("UPBIT_SECRET_KEY"))

def buy_btc(price=int, quantity=float):
    # 지정가 매수 주문 (예: KRW-BTC를 139,000,000원에 0.0001 BTC 매수)
    loggerObj = PrintLogger("Upbit")
    try:
        order_info = upbit.buy_limit_order("KRW-BTC", price, quantity)

        buy_uuid = order_info["uuid"]

        result = buy_state_check(buy_uuid)
        
        data = {
            "is_completed": result["is_completed"],
            "buy_price": result["buy_price"]
        }
        return data
    except requests.exceptions.HTTPError as e:
        print(e.response.text)  # 에러 응답 내용 확인

# Example usage
if __name__ == "__main__":
    print(buy_btc(50000, 0.0001))