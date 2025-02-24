import datetime
import time
import pyodbc as db
import data
from binance.client import Client
import pandas as pd
import multiprocessing
# import psutil
# import threading


# -----------------SQL BAĞLANTISI--------------------
db = db.connect('Driver={SQL Server};'
                'Server=durak;'
                'Database=Binance;'
                'Trusted_Connection=True;'
                'initial katalog=true;')
cursor = db.cursor()

# -----------------API BAĞLANTISI--------------------
client = Client(api_key=data.Pkey, api_secret=data.Skey)


def coin_update():
    # -----------------------------COIN İSİMLERİ GÜNCELLEME---------------------------------------------------
    # verilerin classlara atılması ---------------------------------------------------------------------------
    exchange = client.get_exchange_info()
    timezone = exchange["timezone"]
    serverTime = exchange["serverTime"]
    rateLimits = exchange["rateLimits"]
    exchangeFilters = exchange["exchangeFilters"]
    symbols = exchange["symbols"]
    binance_coin_list = list(map(lambda x: x['symbol'], symbols))
    # ----------------------------------------------------------------------------------------------------------

    # Pairs tablosundan adı değişen coini silme işlemi----------------------------------------------------------
    cursor.execute('select * from [Binance].[dbo].[Pairs]')
    db_coin_list = tuple(map(lambda x: x[0], cursor.fetchall()))
    for each in db_coin_list:
        sayi = 0
        for i in binance_coin_list:
            if each == i:
                sayi += 1
        if sayi == 0:
            print(each, 'Coinin adı değişmiş Pairs ve PairSpecs ve Klines tablosundan SİLDİM')
            cursor.execute("delete from [Binance].[dbo].[Pairs]  where CoinPairs=(?)", each)
            cursor.execute("delete from [Binance].[dbo].[PairSpecs]  where symbol=(?)", each)
            cursor.execute("delete from [Binance].[dbo].[Klines]  where symbol=(?)", each)
    db.commit()
    # ----------------------------------------------------------------------------------------------------------

    # Pairs tablosuna yeni coinleri ekleme, çift olanları silme ve olanları güncelleme işlemi--------------------
    sayac = 0
    yeni_coinler = []
    for each in binance_coin_list:
        if cursor.execute("select count(*) from [Binance].[dbo].[Pairs] where CoinPairs=(?)", each).fetchone()[0] == 0:
            sayac += 1
            yeni_coinler.append(each)
            print(sayac, each, 'Eklendi')
            cursor.execute("insert into [Binance].[dbo].[Pairs] (CoinPairs) Values((?))", each)
        elif cursor.execute("select count(*) from [Binance].[dbo].[Pairs] where CoinPairs=(?)", each).fetchone()[
            0] == 1:
            sayac += 1
            print(sayac, each, 'Güncellendi')
            cursor.execute("update [Binance].[dbo].[Pairs] set CoinPairs=(?) where CoinPairs=(?)", each, each)
        else:
            sayac += 1
            print(sayac, each, 'Silinip Tekrar Eklendi')
            cursor.execute("delete from [Binance].[dbo].[Pairs] where CoinPairs=(?)", each)
            cursor.execute("insert into [Binance].[dbo].[Pairs] (CoinPairs) Values((?))", each)
    print('\n', 'Yeni eklenen Coinler = ', yeni_coinler, '\n')
    # ----------------------------------------------------------------------------------------------------------

    # CoinSpecs tablosunu güncelleme----------------------------------------------------------------------------
    for i in symbols:
        symbol = i['symbol']
        filters = i['filters']
        PRICE_FILTER_minPrice = 0
        PRICE_FILTER_maxPrice = 0
        PRICE_FILTER_tickSize = 0
        PERCENT_PRICE_multiplierUp = 0
        PERCENT_PRICE_multiplierDown = 0
        PERCENT_PRICE_avgPriceMins = 0
        LOT_SIZE_minQty = 0
        LOT_SIZE_maxQty = 0
        LOT_SIZE_stepSize = 0
        MIN_NOTIONAL_minNotional = 0
        MIN_NOTIONAL_applyToMarket = 0
        MIN_NOTIONAL_avgPriceMins = 0
        ICEBERG_PARTS_limit = 0
        MARKET_LOT_SIZE_minQty = 0
        MARKET_LOT_SIZE_maxQty = 0
        MARKET_LOT_SIZE_stepSize = 0
        MAX_NUM_ORDERS_maxNumOrders = 0
        MAX_NUM_ALGO_ORDERS_maxNumAlgoOrders = 0
        for each in filters:
            if each['filterType'] == 'PRICE_FILTER':
                PRICE_FILTER_minPrice = each['minPrice']
                PRICE_FILTER_maxPrice = each['maxPrice']
                PRICE_FILTER_tickSize = each['tickSize']
            elif each['filterType'] == 'PERCENT_PRICE':
                PERCENT_PRICE_multiplierUp = each['multiplierUp']
                PERCENT_PRICE_multiplierDown = each['multiplierDown']
                PERCENT_PRICE_avgPriceMins = each['avgPriceMins']
            elif each['filterType'] == 'LOT_SIZE':
                LOT_SIZE_minQty = each['minQty']
                LOT_SIZE_maxQty = each['maxQty']
                LOT_SIZE_stepSize = each['stepSize']
            elif each['filterType'] == 'MIN_NOTIONAL':
                MIN_NOTIONAL_minNotional = each['minNotional']
                MIN_NOTIONAL_applyToMarket = each['applyToMarket']
                MIN_NOTIONAL_avgPriceMins = each['avgPriceMins']
            elif each['filterType'] == 'ICEBERG_PARTS':
                ICEBERG_PARTS_limit = each['limit']
            elif each['filterType'] == 'MARKET_LOT_SIZE':
                MARKET_LOT_SIZE_minQty = each['minQty']
                MARKET_LOT_SIZE_maxQty = each['maxQty']
                MARKET_LOT_SIZE_stepSize = each['stepSize']
            elif each['filterType'] == 'MAX_NUM_ORDERS':
                MAX_NUM_ORDERS_maxNumOrders = each['maxNumOrders']
            elif each['filterType'] == 'MAX_NUM_ALGO_ORDERS':
                MAX_NUM_ALGO_ORDERS_maxNumAlgoOrders = each['maxNumAlgoOrders']
        coin = (i['symbol'], i['status'], i['baseAsset'], i['baseAssetPrecision'],
                i['quoteAsset'], i['quotePrecision'], i['quoteAssetPrecision'],
                i['baseCommissionPrecision'], i['quoteCommissionPrecision'],
                str(i['icebergAllowed']), str(i['ocoAllowed']),
                str(i['quoteOrderQtyMarketAllowed']),
                str(i['isSpotTradingAllowed']), str(i['isMarginTradingAllowed']),
                PRICE_FILTER_minPrice, PRICE_FILTER_maxPrice, PRICE_FILTER_tickSize, PERCENT_PRICE_multiplierUp,
                PERCENT_PRICE_multiplierDown, PERCENT_PRICE_avgPriceMins, LOT_SIZE_minQty,
                LOT_SIZE_maxQty, LOT_SIZE_stepSize, MIN_NOTIONAL_minNotional, str(MIN_NOTIONAL_applyToMarket),
                MIN_NOTIONAL_avgPriceMins, ICEBERG_PARTS_limit, MARKET_LOT_SIZE_minQty, MARKET_LOT_SIZE_maxQty,
                MARKET_LOT_SIZE_stepSize, MAX_NUM_ORDERS_maxNumOrders, MAX_NUM_ALGO_ORDERS_maxNumAlgoOrders)
        if cursor.execute("select count(*) from [Binance].[dbo].[PairSpecs] where symbol=(?)", symbol).fetchone()[
            0] == 0:
            print(
                f"{cursor.execute('select count(*) from [Binance].[dbo].[PairSpecs] where symbol=(?)', symbol).fetchone()[0]} adet var EKLEDİM {coin}")
            cursor.execute(
                "insert into [Binance].[dbo].[PairSpecs] Values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                coin)
        elif cursor.execute("select count(*) from [Binance].[dbo].[PairSpecs] where symbol=(?)", symbol).fetchone()[
            0] == 1:
            print(
                f"{cursor.execute('select count(*) from [Binance].[dbo].[PairSpecs] where symbol=(?)', symbol).fetchone()[0]} adet var GÜNCELLEDİM {coin}")
            a = list(coin)
            a.append(symbol)
            cursor.execute("update PairSpecs set symbol=(?), status=(?), baseAsset=(?), baseAssetPrecision=(?), "
                           "quoteAsset=(?), quotePrecision=(?), quoteAssetPrecision=(?), baseCommissionPrecision=(?), "
                           "quoteCommissionPrecision=(?), icebergAllowed=(?), ocoAllowed=(?), "
                           "quoteOrderQtyMarketAllowed=(?), isSpotTradingAllowed=(?), isMarginTradingAllowed=(?), "
                           "PRICE_FILTER_minPrice=(?), PRICE_FILTER_maxPrice=(?), PRICE_FILTER_tickSize=(?), "
                           "PERCENT_PRICE_multiplierUp=(?), PERCENT_PRICE_multiplierDown=(?), "
                           "PERCENT_PRICE_avgPriceMins=(?), LOT_SIZE_minQty=(?), LOT_SIZE_maxQty=(?), "
                           "LOT_SIZE_stepSize=(?), MIN_NOTIONAL_minNotional=(?), MIN_NOTIONAL_applyToMarket =(?), "
                           "MIN_NOTIONAL_avgPriceMins=(?), ICEBERG_PARTS_limit =(?), MARKET_LOT_SIZE_minQty =(?), "
                           "MARKET_LOT_SIZE_maxQty =(?), MARKET_LOT_SIZE_stepSize =(?), "
                           "MAX_NUM_ORDERS_maxNumOrders =(?), MAX_NUM_ALGO_ORDERS_maxNumAlgoOrders=(?) where symbol=(?)",
                           a)
        else:
            print(
                f"{cursor.execute('select count(*) from [Binance].[dbo].[PairSpecs] where symbol=(?)', symbol).fetchone()[0]} adet var HEPSİNİ SİLİP YENİ EKLEDİM {coin}")
            cursor.execute("delete from [Binance].[dbo].[PairSpecs]  where symbol=(?)", symbol)
            cursor.execute(
                "insert into [Binance].[dbo].[PairSpecs] Values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                coin)
    db.commit()
    print(time.perf_counter())


def get_klines(coinname, intervals_sql, intervals):
    cointime = time.time()
    print(f"{coinname} paritesinin {str(intervals_sql)} intervalleri taranacak...")
    intervals_binance = (
    Client.KLINE_INTERVAL_1MONTH, Client.KLINE_INTERVAL_1WEEK, Client.KLINE_INTERVAL_3DAY, Client.KLINE_INTERVAL_1DAY,
    Client.KLINE_INTERVAL_12HOUR, Client.KLINE_INTERVAL_8HOUR, Client.KLINE_INTERVAL_6HOUR, Client.KLINE_INTERVAL_4HOUR,
    Client.KLINE_INTERVAL_2HOUR, Client.KLINE_INTERVAL_1HOUR, Client.KLINE_INTERVAL_30MINUTE,
    Client.KLINE_INTERVAL_15MINUTE, Client.KLINE_INTERVAL_5MINUTE, Client.KLINE_INTERVAL_3MINUTE,
    Client.KLINE_INTERVAL_1MINUTE)
    for a in range(len(intervals_sql)):
        intervaltime = time.time()
        try:  # DB'de last timestamp varsa son eklenenden günümüze kadar alıcaz
            cursor.execute("select Open_time from dbo.last_timestamp((?), (?))", coinname, intervals_sql[a])
            last_timestamp = cursor.fetchone()[0]
            bars_since_last_log = client.get_historical_klines(coinname,
                                                               intervals_binance[intervals.index(intervals_sql[a])],
                                                               last_timestamp)[1:-1]
            for i in range(len(bars_since_last_log)):
                to_sql = (coinname, intervals_sql[a], 'Binance', bars_since_last_log[i][0], bars_since_last_log[i][1],
                          bars_since_last_log[i][2], bars_since_last_log[i][3], bars_since_last_log[i][4],
                          bars_since_last_log[i][5], bars_since_last_log[i][6], bars_since_last_log[i][7],
                          bars_since_last_log[i][8], bars_since_last_log[i][9], bars_since_last_log[i][10],
                          bars_since_last_log[i][11])
                cursor.execute(
                    "insert into [Binance].[dbo].[Klines] with (TABLOCK) Values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    to_sql)
                db.commit()
            print(
                f"{coinname} çiftinin {intervals_sql[a]} barlarının {pd.to_datetime(last_timestamp, unit='ms')} Tarihinden itibaren {len(bars_since_last_log)} Adet verisini SQL Klines Tablosuna {round(time.time() - intervaltime, 3)} Saniyede ekledim {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        except TypeError:  # DB'de last timestamp yoksa başlangıçtan itibaren alıcaz
            bars_since_listed = client.get_historical_klines(coinname, intervals_binance[a], 1225411200000)[
                                :-1]  # 31 Ekim 2008
            for bar in range(len(bars_since_listed)):
                to_sql = (coinname, intervals_sql[a], 'Binance', bars_since_listed[bar][0], bars_since_listed[bar][1],
                          bars_since_listed[bar][2], bars_since_listed[bar][3], bars_since_listed[bar][4],
                          bars_since_listed[bar][5], bars_since_listed[bar][6], bars_since_listed[bar][7],
                          bars_since_listed[bar][8], bars_since_listed[bar][9], bars_since_listed[bar][10],
                          bars_since_listed[bar][11])
                cursor.execute(
                    "insert into [Binance].[dbo].[Klines] with (TABLOCK) Values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    to_sql)
                db.commit()
            print(
                f"{coinname} çiftinin {intervals_sql[a]} barlarının başlangıç tarihinden itibaren {len(bars_since_listed)} Adet verisini SQL Klines Tablosuna {round(time.time() - intervaltime, 3)} Saniyede ekledim {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if round(time.time() - cointime, 3) > 3:
        print(
            f"{coinname} çiftinin {intervals_sql} Barları tarandı {round(time.time() - cointime, 3)} Saniye sürdü {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return 1



last_rendered_timestamps = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
if __name__ == '__main__':
    coin_update()
    cursor.execute("SELECT [symbol] FROM [Binance].[dbo].[PairSpecs] where status = 'TRADING' and (quoteAsset = 'USDT' or quoteAsset = 'BTC' or quoteAsset = 'BNB' or quoteAsset = 'ETH') and symbol not like ('%UPUSDT%')  and symbol not like ('%DOWNUSDT%') order by symbol")
    coinnames = tuple(map(lambda x: x[0], cursor.fetchall()))
    print(coinnames)
    for coinname in coinnames:  # while yapacaksan çok dikkatli ol bilgisayarı çökertme
        if coinnames.index(coinname) == 0:  # başa döndüğünü buradan anlıyoruz
            intervals = ('1MONTH', '1w', '3d', '1d', '12h', '8h', '6h', '4h', '2h', '1h', '30m', '15m', '5m', '3m', '1m')
            intervals_duration = (2678400, 604800, 259200, 86400, 43200, 28800, 21600, 14400, 7200, 3600, 1800, 900, 300, 180, 60)
            stamp_now = int(time.time())
            intervals_sql = []
            for i in range(len(intervals)):
                if stamp_now > last_rendered_timestamps[i] + intervals_duration[i]:  # last_rendered_timestamps[i] her işleme girdiğinde yeni değeri almalı
                    intervals_sql.append(intervals[i])
                    last_rendered_timestamps[i] = stamp_now

        get_klines(coinname, intervals_sql, intervals)
    print(time.perf_counter())

        # # Aynı anda kaç tane çekileceği belirlenerek çekme işlemi
        # def again(response_count = 0):
        #     time.sleep(60)
        #     if coinnames.index(coinname) - response_count < 2:    # aynı anda 2 tane çek
        #         response = multiprocessing.Process(target=get_klines, args=(coinname, intervals_sql, intervals)).start()
        #         if response == 1:
        #             response_count += 1
        #     else:
        #         again(response_count)
        # again()



        # İşlemci kullanımına göre çekme işlemi
        def again():
            time.sleep(60)
            print(f"CPU = {psutil.cpu_percent()} and RAM = {psutil.virtual_memory()[2]}")
            if float(psutil.cpu_percent()) < 20:
                multiprocessing.Process(target=get_klines, args=(coinname, intervals_sql, intervals)).start()
            else:
                again()
        again()

