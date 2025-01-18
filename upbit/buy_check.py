import time
import json
import requests
from .order_check import get_order  # Assuming this function exists in api.py
from .order_cancel import cancel_order
from .log_appendar import PrintLogger

def buy_state_check(uuid):
    #상태 주기적 조회
    try:
        #print(f"Checking buy status for UUID: {uuid}")
        loggerObj = PrintLogger("Upbit")
        loop = 0
        while True:
            loop += 1
            result = get_order(uuid)

            #print(result)
            if result["state"] == 'done' and result["remaining_volume"] == 0:  # Replace with actual API call
                loggerObj.info_method(f"매수 성공: {uuid}, price: {result["buy_price"]}")
                data = {
                    "is_completed": True,
                    "buy_price": float(result["buy_price"])
                }
                return data
            if loop == 10:
                cancel_order(uuid)
                loggerObj.info_method(f"10회 시도 후 주문 취소: {uuid}")
                data = {
                    "is_completed": False,
                    "buy_price": 0
                }
                return data
            
            time.sleep(10)
    except requests.exceptions.HTTPError as e:
        print(e.response.text)  # 에러 응답 내용 확인

# Example usage
if __name__ == "__main__":
    print(buy_state_check('C0101000002070778601'))