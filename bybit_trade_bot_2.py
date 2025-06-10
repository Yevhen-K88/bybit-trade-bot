from pybit.unified_trading import HTTP
from class_order import Order
from datetime import datetime
import time

pnl = 0
last_pnl = 0
cnt_orders = 0
open_price = 0
close_price = 0
candle = 0
sec = 0

# start parameters
max_orders = 20
target_profit = 10
timeframe = 15
start_symbol = "XRPUSDT"
start_side = "Buy"
leverage = "20"

order = Order(symbol=start_symbol, side=start_side)
trade_side = order.side

# Инициализация сессии с Bybit API
session = HTTP(
    demo=True,  # Используем тестовую сеть
    api_key="9QSa17CjQuFywUWTVz",  # Вставьте ваш API ключ
    api_secret="kXGIqHCeQk3XWjCkYIsScEfoDDharl5GAQO8",  # Вставьте ваш API секретный ключ
)
try:
    session.set_leverage(
        category="linear",
        symbol=start_symbol,
        buyLeverage=leverage,
        sellLeverage=leverage,
    )
except Exception as e:
    print("Ошибка:", e)

try:
    response = session.get_wallet_balance(accountType="UNIFIED", coin="USDT")
    wallet_balance = response['result']['list'][0]['coin'][0]['walletBalance']
    print("Баланс:", wallet_balance)
    while pnl<target_profit and cnt_orders < max_orders+1:
        if open_price!=0:
            candle = ((close_price-open_price)/open_price)*100
        print("Candle ", candle)
        if candle > 0.01 and trade_side == "Buy":
            order.reverse_side()
        if candle < -0.01 and trade_side == "Sell":
            order.reverse_side()
        while True:
            now = datetime.now()
            # if now.second == 1 and now.minute % timeframe == 0:
            if now.minute % timeframe == 0:
                print(datetime.now(), " ", end='')
                order.exec_order(session)
                sec = datetime.now().second
                print(order)
                trade_side = order.side
                open_price = order.price
                break  # Завершаем цикл после выполнения ордера
            time.sleep(1)

        order.reverse_side()
        time.sleep(timeframe*60-3-sec)
        print(datetime.now(), " ", end='')
        order.exec_order(session)
        print(order)
        close_price = order.price
        closed_pnl = []
        while not closed_pnl:
            closed_pnl = session.get_closed_pnl(
                category="linear",
                symbol=order.symbol,
                startTime = int(time.time() * 1000) - 10000
            )["result"]["list"]
        last_pnl = float(closed_pnl[0]["closedPnl"])
        pnl += last_pnl
        cnt_orders += 1
        print(f"Last PNL: {str(last_pnl)}")
        print(f"PNL: {str(pnl)}")

except Exception as e:
    print("Ошибка:", e)
