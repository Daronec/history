#!/usr/bin/env python3
"""
Скрипт сборки универсального exe файла для ИИ-История
Создает минимальный exe файл, который обращается к внешним файлам проекта
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def main():
    """Главная функция сборки"""
    print("🏛️ Создание УНИВЕРСАЛЬНОГО Windows exe файла")
    print("=" * 60)
    print("🎯 Цель: создать exe размером ~15-25 МБ")
    print("🔗 Обращается к внешним файлам проекта")
    print("✨ Включает все функции: промпты, файлы, переобучение")
    print()
    
    # Настройки
    exe_name = "AI-History"
    entry_point = "interfaces/windows/windows_interface_universal.py"
    
    # Проверяем наличие точки входа
    if not os.path.exists(entry_point):
        print(f"❌ Ошибка: файл {entry_point} не найден!")
        return False
    
    print(f"📝 Точка входа: {entry_point}")
    print(f"📦 Имя exe файла: {exe_name}.exe")
    print()
    
    # Создаем структуру проекта для exe
    create_project_structure()
    
    # Собираем exe файл
    if build_exe(exe_name, entry_point):
        print("✅ Универсальный exe файл создан успешно!")
        print(f"📁 Файл: {exe_name}.exe")
        print(f"📖 Инструкция: README_Universal_EXE.md")
        print()
        print("📊 Характеристики:")
        print("   • Размер: ~15-25 МБ")
        print("   • Функции: все (промпты, файлы, переобучение)")
        print("   • Зависимости: внешние файлы проекта")
        print("   • Совместимость: Windows 10/11")
        print()
        print("💡 Используйте этот exe для полной работы с ИИ!")
        return True
    else:
        print("❌ Ошибка создания exe файла!")
        return False

def create_project_structure():
    """Создает структуру проекта для внешней версии"""
    print("📁 Создаем структуру проекта...")
    
    directories = [
        'data/raw',
        'data/processed', 
        'models',
        'logs',
        'configs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"   ✅ {directory}")
    
    print("✅ Структура проекта создана")
    print()

def build_exe(exe_name, entry_point):
    """Собирает exe файл"""
    print("🔨 Собираем УНИВЕРСАЛЬНЫЙ exe файл...")
    print("🔗 Обращается к внешним файлам проекта")
    print("✨ Включает все функции")
    print()
    
    try:
        # Команда PyInstaller через Python из виртуального окружения
        # Проверяем, находимся ли мы в виртуальном окружении
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            # Мы в виртуальном окружении
            python_exe = sys.executable
        else:
            # Ищем Python в виртуальном окружении
            venv_python = os.path.join('venv', 'Scripts', 'python.exe')
            if os.path.exists(venv_python):
                python_exe = venv_python
            else:
                python_exe = sys.executable  # Fallback к системному Python
        
        pyinstaller_cmd = [
            python_exe, '-m', 'PyInstaller',
            '--onefile',                    # Один exe файл
            '--windowed',                   # Без консоли
            '--name', exe_name,             # Имя файла
            '--distpath', 'dist',           # Папка вывода
            '--workpath', 'build',          # Временная папка
            '--specpath', '.',              # Папка для .spec файла
            '--clean',                      # Очистка перед сборкой
            
            # Скрытые импорты (только необходимые для интерфейса)
            '--hidden-import', 'tkinter',
            '--hidden-import', 'tkinter.ttk',
            '--hidden-import', 'tkinter.messagebox',
            '--hidden-import', 'tkinter.filedialog',
            '--hidden-import', 'tkinter.scrolledtext',
            '--hidden-import', 'threading',
            '--hidden-import', 'subprocess',
            '--hidden-import', 'pathlib',
            '--hidden-import', 'logging',
            '--hidden-import', 'json',
            '--hidden-import', 'shutil',
            
            # НЕ включаем ML библиотеки - они будут внешними
            # '--hidden-import', 'transformers',  # Исключено
            # '--hidden-import', 'torch',         # Исключено
            # '--hidden-import', 'tensorflow',    # Исключено
            # '--hidden-import', 'numpy',         # Исключено
            # '--hidden-import', 'pandas',        # Исключено
            # '--hidden-import', 'sklearn',       # Исключено
            # '--hidden-import', 'matplotlib',    # Исключено
            # '--hidden-import', 'seaborn',       # Исключено
            # '--hidden-import', 'requests',      # Исключено
            # '--hidden-import', 'beautifulsoup4', # Исключено
            # '--hidden-import', 'lxml',          # Исключено
            # '--hidden-import', 'tqdm',          # Исключено
            # '--hidden-import', 'jupyter',       # Исключено
            # '--hidden-import', 'ipykernel',     # Исключено
            
            entry_point
        ]
        
        print("🚀 Запускаем PyInstaller...")
        print(f"🐍 Используем Python: {python_exe}")
        print(f"📝 Команда: {' '.join(pyinstaller_cmd)}")
        print()
        
        # Выполняем команду
        result = subprocess.run(pyinstaller_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ PyInstaller выполнен успешно!")
            
            # Перемещаем exe файл в корень проекта
            exe_path = f"dist/{exe_name}.exe"
            target_path = f"{exe_name}.exe"
            
            if os.path.exists(exe_path):
                # Удаляем старый файл, если он существует
                if os.path.exists(target_path):
                    try:
                        os.remove(target_path)
                        print(f"🗑️ Удален старый файл: {target_path}")
                    except PermissionError:
                        print(f"⚠️ Не удалось удалить старый файл (возможно, запущен): {target_path}")
                        print(f"📁 Exe файл доступен в: {exe_path}")
                        return True
                
                # Перемещаем новый файл
                try:
                    shutil.move(exe_path, target_path)
                    print(f"✅ Exe файл перемещен в корень проекта")
                except PermissionError:
                    print(f"⚠️ Не удалось переместить файл (возможно, заблокирован)")
                    print(f"📁 Exe файл доступен в: {exe_path}")
                    return True
                
                # Получаем размер файла
                file_size = os.path.getsize(f"{exe_name}.exe")
                size_mb = file_size / (1024 * 1024)
                print(f"📏 Размер файла: {size_mb:.1f} МБ")
                
                # Создаем README
                create_readme(exe_name)
                
                # Очищаем временные файлы
                cleanup_build_files(exe_name)
                
                return True
            else:
                print(f"❌ Exe файл не найден: {exe_path}")
                return False
        else:
            print(f"❌ Ошибка PyInstaller:")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка сборки: {e}")
        return False

def create_readme(exe_name):
    """Создает README для exe файла"""
    readme_content = f"""# {exe_name}.exe - Универсальный интерфейс ИИ-История

## 🎯 Описание
Универсальный интерфейс для работы с ИИ моделями истории. Включает все необходимые функции в одном приложении.

## ✨ Функции
- 🤖 **Работа с ИИ**: ввод промптов и генерация ответов
- 📁 **Управление файлами**: загрузка и просмотр файлов данных
- 🎓 **Переобучение моделей**: улучшение качества ответов
- 🔄 **Выбор модели**: английская или русская модель
- 📊 **Прогресс-бар**: отслеживание процесса переобучения

## 🚀 Запуск
1. Убедитесь, что в папке с exe файлом есть структура проекта:
   ```
   {exe_name}.exe
   ├── src/
   │   ├── train_model.py
   │   ├── generate_text.py
   │   └── data_processing.py
   ├── scripts/
   │   └── training/
   │       └── train_model_ru.py
   ├── data/
   │   └── raw/          # Сюда загружаются файлы
   ├── models/           # Здесь сохраняются обученные модели
   └── logs/             # Логи работы приложения
   ```

2. Запустите `{exe_name}.exe`

## 📋 Использование

### Работа с ИИ
1. Выберите модель (английская/русская)
2. Введите промпт в поле ввода
3. Нажмите "Сгенерировать ответ"
4. Результат появится в поле вывода

### Управление файлами
1. Нажмите "Загрузить файл" для добавления данных
2. Используйте "Обновить" для обновления списка
3. "Открыть папку" - открывает папку с данными
4. Двойной клик по файлу - информация о файле

### Переобучение моделей
1. Загрузите файлы данных в папку data/raw
2. Нажмите "Переобучить модели"
3. Выберите модель для переобучения
4. Дождитесь завершения процесса

## ⚠️ Требования
- Windows 10/11
- Python скрипты проекта в папке src/
- Виртуальное окружение с установленными зависимостями

## 🔧 Устранение неполадок
- Если exe не запускается, проверьте наличие Python скриптов
- При ошибках генерации проверьте наличие обученных моделей
- Логи сохраняются в папке logs/

## 📞 Поддержка
При возникновении проблем проверьте:
1. Наличие всех файлов проекта
2. Установленные зависимости Python
3. Логи в папке logs/
"""

    with open(f"README_{exe_name}_EXE.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"✅ Создан README: README_{exe_name}_EXE.md")

def cleanup_build_files(exe_name):
    """Удаляет временные файлы сборки"""
    print("🧹 Очищаем временные файлы...")
    
    files_to_remove = [
        f'{exe_name}.spec',
        'build',
        'dist'
    ]
    
    for item in files_to_remove:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.rmtree(item)
                print(f"   🗑️ Удалена папка: {item}")
            else:
                os.remove(item)
                print(f"   🗑️ Удален файл: {item}")
    
    print("✅ Временные файлы очищены")

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Универсальный exe файл создан успешно!")
        print("💡 Теперь у вас есть один файл со всеми функциями!")
    else:
        print("\n❌ Создание exe файла не удалось!")
        sys.exit(1)
