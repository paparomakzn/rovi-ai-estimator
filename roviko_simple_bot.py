#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
УЛЬТРА-ПРОСТОЙ БОТ РОВИКО - Работает без ошибок!
"""

import json
import time
import urllib.request
import urllib.error
from datetime import datetime

# Конфигурация
CONFIG = {
    'company_name': 'РОВИКО',
    'phone': '+7 (905) 316-05-02',
    'email': 'ars382@mail.ru',
    'token': '8213818961:AAHmvsTLva7shePtE5-NtKzob7vofaGp8Pc',  # Ваш токен
    'admin_id': ''
}

class SimpleBot:
    def __init__(self, token):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.last_update_id = 0
        self.running = True
        
        print("="*60)
        print(f"🏗️  БОТ ДЛЯ КОМПАНИИ: {CONFIG['company_name']}")
        print(f"📞 Контакты: {CONFIG['phone']}")
        print("="*60)
    
    def make_request(self, method, data=None):
        """Выполнить HTTP запрос"""
        url = f"{self.base_url}/{method}"
        
        try:
            if data:
                json_data = json.dumps(data).encode('utf-8')
                req = urllib.request.Request(
                    url,
                    data=json_data,
                    headers={'Content-Type': 'application/json'}
                )
            else:
                req = urllib.request.Request(url)
            
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode('utf-8'))
                
        except Exception as e:
            print(f"⚠️  Ошибка запроса: {e}")
            return None
    
    def get_me(self):
        """Получить информацию о боте"""
        print("🔧 Подключаюсь к Telegram...")
        result = self.make_request('getMe')
        
        if result and result.get('ok'):
            bot_info = result['result']
            print(f"✅ Бот: {bot_info['first_name']}")
            print(f"🔗 @{bot_info['username']}")
            print(f"🆔 ID: {bot_info['id']}")
            return bot_info
        return None
    
    def get_updates(self):
        """Получить новые сообщения"""
        params = {
            'offset': self.last_update_id + 1,
            'timeout': 10
        }
        
        param_str = '&'.join([f"{k}={v}" for k, v in params.items()])
        url = f"{self.base_url}/getUpdates?{param_str}"
        
        try:
            with urllib.request.urlopen(url, timeout=35) as response:
                data = json.loads(response.read().decode('utf-8'))
                if data.get('ok'):
                    return data['result']
        except:
            pass
        return []
    
    def send_message(self, chat_id, text):
        """Отправить сообщение"""
        data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        result = self.make_request('sendMessage', data)
        return result and result.get('ok', False)
    
    def handle_message(self, message):
        """Обработать сообщение"""
        chat_id = message['chat']['id']
        text = message.get('text', '')
        user = message.get('from', {})
        username = user.get('username', 'Гость')
        
        print(f"📥 {username}: {text}")
        
        if text.startswith('/start'):
            response = f"""🏗️ Добро пожаловать в {CONFIG['company_name']}!

🤖 Я - ИИ-помощник для расчета строительных смет.

📋 **Как использовать:**
1. Загрузите чертеж (PNG, JPG, PDF)
2. В подписи укажите задание

📝 **Примеры:**
• "Рассчитай покраску стен 20м²"
• "Смета на укладку плитки"
• "Отделка потолка"

📞 **Контакты:**
{CONFIG['phone']}
{CONFIG['email']}

ℹ️ /help - помощь
📊 /status - статус"""
            
        elif text.startswith('/help'):
            response = """📚 **Помощь:**

1. **Подготовьте чертеж**
2. **Загрузите в этот чат**
3. **Добавьте описание**

🛠 **Форматы:** PNG, JPG, PDF
📏 **Размер:** до 20MB

📞 **Поддержка:** {phone}""".format(phone=CONFIG['phone'])
            
        elif text.startswith('/status'):
            response = f"""📊 **Статус:**

✅ Бот работает
🏢 {CONFIG['company_name']}
📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}
👤 Ваш ID: {chat_id}"""
            
        elif text.strip():
            response = f"""📝 Получил: "{text}"

ℹ️ Для расчета сметы загрузите чертеж.
Используйте /help для инструкций."""
            
        else:
            response = "Напишите /start для начала"
        
        self.send_message(chat_id, response)
    
    def run(self):
        """Запустить бота"""
        # Проверяем подключение
        bot_info = self.get_me()
        if not bot_info:
            print("❌ Не удалось подключиться")
            return
        
        print(f"\n🔗 Ссылка: https://t.me/{bot_info['username']}")
        print("\n🤖 Бот запущен!")
        print("🔄 Проверяю сообщения...")
        print("⚠️  Ctrl+C для остановки")
        print("\n📱 Напишите /start в Telegram")
        print("="*60)
        
        try:
            while self.running:
                updates = self.get_updates()
                
                for update in updates:
                    if 'update_id' in update:
                        self.last_update_id = update['update_id']
                    
                    if 'message' in update:
                        self.handle_message(update['message'])
                
                time.sleep(2)  # Ждем 2 секунды
                
        except KeyboardInterrupt:
            print("\n\n👋 Остановка...")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
        
        print(f"\n🏁 Бот остановлен")

def main():
    """Главная функция"""
    token = CONFIG['token']
    
    if not token or 'ВАШ_ТОКЕН' in token:
        print("❌ Вставьте токен в код!")
        return
    
    bot = SimpleBot(token)
    bot.run()
    
    input("\nНажмите Enter...")

if __name__ == "__main__":
    main()