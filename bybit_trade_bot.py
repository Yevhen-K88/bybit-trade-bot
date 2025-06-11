from telethon import TelegramClient, events
from telegram import Bot
import asyncio
import keys

# Данные вашего бота и API
API_ID = keys.API_ID
API_HASH = keys.API_HASH
CHAT_ID = keys.CHAT_ID
BOT_TOKEN = keys.BOT_TOKEN
SOURCE_CHANNEL = keys.SOURCE_CHANNEL

# Инициализация клиентов
client = TelegramClient('session_name', API_ID, API_HASH)
bot = Bot(token=BOT_TOKEN)

# Функция обработки сообщений из канала
@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
# @client.on(events.NewMessage())
async def handler(event):
    chat = await event.get_chat()
    sender = await event.get_sender()
    print("1111")
    message = event.message.message  # Получение текста сообщения
    try:
        print(f"Нове повідомлення в ({chat.id}): {message}")
        print(f"Відправник: {sender.username if sender.username else sender.id}")
        # Пересылка сообщения в ваш бот
        # await client.send_message(entity=CHAT_ID, message=message)
        # if chat_id != 6608004828:
        #     await bot.send_message(chat_id=CHAT_ID, text=str(chat_id)+" "+message)
    except Exception as e:
        print(f"Ошибка отправки сообщения: {e}")

async def send_message_to_user():
    try:
        # Отправка сообщения
        await bot.send_message(chat_id=CHAT_ID, text="Привет! Это тестовое сообщение от бота.")
        print("Сообщение успешно отправлено!")
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")

# Основная функция запуска
async def main():
    print("Бот запущен...")
    async with client:
        await send_message_to_user()
        await client.run_until_disconnected()

# Запуск программы
if __name__ == "__main__":
    asyncio.run(main())
