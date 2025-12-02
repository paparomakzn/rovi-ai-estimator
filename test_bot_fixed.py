import requests
import socket
from config import Config

def check_internet():
    """Проверка интернет-подключения"""
    try:
        # Попытка подключения к DNS Google
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def test_bot_with_timeout():
    print("="*60)
    print("🌐 РАСШИРЕННЫЙ ТЕСТ ПОДКЛЮЧЕНИЯ РОВИКО")
    print("="*60)
    
    # Проверка интернета
    print("\n1. 🔌 ПРОВЕРКА ИНТЕРНЕТ-ПОДКЛЮЧЕНИЯ:")
    if check_internet():
        print("   ✅ Интернет доступен")
    else:
        print("   ❌ Нет интернет-подключения")
        print("   • Проверьте Wi-Fi/кабель")
        print("   • Отключите VPN/антивирус")
        return
    
    # Получаем токен
    token = Config.TELEGRAM_TOKEN
    
    print(f"\n2. 🔑 ТОКЕН TELEGRAM:")
    print(f"   Длина: {len(token)} символов")
    print(f"   Формат: {'✅ Правильный' if ':' in token else '❌ Неправильный'}")
    
    if ':' in token:
        bot_id = token.split(':')[0]
        print(f"   ID бота: {bot_id}")
        print(f"   Ссылка: https://t.me/{bot_id}")
    
    print("\n3. 🌐 ПРОВЕРКА ПОДКЛЮЧЕНИЯ К TELEGRAM...")
    
    try:
        # URL для проверки
        url = f"https://api.telegram.org/bot{token}/getMe"
        
        # Увеличенный таймаут - 30 секунд
        print("   Жду ответа от Telegram (30 сек)...")
        response = requests.get(url, timeout=30)
        
        print(f"\n   📡 Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_info = data['result']
                print("\n   🎉 БОТ РАБОТАЕТ!")
                print("   " + "="*50)
                print(f"   🤖 Имя: {bot_info['first_name']}")
                print(f"   👤 @{bot_info['username']}")
                print(f"   🔗 t.me/{bot_info['username']}")
                
                # Сохраняем информацию о боте
                with open('bot_info.txt', 'w') as f:
                    f.write(f"Бот: {bot_info['first_name']}\n")
                    f.write(f"Username: @{bot_info['username']}\n")
                    f.write(f"ID: {bot_info['id']}\n")
                    f.write(f"Ссылка: https://t.me/{bot_info['username']}\n")
                
                print("\n   📝 Информация сохранена в bot_info.txt")
                
            else:
                print(f"\n   ❌ Ошибка Telegram: {data}")
                
        elif response.status_code == 404:
            print("\n   ❌ Бот не найден (неверный токен)")
            print("   • Проверьте токен")
            print("   • Пересоздайте бота у @BotFather")
            
        elif response.status_code == 401:
            print("\n   ❌ Неавторизованный доступ (неверный токен)")
            
        else:
            print(f"\n   ❌ Неожиданный статус: {response.status_code}")
            print(f"   Текст ответа: {response.text[:100]}...")
            
    except requests.exceptions.Timeout:
        print("\n   ❌ ТАЙМАУТ ПОДКЛЮЧЕНИЯ")
        print("   Возможные причины:")
        print("   1. Блокировка Telegram в России")
        print("   2. Проблемы с прокси/антивирусом")
        print("   3. Очень медленный интернет")
        
    except requests.exceptions.ConnectionError:
        print("\n   ❌ ОШИБКА ПОДКЛЮЧЕНИЯ")
        print("   Telegram API недоступен")
        print("   Попробуйте использовать VPN")
        
    except Exception as e:
        print(f"\n   ❌ ОШИБКА: {type(e).__name__}")
        print(f"   {e}")
    
    print("\n" + "="*60)
    print("📞 Контакты для поддержки:")
    print(f"Телефон: {Config.COMPANY_PHONE}")
    print(f"Email: {Config.COMPANY_EMAIL}")
    print("="*60)

if __name__ == "__main__":
    test_bot_with_timeout()
    input("\nНажмите Enter для выхода...")