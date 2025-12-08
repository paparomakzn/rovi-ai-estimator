import os
import sys
import multiprocessing
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Roviko Telegram Bot is running"

def run_bot():
    """Запуск Telegram бота в отдельном процессе"""
    # Добавляем путь для импорта
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from telegram_bot import RovikoBot
    bot = RovikoBot()
    bot.run()

if __name__ == "__main__":
    # Запускаем бота в отдельном процессе
    bot_process = multiprocessing.Process(target=run_bot, daemon=True)
    bot_process.start()
    # Запускаем Flask-сервер на порту, который даст Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, use_reloader=False)  # use_reloader=False важно!
