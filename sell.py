import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv
import requests
load_dotenv ()
import python_bithumb
from order_chance import get_balance_and_locked_and_fee
from price_util import cutting_unit_price

access_key = os.getenv("BITHUMB_ACCESS_KEY")
secret_key = os.getenv("BITHUMB_SECRET_KEY")

bithumb = python_bithumb.Bithumb(access_key, secret_key)

def sell_btc(current_price=int, quantity=float):
    # Simulate a sell operation
    try:
        # 잔액과 수수료 가져오기
        response = get_balance_and_locked_and_fee()
        data = json.loads(response)  # JSON 문자열을 딕셔너리로 변환

        # 매도 잔고가 있고 매도 주문이 없으면서 매수 주문도 없는 상태만 매도 한다.
        if data["ask_balance"] > 0 and data["ask_locked"] == 0 and data["bid_locked"] == 0:

            # 매도가 현재가 + 0.02%
            sell_price = float(current_price + (current_price * 0.0002))
            final_sell_price = cutting_unit_price(1000, sell_price)
        
            print(f"매도 가격: {current_price} {final_sell_price}, {quantity}")

            order_info = bithumb.sell_limit_order("KRW-BTC", final_sell_price, quantity)

            # 로그 파일 설정
            with open("/Users/sniper76/VScodeProjects/result.txt", 'a') as the_file:
                the_file.write(f"매도 주문 생성: {order_info}\n")

            return order_info

    except requests.exceptions.HTTPError as e:
        print(e.response.text)  # 에러 응답 내용 확인
