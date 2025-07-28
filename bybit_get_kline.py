from time import process_time

from pybit.unified_trading import HTTP
import pandas as pd
import keys
import math

session = HTTP(
    demo=True,  # Используем тестовую сеть
    api_key=keys.API_KEY_1,  # Вставьте ваш API ключ
    api_secret=keys.API_SECRET_1,  # Вставьте ваш API секретный ключ
)

klines = session.get_kline(
    category="linear",      # Для USDT-контрактів
    symbol="SOLUSDT",       # Символ
    interval="60",          # Таймфрейм: "1", "3", "5", "15", "30", "60", "240", "D", "W", "M"
    limit=200               # Максимум 200 (за запит)
)['result']['list']

# Формуємо DataFrame
df = pd.DataFrame(klines, columns=[
    "timestamp", "open", "high", "low", "close", "volume", "turnover"
])

# Приведення типів
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
for col in ["open", "high", "low", "close", "volume", "turnover"]:
    df[col] = df[col].astype(float)

# Ставимо timestamp як індекс
df.set_index("timestamp", inplace=True)

df["pct_change"] = abs(((df["close"] - df["open"]) / df["open"]) * 100)

df["candle_type"] = "doji"
df.loc[df["close"]>df["open"],"candle_type"] = "buy"
df.loc[df["close"]<df["open"],"candle_type"] = "sell"

change = (df["candle_type"]!=df["candle_type"].shift(1)).sum()
df["type_changed"] = df["candle_type"] != df["candle_type"].shift(1)
total_change_on_switch = df.loc[df["type_changed"], "pct_change"].sum()
total_change_without_switch = df.loc[~df["type_changed"], "pct_change"].sum()

print(f"Сума % змін у свічках, де змінився тип: {total_change_on_switch:.2f}%")
print(f"Сума % змін у свічках, де не змінився тип: {total_change_without_switch:.2f}%")

no_change = (df["candle_type"]==df["candle_type"].shift(1)).sum()

print(f"change {change}")
print(f"no_change {no_change}")

#print(df.tail())
#print(df.head())
