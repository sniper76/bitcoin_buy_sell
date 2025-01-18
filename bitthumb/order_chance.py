import os
from dotenv import load_dotenv
load_dotenv ()
import python_bithumb
import json

access_key = os.getenv("BITHUMB_ACCESS_KEY")
secret_key = os.getenv("BITHUMB_SECRET_KEY")

bithumb = python_bithumb.Bithumb(access_key, secret_key)

# order_chance.py
def get_balance_and_locked_and_fee():
    """
    잔액과 수수료 반환 함수
    :return: 잔액, 수수료
    """
    #balance = 10000  # 잔액
    #fee_rate = 0.0025  # 수수료 (0.25%)

    # 주문 가능 정보 조회 (주문 전 최소 거래금액, 수수료 등 확인)
    chance_info = bithumb.get_order_chance("KRW-BTC")
    #print(chance_info)

    data = {
        "bid_balance": float(chance_info["bid_account"]["balance"]),
        "bid_locked": float(chance_info["bid_account"]["locked"]),
        "bid_fee_rate": float(chance_info["bid_fee"]),
        "ask_balance": float(chance_info["ask_account"]["balance"]),
        "ask_locked": float(chance_info["ask_account"]["locked"]),
        "ask_fee_rate": float(chance_info["ask_fee"])
    }
    return json.dumps(data)
