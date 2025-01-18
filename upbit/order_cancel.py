import os
from dotenv import load_dotenv
load_dotenv ()
import requests
import pyupbit


upbit = pyupbit.Upbit(os.getenv("UPBIT_ACCESS_KEY"), os.getenv("UPBIT_SECRET_KEY"))

def cancel_order(uuid:str):
    # 주문 취소 (UUID 필요)
    try:
        cancel_result = upbit.cancel_order(uuid)

        return cancel_result
    except requests.exceptions.HTTPError as e:
        print(e.response.text)  # 에러 응답 내용 확인

# Example usage
if __name__ == "__main__":
    print(cancel_order('C0101000002070778601'))