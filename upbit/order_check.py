import time
import json
import requests
from upbit.get_order_check import get_order  # Assuming this function exists in api.py
from upbit.order_cancel import cancel_order
from upbit.log_appendar import PrintLogger

def order_state_check(uuid:str, typeText:str, sleepSecond=int):
    loggerObj = PrintLogger("Upbit")
    try:
        #print(f"Checking order status for UUID: {uuid}")
        loop = 0
        while True:
            loop += 1
            loggerObj.debug_method(f"Checking status...{loop}")
            result = get_order(uuid)

            #print(result)
            if result["state"] == 'done' and result["remaining_volume"] == 0:  # Replace with actual API call
                loggerObj.info_method(f"{typeText} 성공: {uuid}, price: {result["price"]}")
                data = {
                    "is_completed": True,
                    "price": float(result["price"])
                }
                return data
            if loop == 10:
                cancel_order(uuid)
                loggerObj.info_method(f"10회 시도 후 주문 취소: {uuid}")
                data = {
                    "is_completed": False,
                    "price": 0
                }
                return data
            
            time.sleep(sleepSecond)
    except requests.exceptions.HTTPError as e:
        print(e.response.text)  # 에러 응답 내용 확인

# Example usage
if __name__ == "__main__":
    print(order_state_check('C0101000002070778601'))