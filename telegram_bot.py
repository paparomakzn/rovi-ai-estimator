import os
import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import Config

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class RovikoBot:
    def __init__(self):
        self.token = Config.TELEGRAM_TOKEN
        self.company_name = Config.COMPANY_NAME
        self.logger = logging.getLogger(__name__)
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user = update.effective_user
        self.logger.info(f"Пользователь {user.id} запустил бота")
        
        welcome_text = f"""🏗️ Добро пожаловать в {self.company_name}!

Я - ИИ-помощник для расчета строительных смет.

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
        self.logger.info(f"Отправлено приветствие пользователю {user.id}")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /help"""
        help_text = """📚 **Помощь по использованию:**

1. **Подготовьте чертеж** помещения
2. **Загрузите файл** в этот чат
3. **Добавьте описание**, например:
   • "Покраска стен в гостиной"
   • "Укладка плитки в ванной 10м²"
   • "Отделка потолка"

📞 **Техподдержка:** {Config.COMPANY_PHONE}

🛠 **Поддерживаемые форматы:**
PNG, JPG, PDF, DXF

📏 **Макс. размер:** {Config.MAX_FILE_SIZE/(1024*1024):.0f}MB""".format(Config=Config)
        
        await update.message.reply_text(help_text)
    
    async def echo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Простой ответ на текстовые сообщения"""
        user_message = update.message.text
        self.logger.info(f"Сообщение от {update.effective_user.id}: {user_message}")
        
        response = f"📝 Получил ваше сообщение: \"{user_message}\"\n\n"
        response += "Для расчета сметы загрузите чертеж с описанием работы."
        
        await update.message.reply_text(response)
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик ошибок"""
        self.logger.error(f"Ошибка: {context.error}")
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ Произошла ошибка. Пожалуйста, попробуйте позже."
            )
    
    def run(self):
        """Запуск бота"""
        # Проверка токена
        if self.token == 'ВАШ_ТОКЕН_БОТА' or 'ВАШ_ТОКЕН_БОТА' in self.token:
            print("❌ ОШИБКА: Токен Telegram не настроен!")
            print("Получите токен у @BotFather и вставьте в config.py")
            input("Нажмите Enter для выхода...")
            return
        
        print("="*60)
        print(f"🏗️  ЗАПУСК БОТА ДЛЯ КОМПАНИИ: {self.company_name}")
        print(f"📞 Контакты: {Config.COMPANY_PHONE}")
        print("="*60)
        print("\n🤖 Инициализация бота...")
        
        try:
            # Создание приложения
            application = Application.builder().token(self.token).build()
            
            # Регистрация обработчиков
            application.add_handler(CommandHandler("start", self.start))
            application.add_handler(CommandHandler("help", self.help_command))
            application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.echo))
            
            # Обработчик ошибок
            application.add_error_handler(self.error_handler)
            
            print("✅ Бот инициализирован")
            print("🔄 Запускаю опрос сообщений...")
            print("⚠️  Для остановки нажмите Ctrl+C")
            print("\n" + "="*60)
            
            # Запуск бота
            application.run_polling(allowed_updates=Update.ALL_TYPES)
            
        except Exception as e:
            print(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
            input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    bot = RovikoBot()
    bot.run()