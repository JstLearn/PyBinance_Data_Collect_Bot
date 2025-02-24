# import datetime
# import time
# import pyodbc as db
# import data
# from binance.client import Client
# import pandas as pd
# import requests as r
# import urllib.request
# import multiprocessing
# # import threading
# # import numpy as np
# import hmac
# import hashlib
# import json
# from urllib.parse import urljoin, urlencode
# # from TradingView import *
#
#
#
#
# # -----------------SQL BAĞLANTISI--------------------
# db = db.connect('Driver={SQL Server};'
#                 'Server=DENIZ;'
#                 'Database=Binance;'
#                 'Trusted_Connection=True;'
#                 'initial katalog=true;')
# cursor = db.cursor()
#
#
# # -----------------API BAĞLANTISI--------------------
# client = Client(api_key=data.Pkey, api_secret=data.Skey)
#
#
# def get_all_symbols_fapi():
#     a = urllib.request.urlopen(f"{data.fapi}/exchangeInfo").read()
#     return list(map(lambda symbol: symbol['symbol'], json.loads(a)))
#
#
# def get_all_symbols():
#     a = urllib.request.urlopen(f"{data.api0}/api/v3/exchangeInfo").read()
#     return list(map(lambda symbol: symbol['symbol'], json.loads(a)['symbols']))
#
#
# def parametreler():
#     params = {
#         'symbol': 'BTCUSDT', 'interval': '15m', 'limit': 50, 'timestamp': int(time.time())
#     }
#     querystring = urlencode(parametreler())
#     params['signature'] = hmac.new(data.Skey.encode('utf-8'), querystring.encode('utf-8'),
#                                    hashlib.sha256).hexdigest()
#     url = data.fapi
#     headers = {
#         'Content-Type': 'application/json',
#         'X-MBX-APIKEY': data.Pkey
#     }
#     response = r.request("GET", url, headers=headers, params=params).json()
#     return response
#
#
# def coin_update():   # exchange info tekte çekilebiliyormuş düzenleme yap
#     start = time.time()
#     # -----------------------------COIN İSİMLERİ GÜNCELLEME---------------------------------------------------
#     binance_coin_list = list(map(lambda x: x['symbol'], client.get_all_tickers()))
#     cursor.execute('select * from Pairs')
#     db_coin_list = tuple(map(lambda x: x[0], cursor.fetchall()))
#     for each in db_coin_list:
#         sayi = 0
#         for i in binance_coin_list:
#             if each == i:
#                 sayi += 1
#         if sayi == 0:
#             print(each, 'Coinin adı değişmiş Pairs ve PairSpecs tablosundan SİLDİM')
#             cursor.execute("delete from Pairs  where CoinPairs=(?)", each)
#             cursor.execute("delete from PairSpecs  where symbol=(?)", each)
#     db.commit()
#     sayac = 0
#     yeni_coinler = []
#     for each in binance_coin_list:
#         if cursor.execute("select count(*) from Pairs where CoinPairs=(?)", each).fetchone()[0] == 0:
#             sayac += 1
#             yeni_coinler.append(each)
#             print(sayac, each, 'Eklendi')
#             cursor.execute("insert into Pairs (CoinPairs) Values((?))", each)
#         elif cursor.execute("select count(*) from Pairs where CoinPairs=(?)", each).fetchone()[0] == 1:
#             sayac += 1
#             print(sayac, each, 'Güncellendi')
#             cursor.execute("update Pairs set CoinPairs=(?) where CoinPairs=(?)", each, each)
#         else:
#             sayac += 1
#             print(sayac, each, 'Silinip Tekrar Eklendi')
#             cursor.execute("delete from Pairs  where CoinPairs=(?)", each)
#             cursor.execute("insert into Pairs (CoinPairs) Values((?))", each)
#     print('\n', 'Yeni eklenen Coinler = ', yeni_coinler, '\n')
#
# # -----------------------------COIN ÖZELLİKLERİ GÜNCELEME------------------------------------------------------
#     cursor.execute('select * from Pairs')
#     pairs = tuple(map(lambda x: x[0], cursor.fetchall()))
#     for i in range(len(pairs)):
#         time.sleep(0.02)   # aksi halde binance banns for a while
#         coinspecs = client.get_symbol_info(pairs[i])
#         filters = coinspecs['filters']
#         PRICE_FILTER_minPrice = 0
#         PRICE_FILTER_maxPrice = 0
#         PRICE_FILTER_tickSize = 0
#         PERCENT_PRICE_multiplierUp = 0
#         PERCENT_PRICE_multiplierDown = 0
#         PERCENT_PRICE_avgPriceMins = 0
#         LOT_SIZE_minQty = 0
#         LOT_SIZE_maxQty = 0
#         LOT_SIZE_stepSize = 0
#         MIN_NOTIONAL_minNotional = 0
#         MIN_NOTIONAL_applyToMarket = 0
#         MIN_NOTIONAL_avgPriceMins = 0
#         ICEBERG_PARTS_limit = 0
#         MARKET_LOT_SIZE_minQty = 0
#         MARKET_LOT_SIZE_maxQty = 0
#         MARKET_LOT_SIZE_stepSize = 0
#         MAX_NUM_ORDERS_maxNumOrders = 0
#         MAX_NUM_ALGO_ORDERS_maxNumAlgoOrders = 0
#         for each in filters:
#             if each['filterType'] == 'PRICE_FILTER':
#                 PRICE_FILTER_minPrice = each['minPrice']
#                 PRICE_FILTER_maxPrice = each['maxPrice']
#                 PRICE_FILTER_tickSize = each['tickSize']
#             elif each['filterType'] == 'PERCENT_PRICE':
#                 PERCENT_PRICE_multiplierUp = each['multiplierUp']
#                 PERCENT_PRICE_multiplierDown = each['multiplierDown']
#                 PERCENT_PRICE_avgPriceMins = each['avgPriceMins']
#             elif each['filterType'] == 'LOT_SIZE':
#                 LOT_SIZE_minQty = each['minQty']
#                 LOT_SIZE_maxQty = each['maxQty']
#                 LOT_SIZE_stepSize = each['stepSize']
#             elif each['filterType'] == 'MIN_NOTIONAL':
#                 MIN_NOTIONAL_minNotional = each['minNotional']
#                 MIN_NOTIONAL_applyToMarket = each['applyToMarket']
#                 MIN_NOTIONAL_avgPriceMins = each['avgPriceMins']
#             elif each['filterType'] == 'ICEBERG_PARTS':
#                 ICEBERG_PARTS_limit = each['limit']
#             elif each['filterType'] == 'MARKET_LOT_SIZE':
#                 MARKET_LOT_SIZE_minQty = each['minQty']
#                 MARKET_LOT_SIZE_maxQty = each['maxQty']
#                 MARKET_LOT_SIZE_stepSize = each['stepSize']
#             elif each['filterType'] == 'MAX_NUM_ORDERS':
#                 MAX_NUM_ORDERS_maxNumOrders = each['maxNumOrders']
#             elif each['filterType'] == 'MAX_NUM_ALGO_ORDERS':
#                 MAX_NUM_ALGO_ORDERS_maxNumAlgoOrders = each['maxNumAlgoOrders']
#         coin = (coinspecs['symbol'], coinspecs['status'], coinspecs['baseAsset'], coinspecs['baseAssetPrecision'],
#                 coinspecs['quoteAsset'], coinspecs['quotePrecision'], coinspecs['quoteAssetPrecision'],
#                 coinspecs['baseCommissionPrecision'], coinspecs['quoteCommissionPrecision'],
#                 str(coinspecs['icebergAllowed']), str(coinspecs['ocoAllowed']),
#                 str(coinspecs['quoteOrderQtyMarketAllowed']),
#                 str(coinspecs['isSpotTradingAllowed']), str(coinspecs['isMarginTradingAllowed']),
#                 PRICE_FILTER_minPrice, PRICE_FILTER_maxPrice, PRICE_FILTER_tickSize, PERCENT_PRICE_multiplierUp,
#                 PERCENT_PRICE_multiplierDown, PERCENT_PRICE_avgPriceMins, LOT_SIZE_minQty,
#                 LOT_SIZE_maxQty, LOT_SIZE_stepSize, MIN_NOTIONAL_minNotional, str(MIN_NOTIONAL_applyToMarket),
#                 MIN_NOTIONAL_avgPriceMins, ICEBERG_PARTS_limit, MARKET_LOT_SIZE_minQty, MARKET_LOT_SIZE_maxQty,
#                 MARKET_LOT_SIZE_stepSize, MAX_NUM_ORDERS_maxNumOrders, MAX_NUM_ALGO_ORDERS_maxNumAlgoOrders)
#         if cursor.execute("select count(*) from PairSpecs where symbol=(?)", pairs[i]).fetchone()[0] == 0:
#             print(f"{i} numaralı coinden {cursor.execute('select count(*) from PairSpecs where symbol=(?)', pairs[i]).fetchone()[0]} adet var EKLEDİM {coin}")
#             cursor.execute("insert into PairSpecs Values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,"
#                            " ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", coin)
#         elif cursor.execute("select count(*) from PairSpecs where symbol=(?)", pairs[i]).fetchone()[0] == 1:
#             print(f"{i} numaralı coinden {cursor.execute('select count(*) from PairSpecs where symbol=(?)', pairs[i]).fetchone()[0]} adet var GÜNCELLEDİM {coin}")
#             a = list(coin)
#             a.append(pairs[i])
#             cursor.execute("update PairSpecs set symbol=(?), status=(?), baseAsset=(?), baseAssetPrecision=(?), "
#                            "quoteAsset=(?), quotePrecision=(?), quoteAssetPrecision=(?), baseCommissionPrecision=(?), "
#                            "quoteCommissionPrecision=(?), icebergAllowed=(?), ocoAllowed=(?), "
#                            "quoteOrderQtyMarketAllowed=(?), isSpotTradingAllowed=(?), isMarginTradingAllowed=(?), "
#                            "PRICE_FILTER_minPrice=(?), PRICE_FILTER_maxPrice=(?), PRICE_FILTER_tickSize=(?), "
#                            "PERCENT_PRICE_multiplierUp=(?), PERCENT_PRICE_multiplierDown=(?), "
#                            "PERCENT_PRICE_avgPriceMins=(?), LOT_SIZE_minQty=(?), LOT_SIZE_maxQty=(?), "
#                            "LOT_SIZE_stepSize=(?), MIN_NOTIONAL_minNotional=(?), MIN_NOTIONAL_applyToMarket =(?), "
#                            "MIN_NOTIONAL_avgPriceMins=(?), ICEBERG_PARTS_limit =(?), MARKET_LOT_SIZE_minQty =(?), "
#                            "MARKET_LOT_SIZE_maxQty =(?), MARKET_LOT_SIZE_stepSize =(?), "
#                            "MAX_NUM_ORDERS_maxNumOrders =(?), MAX_NUM_ALGO_ORDERS_maxNumAlgoOrders=(?) where symbol=(?)", a)
#         else:
#             print(f"{i} numaralı coinden {cursor.execute('select count(*) from PairSpecs where symbol=(?)', pairs[i]).fetchone()[0]} adet var HEPSİNİ SİLİP YENİ EKLEDİM {coin}")
#             cursor.execute("delete from PairSpecs  where symbol=(?)", pairs[i])
#             cursor.execute("insert into PairSpecs Values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
#                            "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", coin)
#     db.commit()
#     print(time.time() - start)
#
#
# # coin_update()
#
#
# last_rendered_timestamps = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#
#
# def get_klines(coinname):
#     start = time.time()
#     intervals = ('1MONTH', '1w', '3d', '1d', '12h', '8h', '6h', '4h', '2h', '1h', '30m', '15m', '5m', '3m', '1m')
#     intervals_duration = (2678400, 604800, 259200, 86400, 43200, 28800, 21600, 14400, 7200, 3600, 1800, 900, 300, 180, 60)
#     intervals_binance = (Client.KLINE_INTERVAL_1MONTH, Client.KLINE_INTERVAL_1WEEK, Client.KLINE_INTERVAL_3DAY, Client.KLINE_INTERVAL_1DAY, Client.KLINE_INTERVAL_12HOUR, Client.KLINE_INTERVAL_8HOUR, Client.KLINE_INTERVAL_6HOUR, Client.KLINE_INTERVAL_4HOUR, Client.KLINE_INTERVAL_2HOUR, Client.KLINE_INTERVAL_1HOUR, Client.KLINE_INTERVAL_30MINUTE, Client.KLINE_INTERVAL_15MINUTE, Client.KLINE_INTERVAL_5MINUTE, Client.KLINE_INTERVAL_3MINUTE, Client.KLINE_INTERVAL_1MINUTE)
#     stamp_now = int(time.time())
#     intervals_sql = []
#     for i in range(len(intervals)):
#         if stamp_now > last_rendered_timestamps[i]+intervals_duration[i]:   # last_rendered_timestamps[i] her işleme girdiğinde yeni değeri almalı
#             intervals_sql.append(intervals[i])
#             last_rendered_timestamps[i] = stamp_now
#     for a in range(len(intervals_sql)):
#         intervaltime = time.time()
#         try:                             # DB'de last timestamp varsa son eklenenden günümüze kadar alıcaz
#             cursor.execute("select top (1) Open_time from Klines where symbol=(?) and interval=(?) order by Open_time desc", coinname, intervals_sql[a])
#             last_timestamp = cursor.fetchone()[0]
#             bars_since_last_log = client.get_historical_klines(coinname, intervals_binance[intervals.index(intervals_sql[a])], last_timestamp)[1:-1]
#             for i in range(len(bars_since_last_log)):
#                 to_sql = (coinname, intervals_sql[a], 'Binance', bars_since_last_log[i][0], bars_since_last_log[i][1], bars_since_last_log[i][2], bars_since_last_log[i][3], bars_since_last_log[i][4], bars_since_last_log[i][5], bars_since_last_log[i][6], bars_since_last_log[i][7], bars_since_last_log[i][8], bars_since_last_log[i][9], bars_since_last_log[i][10], bars_since_last_log[i][11])
#                 cursor.execute("insert into Klines Values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", to_sql)
#             print(f"{coinname} çiftinin {intervals_sql[a]} barlarının {pd.to_datetime(last_timestamp, unit='ms')} Tarihinden itibaren {len(bars_since_last_log)} Adet verisini SQL Klines Tablosuna {round(time.time() - intervaltime, 3)} Saniyede ekledim {datetime.datetime.now().strftime('%H:%M:%S')}")
#         except TypeError:                # DB'de last timestamp yoksa başlangıçtan itibaren alıcaz
#             bars_since_listed = client.get_historical_klines(coinname, intervals_binance[a], 1225411200000)[:-1]  # 31 Ekim 2008
#             for bar in range(len(bars_since_listed)):
#                 to_sql = (coinname, intervals_sql[a], 'Binance', bars_since_listed[bar][0], bars_since_listed[bar][1], bars_since_listed[bar][2], bars_since_listed[bar][3], bars_since_listed[bar][4], bars_since_listed[bar][5], bars_since_listed[bar][6], bars_since_listed[bar][7], bars_since_listed[bar][8], bars_since_listed[bar][9], bars_since_listed[bar][10], bars_since_listed[bar][11])
#                 cursor.execute("insert into Klines Values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", to_sql)
#             print(f"{coinname} çiftinin {intervals_sql[a]} barlarının başlangıç tarihinden itibaren {len(bars_since_listed)} Adet verisini SQL Klines Tablosuna {round(time.time()-intervaltime, 3)} Saniyede ekledim {datetime.datetime.now().strftime('%H:%M:%S')}")
#         db.commit()
#     if round(time.time() - start, 3) > 3:
#         print(f"{intervals_sql} Tarandı {round(time.time() - start, 3)} Saniye sürdü {datetime.datetime.now().strftime('%H:%M:%S')}")
#
#
# cursor.execute('select * from Pairs')
# coinnames = tuple(map(lambda x: x[0], cursor.fetchall()))
# pairs2 = coinnames[1:2][0]
# print(pairs2)
# if __name__ == '__main__':
#     for pair in pairs2:
#         get_klines(pair)
#
#
# def uyu(saniye):
#     print(f"sleeping {saniye} second(s)")
#     time.sleep(saniye)
#     print("uyuma bitti")
#
#
# p1 = multiprocessing.Process(target=uyu, args=[1])
# p2 = multiprocessing.Process(target=uyu, args=[1])
#
# if __name__ == '__main__':
#     p1.start()
#     p2.start()
#
# finish = time.perf_counter()
# print(f"{finish} saniye sürdü")