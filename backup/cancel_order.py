import os
from dotenv import load_dotenv
load_dotenv ()
import requests
import python_bithumb

access_key = os.getenv("BITHUMB_ACCESS_KEY")
secret_key = os.getenv("BITHUMB_SECRET_KEY")

try:
    bithumb = python_bithumb.Bithumb(access_key, secret_key)

    uuid = "C0101000002078007904"
    cancel_result = bithumb.cancel_order(uuid)
    print(f"주문 취소: {uuid} {cancel_result}")
except requests.exceptions.HTTPError as e:
    print(e.response.text)  # 에러 응답 내용 확인