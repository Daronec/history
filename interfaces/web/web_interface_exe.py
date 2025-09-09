#!/usr/bin/env python3
"""
Веб-интерфейс для exe версии
Автоматически открывает браузер
"""

import sys
import os
import webbrowser
import time
import threading
from pathlib import Path

# Добавляем путь к модулям
sys.path.append('src')

def open_browser_delayed():
    """Открывает браузер через 5 секунд"""
    time.sleep(5)
    try:
        webbrowser.open('http://localhost:5000')
        print("🌐 Браузер открыт: http://localhost:5000")
    except Exception as e:
        print(f"⚠️ Не удалось открыть браузер: {e}")
        print("📱 Откройте вручную: http://localhost:5000")

def main():
    """Основная функция"""
    print("🏛️ ИИ для изучения истории")
    print("=" * 40)
    print("🚀 Запускаем веб-интерфейс...")
    print("📱 Браузер откроется автоматически через 5 секунд")
    print("🛑 Для остановки нажмите Ctrl+C")
    print()
    
    # Запускаем браузер в отдельном потоке
    browser_thread = threading.Thread(target=open_browser_delayed)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Импортируем и запускаем веб-интерфейс
    try:
        from web_interface import app
        print("✅ Веб-сервер запущен на http://localhost:5000")
        app.run(debug=False, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")
        print("💡 Возможные решения:")
        print("   1. Проверьте, что все файлы на месте")
        print("   2. Убедитесь, что порт 5000 свободен")
        print("   3. Проверьте подключение к интернету")
        input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()
