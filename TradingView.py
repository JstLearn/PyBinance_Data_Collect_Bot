"""from tradingview_ta import TA_Handler, Interval

verial = TA_Handler(
    symbol='BTCUSDT',
    screener='crypto',
    exchange='BINANCE',
    interval=Interval.INTERVAL_15_MINUTES
)

data1 = verial.get_analysis().indicators
data2 = verial.get_analysis().moving_averages
data3 = verial.get_analysis().oscillators
data4 = verial.get_analysis().summary
print(data1)
print(data2)
print(data3)
print(data4)
print(data1['BB.lower'])
"""