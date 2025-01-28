import os
from dotenv import load_dotenv
load_dotenv ()
import time
from datetime import datetime
import json
import requests
import python_bithumb
from bitthumb.order_check import order_state_check
from bitthumb.log_appendar import PrintLogger

access_key = os.getenv("BITHUMB_ACCESS_KEY")
secret_key = os.getenv("BITHUMB_SECRET_KEY")

bithumb = python_bithumb.Bithumb(access_key, secret_key)

def buy_btc(price:int, quantity:float, loopCount:int):
    # 지정가 매수 주문 (예: KRW-BTC를 139,000,000원에 0.0001 BTC 매수)
    try:
        obj = PrintLogger("BitTb")
        obj.info_method(f"매수 가격: {price}, {quantity}")
        order_info = bithumb.buy_limit_order("KRW-BTC", price, quantity)

        buy_uuid = order_info["uuid"]
        #print(f"Buy initiated with UUID: {buy_uuid}")

        # 로그 파일 설정
        #with open("/Users/sniper76/VScodeProjects/result.txt", 'a') as the_file:
        #    the_file.write(f"매수 주문 생성: {order_info}\n")

        # Check if the buy is completed
        result = order_state_check(buy_uuid, "매수", loopCount)
        
        data = {
            "is_completed": result["is_completed"],
            "buy_price": result["price"]
        }
        return data
    except requests.exceptions.HTTPError as e:
        print(e.response.text)  # 에러 응답 내용 확인