import time
import json
import requests
from order_check import get_order  # Assuming this function exists in api.py
from order_cancel import cancel_order

def buy_state_check(uuid):
    try:
        #print(f"Checking buy status for UUID: {uuid}")
        loop = 0
        while True:
            time.sleep(10)
            loop += 1
            print(f"Checking status...{loop}")
            result = get_order(uuid)
            if loop == 6:
                print("6 재시도 후 주문취소")
                cancel_order(uuid)
                data = {
                    "is_completed": False,
                    "buy_price": 0
                }
                return data

            #print(result)
            if result["state"] == 'done' and result["remaining_volume"] == 0:  # Replace with actual API call
                print(f"Buy completed UUID: {uuid}")

                data = {
                    "is_completed": True,
                    "buy_price": float(result["buy_price"])
                }
                return data
    except requests.exceptions.HTTPError as e:
        print(e.response.text)  # 에러 응답 내용 확인
# Example usage
#if __name__ == "__main__":
#    print(buy_state_check('C0101000002070778601'))