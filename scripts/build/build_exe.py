#!/usr/bin/env python3
"""
Скрипт для создания exe файла ИИ интерфейса
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """Устанавливает PyInstaller если его нет"""
    try:
        import PyInstaller
        print("✅ PyInstaller уже установлен")
    except ImportError:
        print("📦 Устанавливаем PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✅ PyInstaller установлен")

def create_spec_file():
    """Создает spec файл для PyInstaller"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['web_interface.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('src', 'src'),
        ('data', 'data'),
        ('models', 'models'),
    ],
    hiddenimports=[
        'flask',
        'transformers',
        'torch',
        'tensorflow',
        'numpy',
        'pandas',
        'sklearn',
        'matplotlib',
        'seaborn',
        'requests',
        'beautifulsoup4',
        'lxml',
        'tqdm',
        'jupyter',
        'ipykernel',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ИИ_История',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
'''
    
    with open('ИИ_История.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ Создан spec файл: ИИ_История.spec")

def create_launcher_script():
    """Создает скрипт-запускатель для exe"""
    launcher_content = '''#!/usr/bin/env python3
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
'''
    
    with open('launcher.py', 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    print("✅ Создан скрипт-запускатель: launcher.py")

def build_exe():
    """Собирает exe файл"""
    print("🔨 Собираем exe файл...")
    
    # Создаем spec файл
    create_spec_file()
    
    # Собираем exe
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--console",
        "--name", "ИИ_История",
        "--add-data", "templates;templates",
        "--add-data", "src;src", 
        "--add-data", "data;data",
        "--add-data", "models;models",
        "--hidden-import", "flask",
        "--hidden-import", "transformers",
        "--hidden-import", "torch",
        "--hidden-import", "tensorflow",
        "--hidden-import", "numpy",
        "--hidden-import", "pandas",
        "--hidden-import", "sklearn",
        "--hidden-import", "matplotlib",
        "--hidden-import", "seaborn",
        "--hidden-import", "requests",
        "--hidden-import", "beautifulsoup4",
        "--hidden-import", "lxml",
        "--hidden-import", "tqdm",
        "--hidden-import", "jupyter",
        "--hidden-import", "ipykernel",
        "launcher.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Exe файл создан успешно!")
        
        # Перемещаем exe в корень проекта
        exe_path = Path("dist/ИИ_История.exe")
        if exe_path.exists():
            shutil.move(str(exe_path), "ИИ_История.exe")
            print("✅ Exe файл перемещен в корень проекта")
        
        # Очищаем временные файлы
        if Path("build").exists():
            shutil.rmtree("build")
        if Path("dist").exists():
            shutil.rmtree("dist")
        if Path("ИИ_История.spec").exists():
            os.remove("ИИ_История.spec")
        
        print("🧹 Временные файлы очищены")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка сборки: {e}")
        return False
    
    return True

def create_readme():
    """Создает README для exe файла"""
    readme_content = '''# 🏛️ ИИ для изучения истории - Exe версия

## 🚀 Запуск

Просто запустите файл `ИИ_История.exe` - браузер откроется автоматически!

## 📱 Использование

1. **Запустите** `ИИ_История.exe`
2. **Дождитесь** загрузки моделей (может занять несколько минут)
3. **Откройте** http://localhost:5000 в браузере
4. **Введите** промпт на русском языке
5. **Получите** ответ от ИИ

## 💡 Примеры промптов

- "В 1812 году произошло"
- "Петр I известен тем, что"
- "Сталин родился в"
- "Революция 1917 года привела к"

## ⚙️ Требования

- Windows 10/11
- Интернет-соединение (для загрузки моделей)
- 2+ ГБ свободного места

## 🚨 Решение проблем

- **Если exe не запускается** - проверьте антивирус
- **Если браузер не открывается** - откройте http://localhost:5000 вручную
- **Если модели не загружаются** - проверьте интернет-соединение

## 🎉 Готово!

Теперь у вас есть полноценное приложение для изучения истории с ИИ!
'''
    
    with open('README_EXE.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ Создан README: README_EXE.md")

def main():
    """Основная функция"""
    print("🏛️ Создание exe файла для ИИ интерфейса")
    print("=" * 50)
    
    # Проверяем наличие необходимых файлов
    required_files = ['web_interface.py', 'templates/index.html', 'src/models/history_ai.py']
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ Не найден файл: {file}")
            return
    
    print("✅ Все необходимые файлы найдены")
    
    # Устанавливаем PyInstaller
    install_pyinstaller()
    
    # Создаем скрипт-запускатель
    create_launcher_script()
    
    # Собираем exe
    if build_exe():
        create_readme()
        print()
        print("🎉 Exe файл создан успешно!")
        print("📁 Файл: ИИ_История.exe")
        print("📖 Инструкция: README_EXE.md")
        print()
        print("🚀 Теперь вы можете запускать ИИ интерфейс одним кликом!")
    else:
        print("❌ Ошибка создания exe файла")

if __name__ == "__main__":
    main()
