import os
from dotenv import load_dotenv
load_dotenv ()
import python_bithumb
import json
import requests
from upbit.log_appendar import PrintLogger

access_key = os.getenv("BITHUMB_ACCESS_KEY")
secret_key = os.getenv("BITHUMB_SECRET_KEY")

bithumb = python_bithumb.Bithumb(access_key, secret_key)

# order_check.py
def get_order(uuid:str):
    obj = PrintLogger("BitTb")
    try:
        obj.debug_method(f"개별 주문 조회: {uuid}")
        # 개별 주문 조회 (UUID 필요)
        order_detail = bithumb.get_order(uuid)
        #print(order_detail)
        data = {
            "state": order_detail["state"],
            "buy_price": float(order_detail["price"]),
            "remaining_volume": float(order_detail["remaining_volume"])
        }
        return data
    except requests.exceptions.HTTPError as e:
        obj.debug_method(e.response.text)  # 에러 응답 내용 확인

# Example usage
#if __name__ == "__main__":
#    print(get_order('C0101000002070778601'))