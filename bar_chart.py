import python_bithumb
import csv

def get_bar_chart_data():
    # 1. 빗썸 차트 데이터 가져오기 (1분봉)
    df = python_bithumb.get_ohlcv("KRW-BTC", interval="minute1", count=10)

    # 조건 2: 하락율 차이값 계산
    df["diff_1"] = df["close"].diff()  # 이전 열과 종가 차이

    df_length = 10

    # 조건 3: 매수 조건 (차이값이 양수인 경우 매수)
    df["buy_signal"] = (df["diff_1"].iloc[df_length - 1] > 0) & (df["diff_1"].iloc[df_length - 2] > 0)

    column_names = ['candle_date_time_utc', 'diff_1', 'open', 'low', 'high', 'close', 'buy_signal']

    result = df.iloc[-1, -1]
    if result:
        df.to_csv('/Users/sniper76/VScodeProjects/result.csv', mode='a', sep='\t', columns=column_names, header=True, index=False)

    return result

