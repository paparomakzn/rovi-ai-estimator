from config import Config

print("="*50)
print("ПРОВЕРКА НАСТРОЕК РОВИКО")
print("="*50)
print(f"Компания: {Config.COMPANY_NAME}")
print(f"Телефон: {Config.COMPANY_PHONE}")
print(f"Email: {Config.COMPANY_EMAIL}")
print(f"Telegram токен: {'НЕ настроен' if Config.TELEGRAM_TOKEN == 'ВАШ_ТОКЕН_БОТА' else 'Настроен'}")
print("="*50)

input("Нажмите Enter для выхода...")