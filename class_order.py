import time
from dataclasses import dataclass

@dataclass
class Order:
    symbol: str = ""
    side: str = ""
    id: str = ""
    price: float = 0

    def exec_order(self, session):
        result = session.place_order(
            category="linear",
            symbol=self.symbol,
            side=self.side,
            orderType="Market",
            qty="100",
            marketUnit="quoteCoin"
        )
        self.id = result['result']['orderId']

        # Очікування появи ордера в open_orders
        for _ in range(10):  # максимум 10 спроб
            time.sleep(0.5)  # 0.5 секунди пауза
            open_orders = session.get_open_orders(category="linear", orderId=self.id)
            orders_list = open_orders.get('result', {}).get('list', [])
            if orders_list and orders_list[0].get('avgPrice'):
                self.price = float(orders_list[0]['avgPrice'])
                return self.id

        # Якщо після всіх спроб не вдалося отримати ціну
        raise Exception("Не вдалося отримати avgPrice для ордера")

    def reverse_side(self):
        if self.side == "Buy":
            self.side = "Sell"
        else:
            self.side = "Buy"