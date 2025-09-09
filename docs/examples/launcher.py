#!/usr/bin/env python3
"""
Запускатель для ИИ интерфейса
"""

import os
import sys
import webbrowser
import time
import threading
from pathlib import Path

def open_browser():
    """Открывает браузер через 3 секунды"""
    time.sleep(3)
    webbrowser.open('http://localhost:5000')

def main():
    print("🏛️ ИИ для изучения истории")
    print("=" * 40)
    print("🚀 Запускаем веб-интерфейс...")
    print("📱 Браузер откроется автоматически")
    print("🛑 Для остановки нажмите Ctrl+C")
    print()
    
    # Запускаем браузер в отдельном потоке
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Импортируем и запускаем веб-интерфейс
    try:
        from web_interface import app
        app.run(debug=False, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")
        input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    main()
