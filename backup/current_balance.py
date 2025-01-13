import os
from dotenv import load_dotenv
load_dotenv ()
import python_bithumb

access_key = os.getenv("BITHUMB_ACCESS_KEY")
secret_key = os.getenv("BITHUMB_SECRET_KEY")

bithumb = python_bithumb.Bithumb(access_key, secret_key)

# 특정 화폐의 잔고 조회
krw_balance = bithumb.get_balance("KRW")
print(krw_balance)
#print(krw_balance - (krw_balance * 0.1))