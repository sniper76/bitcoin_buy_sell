import time
import json
import requests
from bitthumb.get_order_check import get_order  # Assuming this function exists in api.py
from bitthumb.order_cancel import cancel_order
from bitthumb.log_appendar import PrintLogger

def order_state_check(uuid:str, typeText:str):
    obj = PrintLogger("BitTb")
    try:
        #print(f"Checking order status for UUID: {uuid}")
        loop = 0
        while True:
            loop += 1
            obj.debug_method(f"Checking status...{loop}")
            result = get_order(uuid)

            #print(result)
            if result["state"] == 'done' and result["remaining_volume"] == 0:  # Replace with actual API call
                obj.info_method(f"{typeText} 성공: {uuid}, price: {result["price"]}")
                data = {
                    "is_completed": True,
                    "price": float(result["price"])
                }
                return data
            if loop == 10:
                obj.info_method("10회 재시도 후 주문취소")
                cancel_order(uuid)
                data = {
                    "is_completed": False,
                    "buy_price": 0
                }
                return data
            
            time.sleep(10)
    except requests.exceptions.HTTPError as e:
        obj.info_method(e.response.text)  # 에러 응답 내용 확인
# Example usage
#if __name__ == "__main__":
#    print(buy_state_check('C0101000002070778601'))