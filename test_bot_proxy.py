import requests
from config import Config

def test_with_proxy():
    print("Тест бота через прокси...")
    
    token = Config.TELEGRAM_TOKEN
    
    # Попробуйте разные прокси (если нужно)
    proxies = {
        'http': 'http://proxy.example.com:8080',
        'https': 'http://proxy.example.com:8080',
    }
    
    try:
        # Без прокси сначала
        print("Попытка без прокси...")
        response = requests.get(f"https://api.telegram.org/bot{token}/getMe", timeout=10)
        print(f"Успешно! Статус: {response.status_code}")
        
    except:
        print("Без прокси не получилось, пробую с прокси...")
        # Здесь нужно будет настроить реальный прокси
        
    input("Нажмите Enter...")