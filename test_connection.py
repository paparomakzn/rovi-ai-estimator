# test_connection.py - Простой тест подключения
import asyncio
import sys
from config import Config

async def simple_test():
    print("🔧 Тест подключения к Telegram...")
    
    token = Config.TELEGRAM_TOKEN
    
    if token == 'ВАШ_ТОКЕН_БОТА':
        print("❌ Токен не настроен")
        return
    
    print(f"Токен: {token[:15]}...")
    
    try:
        # Пробуем импортировать библиотеку
        from telegram import Bot
        
        bot = Bot(token=token)
        info = await bot.get_me()
        
        print(f"✅ Успех! Бот: {info.first_name}")
        print(f"🔗 @{info.username}")
        print(f"🆔 ID: {info.id}")
        
    except ImportError:
        print("❌ Библиотека 'python-telegram-bot' не установлена")
        print("Выполните: pip install python-telegram-bot==20.3")
    except Exception as e:
        print(f"❌ Ошибка: {type(e).__name__}: {e}")

if __name__ == "__main__":
    # Важно для Windows
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(simple_test())
    input("\nНажмите Enter...")