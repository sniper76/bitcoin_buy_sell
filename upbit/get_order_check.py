import os
from dotenv import load_dotenv
load_dotenv ()
import pyupbit
import json
import requests


upbit = pyupbit.Upbit(os.getenv("UPBIT_ACCESS_KEY"), os.getenv("UPBIT_SECRET_KEY"))

# order_check.py
def get_order(uuid:str):
    #주문조회
    try:
        # 개별 주문 조회 (UUID 필요)
        order_detail = upbit.get_order(uuid)
        #print(order_detail)
        data = {
            "state": order_detail["state"],
            "price": float(order_detail["price"]),
            "remaining_volume": float(order_detail["remaining_volume"])
        }
        return data
    except requests.exceptions.HTTPError as e:
        print(e.response.text)  # 에러 응답 내용 확인

# Example usage
if __name__ == "__main__":
    print(get_order('C0101000002070778601'))