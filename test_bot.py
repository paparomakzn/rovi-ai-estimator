import requests
from config import Config

def test_bot():
    print("="*50)
    print("🤖 ТЕСТИРОВАНИЕ TELEGRAM БОТА РОВИКО")
    print("="*50)
    
    # Получаем токен из config.py
    token = Config.TELEGRAM_TOKEN
    
    # Проверяем, что токен не стандартный
    if token == 'ВАШ_ТОКЕН_БОТА' or 'ВАШ_ТОКЕН_БОТА' in token:
        print("❌ ТОКЕН НЕ НАСТРОЕН!")
        print("\nЧто делать:")
        print("1. Откройте Telegram")
        print("2. Найдите @BotFather")
        print("3. Создайте бота: /newbot")
        print("4. Скопируйте токен")
        print("5. Вставьте токен в config.py")
        return
    
    print(f"🔑 Токен получен: {token[:15]}...")
    print("🔧 Проверяю подключение к Telegram API...")
    
    try:
        # URL для проверки бота
        url = f"https://api.telegram.org/bot{token}/getMe"
        
        # Отправляем запрос
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('ok'):
                bot_info = data['result']
                print("\n✅ БОТ РАБОТАЕТ КОРРЕКТНО!")
                print("="*50)
                print(f"🤖 Имя бота: {bot_info['first_name']}")
                print(f"👤 Username: @{bot_info['username']}")
                print(f"🔗 Ссылка: https://t.me/{bot_info['username']}")
                print(f"🆔 ID бота: {bot_info['id']}")
                
                # Проверка admin chat id
                if Config.ADMIN_CHAT_ID and Config.ADMIN_CHAT_ID != '':
                    print(f"👑 Admin Chat ID: {Config.ADMIN_CHAT_ID}")
                else:
                    print("⚠️  Admin Chat ID не настроен")
                
                print("="*50)
                print("\n🎉 ВСЕ НАСТРОЙКИ КОРРЕКТНЫ!")
                print("Бот готов к работе!")
                
            else:
                print(f"❌ Ошибка в ответе Telegram: {data}")
                
        else:
            print(f"❌ Ошибка HTTP: {response.status_code}")
            print(f"📋 Ответ: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Таймаут подключения к Telegram")
        print("Проверьте интернет-соединение")
        
    except requests.exceptions.ConnectionError:
        print("❌ Ошибка подключения")
        print("Проверьте интернет-соединение")
        
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {type(e).__name__}: {e}")

if __name__ == "__main__":
    test_bot()
    input("\nНажмите Enter для выхода...")