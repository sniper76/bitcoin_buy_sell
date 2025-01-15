import python_bithumb
import csv

def get_volatility_rate_bar_chart_data():
    # 1. 빗썸 차트 데이터 가져오기 (1분봉)
    df = python_bithumb.get_ohlcv("KRW-BTC", interval="minute3", count=10)

    # 조건 2: 하락율 차이값 계산
    df["diff_1"] = df["close"].diff()  # 이전 열과 종가 차이

    df_length = 10
    
    # 변동폭 계산
    df["volatility"] = df["high"] - df["low"]

    # 변동 비율 계산
    df["volatility_rate"] = (df["volatility"] / df["low"]) * 100

    # 변동 비율 소수점 제한
    df["volatility_rate"] = df["volatility_rate"].round(2)

    # 조건 3: 매수 조건 (차이값이 양수인 경우 매수)
    df["buy_signal"] = df["diff_1"].diff() > 0

    #마지막에서 두번째 열(1분전 종가)
    last_second_row_volatility_rate = float(df["volatility_rate"].iloc[df_length - 2])
    
    last_second_row_close_price = float(df["close"].iloc[df_length - 2])
    last_row_close_price = float(df["close"].iloc[df_length - 1])

    last_second_row_diff_price = float(df["diff_1"].iloc[df_length - 2])
    last_row_diff_price = float(df["diff_1"].iloc[df_length - 1])

    #print(df.dtypes)
    
    #print(df[["open", "low", "high", "close", "volatility", "volatility_rate", "diff_1", "buy_signal"]])
    print(f"last_second_row_volatility_rate: {last_second_row_volatility_rate}, last_second_row_close_price: {last_second_row_close_price}, last_row_close_price: {last_row_close_price}")
    if last_second_row_volatility_rate > 0.05 and last_second_row_close_price < last_row_close_price and last_second_row_diff_price > 0 and last_row_diff_price > 0:
        column_names = ['candle_date_time_utc', 'diff_1', 'open', 'low', 'high', 'close', 'volatility', 'volatility_rate', 'buy_signal']

        #buy_signal = df.iloc[-1, -1]
        #df.to_csv('/Users/sniper76/VScodeProjects/result.csv', mode='a', sep='\t', columns=column_names, header=True, index=False)

        data = {
            "buy_signal": True,
            "buy_price": last_second_row_close_price,
            "sell_price": last_row_close_price
        }
        return data

    data = {
        "buy_signal": False
    }
    return data

