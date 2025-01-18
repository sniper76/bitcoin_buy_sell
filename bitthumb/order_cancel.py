import os
from dotenv import load_dotenv
load_dotenv ()
import requests
import python_bithumb
from upbit.log_appendar import PrintLogger

access_key = os.getenv("BITHUMB_ACCESS_KEY")
secret_key = os.getenv("BITHUMB_SECRET_KEY")

bithumb = python_bithumb.Bithumb(access_key, secret_key)

def cancel_order(uuid:str):
    obj = PrintLogger("BitTb")
    # 주문 취소 (UUID 필요)
    try:
        cancel_result = bithumb.cancel_order(uuid)
        obj.info_method(f"주문 취소: {uuid} {cancel_result}")

        return cancel_result
    except requests.exceptions.HTTPError as e:
        obj.info_method(e.response.text)  # 에러 응답 내용 확인