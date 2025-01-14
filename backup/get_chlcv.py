import time
import json
import python_bithumb
from datetime import datetime
import csv

# 1. 빗썸 차트 데이터 가져오기 (1분봉)
df = python_bithumb.get_ohlcv("KRW-BTC", interval="minute1", count=10)

#print(df["close"].diff(1))
#print(df["close"].diff(2))

# 조건 2: 하락율 차이값 계산 (이전 두개의 열과 비교)
df["diff_1"] = df["close"].diff()  # 이전 열과 차이

# 조건 3: 매수 조건 (차이값이 양수인 경우 매수)
df["buy_signal"] = (df["diff_1"].iloc[9] > 0) & (df["diff_1"].iloc[8] > 0)

print(df[['close', 'diff_1', 'buy_signal']])
current_date = datetime.now()
result = df.iloc[9]
print(current_date)
print(result)
