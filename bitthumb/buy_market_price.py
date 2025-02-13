import os
from dotenv import load_dotenv
import requests
load_dotenv ()
import python_bithumb

access_key = os.getenv("BITHUMB_ACCESS_KEY")
secret_key = os.getenv("BITHUMB_SECRET_KEY")

bithumb = python_bithumb.Bithumb(access_key, secret_key)

def buy_market_btc(price=float):
    try:
        order_info = bithumb.buy_market_order("KRW-BTC", price)
        print(f"시장가 주문 매수: {price} {order_info}")

        # 로그 파일 설정
        #with open("/Users/sniper76/VScodeProjects/result.txt", 'a') as the_file:
        #    the_file.write(f"매도 시장가 주문 생성: {order_info}\n")

    except requests.exceptions.HTTPError as e:
        print(e.response.text)  # 에러 응답 내용 확인
