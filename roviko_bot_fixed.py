#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ИСПРАВЛЕННЫЙ БОТ ДЛЯ РОВИКО - Работает на Windows
"""

import os
import sys
import asyncio
import logging
from typing import Optional

# Настройка logging перед всем остальным
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('roviko_bot.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# Импорты должны быть после настройки logging
try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
    import telegram.error
except ImportError as e:
    logger.error(f"Ошибка импорта: {e}")
    print("❌ Библиотеки не установлены!")
    print("Выполните: pip install -r requirements.txt")
    sys.exit(1)

# Импорт конфигурации
try:
    from config import Config
except ImportError:
    print("❌ Не найден config.py!")
    sys.exit(1)

class RovikoBot:
    def __init__(self):
        self.token = Config.TELEGRAM_TOKEN
        self.company_name = Config.COMPANY_NAME
        
        # Проверка токена
        if self.token == 'ВАШ_ТОКЕН_БОТА' or 'ВАШ_ТОКЕН_БОТА' in self.token:
            logger.error("Токен не настроен!")
            raise ValueError("Токен Telegram не настроен в config.py")
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user = update.effective_user
        logger.info(f"Пользователь {user.id} ({user.username}) запустил бота")
        
        welcome_text = f"""🏗️ Добро пожаловать в {self.company_name}!

🤖 Я - ИИ-помощник для расчета строительных смет.

📋 **Как использовать:**
1. Загрузите чертеж (PNG, JPG, PDF)
2. В подписи укажите задание

📝 **Примеры:**
• "Рассчитай покраску стен 20м²"
• "Смета на укладку плитки в ванной"
• "Отделка потолка в спальне"

📞 **Контакты:**
{Config.COMPANY_PHONE}
{Config.COMPANY_EMAIL}"""
        
        await update.message.reply_text(welcome_text)
        logger.info(f"Отправлено приветствие пользователю {user.id}")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /help"""
        help_text = f"""📚 **Помощь по использованию:**

1. **Подготовьте чертеж** помещения
2. **Загрузите файл** в этот чат
3. **Добавьте описание**, например:
   • "Покраска стен в гостиной"
   • "Укладка плитки в ванной 10м²"
   • "Отделка потолка"

📞 **Техподдержка:** {Config.COMPANY_PHONE}

🛠 **Поддерживаемые форматы:**
PNG, JPG, PDF, DXF

📏 **Макс. размер:** {Config.MAX_FILE_SIZE/(1024*1024):.0f}MB"""
        
        await update.message.reply_text(help_text)
    
    async def echo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Простой ответ на текстовые сообщения"""
        user_message = update.message.text
        user = update.effective_user
        
        logger.info(f"Сообщение от {user.id}: {user_message[:50]}...")
        
        response = f"📝 Получил: \"{user_message}\"\n\n"
        response += "Для расчета сметы загрузите чертеж с описанием работы.\n"
        response += "Используйте /help для инструкций."
        
        await update.message.reply_text(response)
    
    async def error_handler(self, update: Optional[Update], context: ContextTypes.DEFAULT_TYPE):
        """Обработчик ошибок"""
        logger.error(f"Ошибка в обработчике: {context.error}", exc_info=context.error)
        
        if update and update.effective_message:
            try:
                await update.effective_message.reply_text(
                    "❌ Произошла ошибка. Пожалуйста, попробуйте позже или напишите /start"
                )
            except:
                pass
    
    def create_application(self):
        """Создание и настройка приложения"""
        try:
            # Создаем приложение с настройками для Windows
            application = Application.builder() \
                .token(self.token) \
                .connect_timeout(30.0) \
                .read_timeout(30.0) \
                .write_timeout(30.0) \
                .pool_timeout(30.0) \
                .build()
            
            # Добавляем обработчики
            application.add_handler(CommandHandler("start", self.start))
            application.add_handler(CommandHandler("help", self.help_command))
            application.add_handler(CommandHandler("test", self.start))
            application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.echo))
            
            # Обработчик ошибок
            application.add_error_handler(self.error_handler)
            
            return application
            
        except Exception as e:
            logger.error(f"Ошибка создания приложения: {e}")
            raise
    
    def run(self):
        """Запуск бота"""
        print("="*70)
        print(f"🏗️  ЗАПУСК БОТА ДЛЯ КОМПАНИИ: {self.company_name}")
        print(f"📞 Контакты: {Config.COMPANY_PHONE}")
        print(f"📧 Email: {Config.COMPANY_EMAIL}")
        print("="*70)
        print("\n🤖 Инициализация бота...")
        
        try:
            # Создаем приложение
            application = self.create_application()
            
            print("✅ Приложение создано")
            print("🔗 Получаю информацию о боте...")
            
            # Пробуем получить информацию о боте
            async def get_bot_info():
                bot_info = await application.bot.get_me()
                return bot_info
            
            bot_info = asyncio.run(get_bot_info())
            print(f"✅ Бот: {bot_info.first_name} (@{bot_info.username})")
            print(f"🔗 Ссылка: https://t.me/{bot_info.username}")
            
            print("\n🔄 Запускаю опрос сообщений...")
            print("⚠️  Для остановки нажмите Ctrl+C")
            print("\n" + "="*70)
            print("📱 Теперь откройте Telegram и напишите боту /start")
            print("="*70)
            
            # Запускаем бота
            application.run_polling(
                drop_pending_updates=True,
                allowed_updates=Update.ALL_TYPES,
                close_loop=False
            )
            
        except telegram.error.InvalidToken:
            print("\n❌ НЕВЕРНЫЙ ТОКЕН!")
            print("Проверьте токен в config.py")
            print("Получите новый токен у @BotFather")
            
        except telegram.error.NetworkError as e:
            print(f"\n❌ ОШИБКА СЕТИ: {e}")
            print("Проверьте интернет-подключение")
            print("Если в России - возможно нужен VPN")
            
        except Exception as e:
            print(f"\n❌ КРИТИЧЕСКАЯ ОШИБКА: {type(e).__name__}")
            print(f"Сообщение: {e}")
            logger.exception("Критическая ошибка")
            
        finally:
            print("\n" + "="*70)
            print("Бот остановлен")
            input("Нажмите Enter для выхода...")

def main():
    """Главная функция"""
    try:
        bot = RovikoBot()
        bot.run()
    except ValueError as e:
        print(f"\n❌ {e}")
        print("Откройте config.py и вставьте токен от @BotFather")
        input("Нажмите Enter для выхода...")
    except KeyboardInterrupt:
        print("\n\n👋 Бот остановлен пользователем")
    except Exception as e:
        print(f"\n❌ Неожиданная ошибка: {e}")
        input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    # Для Windows важно правильно настроить asyncio
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    main()