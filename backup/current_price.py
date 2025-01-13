import python_bithumb

# 현재가 조회 (단일 티커)
current_price = python_bithumb.get_current_price("KRW-BTC")
print(current_price)