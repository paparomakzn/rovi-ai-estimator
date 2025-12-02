# simple_test.py - Простой тест без requests
from config import Config

print("="*50)
print("🤖 ПРОСТОЙ ТЕСТ TELEGRAM БОТА РОВИКО")
print("="*50)

# Получаем токен
token = Config.TELEGRAM_TOKEN

print(f"🔑 Токен из config.py: {token}")

if token == 'ВАШ_ТОКЕН_БОТА' or 'ВАШ_ТОКЕН_БОТА' in token:
    print("\n❌ ТОКЕН НЕ НАСТРОЕН!")
    print("\nТекущий токен: стандартный шаблон")
    print("Нужно получить реальный токен у @BotFather")
else:
    print("\n✅ ТОКЕН НАСТРОЕН!")
    print(f"Длина токена: {len(token)} символов")
    print(f"Первые 15 символов: {token[:15]}...")
    
    # Проверяем формат токена
    if ':' in token:
        print("✅ Формат токена правильный (содержит ':')")
        bot_id = token.split(':')[0]
        print(f"🆔 ID бота: {bot_id}")
        print(f"🔗 Ссылка на бота: https://t.me/{bot_id}")
    else:
        print("⚠️  Возможно неверный формат токена")

# Проверка admin chat id
if Config.ADMIN_CHAT_ID and Config.ADMIN_CHAT_ID != '':
    print(f"\n👑 Admin Chat ID: {Config.ADMIN_CHAT_ID}")
else:
    print("\n⚠️  Admin Chat ID не настроен")

print("\n" + "="*50)
print("📞 Контакты компании:")
print(f"Телефон: {Config.COMPANY_PHONE}")
print(f"Email: {Config.COMPANY_EMAIL}")
print("="*50)

input("\nНажмите Enter для выхода...")