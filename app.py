import os
import threading
from flask import Flask
from telegram_bot import RovikoBot  # Импортируем нашего бота

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Roviko Telegram Bot is running"

def run_bot():
    """Запуск Telegram бота в отдельном потоке"""
    bot = RovikoBot()
    bot.run()

if __name__ == "__main__":
    # Запускаем бота в фоновом потоке
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    # Запускаем Flask-сервер на порту, который даст Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
