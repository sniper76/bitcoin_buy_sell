import os
from dotenv import load_dotenv
load_dotenv ()
import pyupbit
import json


upbit = pyupbit.Upbit(os.getenv("UPBIT_ACCESS_KEY"), os.getenv("UPBIT_SECRET_KEY"))

# order_chance.py
def get_balance_and_locked_and_fee():
    """
    잔액과 수수료 반환 함수
    :return: 잔액, 수수료
    """
    #balance = 10000  # 잔액
    #fee_rate = 0.0005  # 수수료 (0.05%)

    # 주문 가능 정보 조회 (주문 전 최소 거래금액, 수수료 등 확인)
    chance_info = upbit.get_chance("KRW-BTC")

    data = {
        "bid_balance": float(chance_info["bid_account"]["balance"]),
        "bid_locked": float(chance_info["bid_account"]["locked"]),
        "bid_fee_rate": float(chance_info["bid_fee"]),
        "ask_balance": float(chance_info["ask_account"]["balance"]),
        "ask_locked": float(chance_info["ask_account"]["locked"]),
        "ask_fee_rate": float(chance_info["ask_fee"])
    }
    return json.dumps(data)

# Example usage
if __name__ == "__main__":
    print(get_balance_and_locked_and_fee())
