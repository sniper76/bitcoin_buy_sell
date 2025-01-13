import os
from dotenv import load_dotenv
load_dotenv ()
import python_bithumb

access_key = os.getenv("BITHUMB_ACCESS_KEY")
secret_key = os.getenv("BITHUMB_SECRET_KEY")

bithumb = python_bithumb.Bithumb(access_key, secret_key)

# 주문 가능 정보 조회 (주문 전 최소 거래금액, 수수료 등 확인)
chance_info = bithumb.get_order_chance("KRW-BTC")
print(chance_info)
#print(chance_info["bid_account"]["balance"])
#print(chance_info["bid_account"]["locked"])# 매수 주문 존재시 락걸림주문 존재시 락걸림
#print(chance_info["ask_account"]["balance"])
#print(chance_info["ask_account"]["locked"])# 매도 주문 존재시 락걸림주문 존재시 락걸림
#print(chance_info["bid_fee"])
#print(chance_info["ask_fee"])