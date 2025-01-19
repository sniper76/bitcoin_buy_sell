from datetime import datetime, time
import time as t

def run_process():
    while True:
        now = datetime.now().time()  # 현재 시간 가져오기
        
        # 23:00 ~ 06:00 사이인지 확인
        if time(23, 0, 0) <= now or now <= time(6, 0, 0):
            print("run")
        else:
            print("processing")
        
        # 1분 대기
        t.sleep(60)

# 함수 실행
if __name__ == "__main__":
    run_process()
