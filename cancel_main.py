# main.py
import time
import json
import python_bithumb
from datetime import datetime, timedelta
from order_chance import get_balance_and_locked_and_fee
from order_cancel import sell_cancel
from find_text import find_last_row_uuid_and_state
from check_minute import is_time_exceeded
from sell_market_price import sell_market_btc

def main():
    try:
        while True:
            result = find_last_row_uuid_and_state('/Users/sniper76/VScodeProjects/result.txt')
            #print(result)

            # 잔액과 수수료 가져오기
            response = get_balance_and_locked_and_fee()
            data = json.loads(response)  # JSON 문자열을 딕셔너리로 변환
            
            if result['side'] == 'ask' and is_time_exceeded(result['created_at']) and data["ask_locked"] > 0:
                cancel_result = sell_cancel(result['uuid'])

                time.sleep(2)
                #현재 시장가로 바로 매도 주문 처리
                sell_market_btc(float(cancel_result["remaining_volume"]))

            # 2분 대기
            time.sleep(120)

    except KeyboardInterrupt:
        print("프로그램이 종료되었습니다.")

if __name__ == "__main__":
    main()
