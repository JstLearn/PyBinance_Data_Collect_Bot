cursor.execute("15 dklik sql sorgusu")
alınacaklar = tuple(map(lambda x: x[0], cursor.fetchall()))
BTC=0 USDT=0 ETH=0 BNB=0
for parite in alınacaklar
    if 'BTC' in parite:
        BTC+=1
    elif 'USDT' in parite:
        USDT+=1
    elif 'USDT' in parite:
        BNB+=1
    elif 'USDT' in parite:
        ETH+=1

if BTC>2
    BTC_activate_time= time.now() + 7200 # BTC paritesinin aktif olma saatini hesapladık
if USDT>2
    USDT_activate_time = time.now() + 7200  # USDT paritesinin aktif olma saatini hesapladık
if ETH > 2
    ETH_activate_time = time.now() + 7200  # ETH paritesinin aktif olma saatini hesapladık
if BNB > 2
    BNB_activate_time = time.now() + 7200  # BNB paritesinin aktif olma saatini hesapladık


if time.now() > BTC_activate_time
    # BTC paritesinin al sinyallerini borsaya iletebilirsin
if time.now() > USDT_activate_time
    # USDT paritesinin al sinyallerini borsaya iletebilirsin
if time.now() > ETH_activate_time
    # ETH paritesinin al sinyallerini borsaya iletebilirsin
if time.now() > BNB_activate_time
    # BNB paritesinin al sinyallerini borsaya iletebilirsin

