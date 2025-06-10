import ntplib
from time import ctime
from pybit.unified_trading import HTTP
from dataclasses import dataclass
from datetime import datetime
import time

@dataclass
class Order:
    symbol: str = ""
    side: str = ""

pnl = 0
last_pnl = 0

# start parameters
start_symbol = "ETHUSDT"
start_side = "Buy"

order = Order(symbol=start_symbol, side=start_side)

# Получаем точное время с сервера NTP
def get_ntp_time():
    c = ntplib.NTPClient()
    response = c.request('time.google.com')
    return response.tx_time  # Время в формате UTC

def open_order(ord: Order):
    return session.place_order(
        category="linear",
        symbol=ord.symbol,
        side=ord.side,
        orderType="Market",
        qty="0.05",
        marketUnit="quoteCoin"
    )

# Синхронизация времени
ntp_time = get_ntp_time()
print("Точное время с NTP сервера:", ctime(ntp_time))

# Инициализация сессии с Bybit API
session = HTTP(
    demo=True,  # Используем тестовую сеть
    api_key="9QSa17CjQuFywUWTVz",  # Вставьте ваш API ключ
    api_secret="kXGIqHCeQk3XWjCkYIsScEfoDDharl5GAQO8",  # Вставьте ваш API секретный ключ
)

try:
    response = session.get_wallet_balance(accountType="UNIFIED", coin="USDT")
    wallet_balance = response['result']['list'][0]['coin'][0]['walletBalance']
    print("Баланс:", wallet_balance)
    while True:
        now = datetime.now()
        if now.second == 00 and now.minute in {00, 15, 30, 45}:
            print(datetime.now())
            print(open_order(order))
            break  # Завершаем цикл после выполнения ордера
        time.sleep(1)

    order.side = "Sell" if order.side == "Buy" else "Buy"
    time.sleep(15*60-1)
    print(datetime.now())
    print(open_order(order))
    time.sleep(1)
    closed_pnl = session.get_closed_pnl(
        category="linear",
        symbol=order.symbol,
        startTime = int(time.time() * 1000) - 10000
    )["result"]["list"]
    print(closed_pnl[0]["closedPnl"])

except Exception as e:
    print("Ошибка:", e)
