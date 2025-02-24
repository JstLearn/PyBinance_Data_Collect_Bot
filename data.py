Pkey = 'CoYR3M8blHJsyJWiNgKP3c5qf9JKNWoPtKjbA8Y4F8ssyiMVFG0wfwcYI2LwRdxA'
Skey = 'PJNsEcIIIX1A8g3AnxCQljocj62k4R2SYjf0eE5cQfhNs18WqMymu0mUDs50talv'

# -----------------GLOBAL DEĞİŞKENLER--------------------

fapi = "https://fapi.binance.com/fapi/v1/"
api0 = "https://api.binance.com"
api1 = "https://api1.binance.com"
api2 = "https://api2.binance.com"
api3 = "https://api3.binance.com"

# toplu veri çekilebilir
api24hr = api0 + "/api/v3/ticker/24hr"
Price = api0 + "/api/v3/ticker/price"
bookticker = api0 + "/api/v3/ticker/bookTicker"

# hem toplu hem sembol ile çekilebilir
exchange_info = api0 + "/api/v3/exchangeInfo"  # ?symbol=BNBBTC
symbol_book = api0 + "/api/v3/depth"  # ?symbol=BNBBTC&limit=1000

# sembol vererek sorulacaklar
order_book = api0 + "/api/v3/depth"
klines = api0 + "/api/v3/klines"


# print(client.get_asset_balance('BTC'))


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