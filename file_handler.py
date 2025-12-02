# file_handler.py - Обработка загруженных файлов
import os
import tempfile
from config import Config

class FileHandler:
    @staticmethod
    def is_supported_format(filename):
        """Проверка формата файла"""
        ext = os.path.splitext(filename)[1].lower()
        return ext in Config.SUPPORTED_FORMATS
    
    @staticmethod
    def is_valid_size(file_size):
        """Проверка размера файла"""
        return file_size <= Config.MAX_FILE_SIZE
    
    @staticmethod
    def save_temporary_file(file_content, extension='.png'):
        """Сохранить файл временно"""
        with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp:
            tmp.write(file_content)
            return tmp.name
    
    @staticmethod
    def cleanup_file(filepath):
        """Удалить временный файл"""
        try:
            if os.path.exists(filepath):
                os.unlink(filepath)
        except:
            pass