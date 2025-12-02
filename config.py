# config.py - Настройки для компании РОВИКО
import os

class Config:
    # Данные компании
    COMPANY_NAME = "РОВИКО"
    LEGAL_ENTITY = "ИП Арестов Роман Сергеевич"
    COMPANY_PHONE = "+7 (905) 316-05-02"  # Замените на ваш телефон
    COMPANY_EMAIL = "ars382@mail.ru"
    COMPANY_WEBSITE = "spkd116.ru"
    
    # Telegram настройки
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '8213818961:AAHmvsTLva7shePtE5-NtKzob7vofaGp8Pc')
    ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID', '302358685')
    
    # Реквизиты
    COMPANY_REQUISITES = "ИП Арестов Р.С. | ИНН 165916166325 | ОГРНИП 319169000097071"
    
    # Настройки обработки файлов
    MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB
    SUPPORTED_FORMATS = ['.png', '.jpg', '.jpeg', '.pdf', '.dxf']
    
    # Цены для расчетов (руб/м²)
    PRICES = {
        'wall_painting': 350,    # Покраска стен
        'tiling': 1200,          # Укладка плитки
        'wallpaper': 450,        # Оклейка обоями
        'plaster': 550,          # Штукатурка
        'drywall': 850,          # Гипсокартон
    }
    
    # Настройки компании
    WORK_TYPES = {
        'wall_painting': 'Покраска стен',
        'tiling': 'Укладка плитки',
        'wallpaper': 'Оклейка обоями',
        'plaster': 'Штукатурные работы',
        'drywall': 'Монтаж гипсокартона'
    }