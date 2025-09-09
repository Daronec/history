#!/usr/bin/env python3
"""
Создание оптимизированного exe файла для Windows интерфейса
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

def build_optimized_exe():
    """Собирает оптимизированный exe файл"""
    print("🔨 Собираем ОПТИМИЗИРОВАННЫЙ exe файл...")
    print("📉 Исключаем тяжелые библиотеки для уменьшения размера")
    
    # Команда для PyInstaller с исключениями
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",  # Без консоли
        "--name", "ИИ_История_Windows_Lite",
        "--add-data", "src;src",
        "--add-data", "data;data", 
        "--add-data", "models;models",
        
        # Основные модули
        "--hidden-import", "tkinter",
        "--hidden-import", "tkinter.ttk",
        "--hidden-import", "tkinter.scrolledtext",
        "--hidden-import", "tkinter.messagebox",
        "--hidden-import", "tkinter.filedialog",
        
        # Минимальные ML модули
        "--hidden-import", "transformers",
        "--hidden-import", "torch",
        "--hidden-import", "numpy",
        
        # Исключаем тяжелые библиотеки
        "--exclude-module", "tensorflow",
        "--exclude-module", "pandas",
        "--exclude-module", "sklearn",
        "--exclude-module", "matplotlib",
        "--exclude-module", "seaborn",
        "--exclude-module", "jupyter",
        "--exclude-module", "ipykernel",
        "--exclude-module", "scipy",
        "--exclude-module", "PIL",
        "--exclude-module", "cv2",
        "--exclude-module", "plotly",
        "--exclude-module", "bokeh",
        "--exclude-module", "dash",
        "--exclude-module", "streamlit",
        
        # Исключаем неиспользуемые модули
        "--exclude-module", "flask",
        "--exclude-module", "django",
        "--exclude-module", "fastapi",
        "--exclude-module", "requests",
        "--exclude-module", "beautifulsoup4",
        "--exclude-module", "lxml",
        "--exclude-module", "tqdm",
        
        "interfaces/windows/windows_interface_exe.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Оптимизированный exe файл создан!")
        
        # Перемещаем exe в корень проекта
        exe_path = Path("dist/ИИ_История_Windows_Lite.exe")
        if exe_path.exists():
            shutil.move(str(exe_path), "ИИ_История_Windows_Lite.exe")
            print("✅ Exe файл перемещен в корень проекта")
        
        # Очищаем временные файлы
        if Path("build").exists():
            shutil.rmtree("build")
        if Path("dist").exists():
            shutil.rmtree("dist")
        if Path("ИИ_История_Windows_Lite.spec").exists():
            os.remove("ИИ_История_Windows_Lite.spec")
        
        print("🧹 Временные файлы очищены")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка сборки: {e}")
        return False

def create_lite_interface():
    """Создает облегченную версию интерфейса без тяжелых зависимостей"""
    print("📝 Создаем облегченную версию интерфейса...")
    
    lite_interface = '''#!/usr/bin/env python3
"""
Облегченная версия Windows интерфейса (без тяжелых ML библиотек)
"""

import sys
import os
import threading
import json
import shutil
from datetime import datetime
from pathlib import Path

# Определяем, запущены ли мы из exe файла
def is_exe():
    return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')

# Настраиваем пути в зависимости от режима запуска
if is_exe():
    # Режим exe - используем папку где находится exe файл
    BASE_DIR = os.path.dirname(sys.executable)
    MODELS_DIR = os.path.join(BASE_DIR, 'models')
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    SRC_DIR = os.path.join(BASE_DIR, 'src')
    
    # Создаем папки если их нет
    os.makedirs(os.path.join(DATA_DIR, 'raw'), exist_ok=True)
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    # Добавляем пути для импорта модулей
    sys.path.append(SRC_DIR)
    # Также добавляем временную папку для доступа к встроенным модулям
    sys.path.append(sys._MEIPASS)
    sys.path.append(os.path.join(sys._MEIPASS, 'src'))
else:
    # Обычный режим
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    MODELS_DIR = os.path.join(BASE_DIR, 'models')
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    SRC_DIR = os.path.join(BASE_DIR, 'src')
    sys.path.append(SRC_DIR)

try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext, messagebox, filedialog
    from tkinter.font import Font
except ImportError:
    print("❌ Tkinter не установлен. Установите: pip install tk")
    sys.exit(1)

class HistoryAILiteApp:
    """Облегченная версия приложения"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🏛️ ИИ для изучения истории (Lite версия)")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Шрифты
        self.title_font = Font(family="Arial", size=16, weight="bold")
        self.button_font = Font(family="Arial", size=10, weight="bold")
        self.small_font = Font(family="Arial", size=9)
        
        # Переменные
        self.data_files = []
        
        # Создаем интерфейс
        self.create_widgets()
        
        # Загружаем историю
        self.load_history()
        
        # Обновляем список файлов
        self.refresh_files_list()
    
    def create_widgets(self):
        """Создает элементы интерфейса"""
        # Заголовок
        title_label = tk.Label(
            self.root,
            text="🏛️ ИИ для изучения истории (Lite версия)",
            font=self.title_font,
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=10)
        
        # Информация о версии
        info_label = tk.Label(
            self.root,
            text="📦 Облегченная версия - только управление файлами и базовые функции",
            font=self.small_font,
            bg='#f0f0f0',
            fg='#7f8c8d'
        )
        info_label.pack(pady=5)
        
        # Основной фрейм
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Левая панель - управление файлами
        left_frame = tk.Frame(main_frame, bg='#ecf0f1', relief='raised', bd=2)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Заголовок левой панели
        left_title = tk.Label(
            left_frame,
            text="📁 Управление файлами",
            font=self.button_font,
            bg='#34495e',
            fg='white',
            pady=10
        )
        left_title.pack(fill='x')
        
        # Кнопки управления файлами
        file_buttons_frame = tk.Frame(left_frame, bg='#ecf0f1')
        file_buttons_frame.pack(fill='x', padx=10, pady=10)
        
        self.upload_btn = tk.Button(
            file_buttons_frame,
            text="📤 Загрузить файл",
            font=self.button_font,
            command=self.upload_file,
            bg='#27ae60',
            fg='white',
            relief='flat',
            padx=20,
            pady=10
        )
        self.upload_btn.pack(side='left', padx=(0, 10))
        
        self.refresh_btn = tk.Button(
            file_buttons_frame,
            text="🔄 Обновить список",
            font=self.button_font,
            command=self.refresh_files_list,
            bg='#3498db',
            fg='white',
            relief='flat',
            padx=20,
            pady=10
        )
        self.refresh_btn.pack(side='left', padx=(0, 10))
        
        self.open_folder_btn = tk.Button(
            file_buttons_frame,
            text="📂 Открыть папку",
            font=self.button_font,
            command=self.open_data_folder,
            bg='#9b59b6',
            fg='white',
            relief='flat',
            padx=20,
            pady=10
        )
        self.open_folder_btn.pack(side='left')
        
        # Список файлов
        files_frame = tk.Frame(left_frame, bg='#ecf0f1')
        files_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Заголовок списка
        files_title = tk.Label(
            files_frame,
            text="📋 Загруженные файлы:",
            font=self.button_font,
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        files_title.pack(anchor='w', pady=(0, 5))
        
        # Таблица файлов
        columns = ('Имя файла', 'Размер', 'Дата')
        self.files_tree = ttk.Treeview(files_frame, columns=columns, show='headings', height=15)
        
        # Настройка колонок
        self.files_tree.heading('Имя файла', text='Имя файла')
        self.files_tree.heading('Размер', text='Размер')
        self.files_tree.heading('Дата', text='Дата')
        
        self.files_tree.column('Имя файла', width=200)
        self.files_tree.column('Размер', width=80)
        self.files_tree.column('Дата', width=100)
        
        # Скроллбар для таблицы
        files_scrollbar = ttk.Scrollbar(files_frame, orient='vertical', command=self.files_tree.yview)
        self.files_tree.configure(yscrollcommand=files_scrollbar.set)
        
        self.files_tree.pack(side='left', fill='both', expand=True)
        files_scrollbar.pack(side='right', fill='y')
        
        # Обработчик двойного клика
        self.files_tree.bind('<Double-1>', self.on_file_double_click)
        
        # Правая панель - информация
        right_frame = tk.Frame(main_frame, bg='#f0f0f0')
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Заголовок правой панели
        right_title = tk.Label(
            right_frame,
            text="ℹ️ Информация",
            font=self.button_font,
            bg='#34495e',
            fg='white',
            pady=10
        )
        right_title.pack(fill='x')
        
        # Информационный текст
        info_text = tk.Text(
            right_frame,
            wrap='word',
            font=self.small_font,
            bg='white',
            fg='#2c3e50',
            padx=10,
            pady=10,
            state='disabled'
        )
        info_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Добавляем информацию
        info_content = """
🏛️ ИИ для изучения истории (Lite версия)

📦 Что включено:
• Управление файлами
• Загрузка данных
• Просмотр списка файлов
• Открытие папок

❌ Что исключено (для уменьшения размера):
• TensorFlow (~1-2 ГБ)
• Pandas (~200-300 МБ)
• Matplotlib (~100-200 МБ)
• Scikit-learn (~200-300 МБ)
• Jupyter (~100-200 МБ)
• Другие тяжелые библиотеки

💡 Использование:
1. Загружайте файлы через интерфейс
2. Просматривайте список загруженных файлов
3. Открывайте папки для прямого доступа
4. Используйте полную версию для работы с ИИ

🎯 Поддерживаемые форматы:
• JSON файлы
• CSV файлы
• TXT файлы
• PDF файлы

📁 Файлы сохраняются в папку data/raw/
        """
        
        info_text.config(state='normal')
        info_text.insert('1.0', info_content)
        info_text.config(state='disabled')
        
        # Статус-бар
        self.status_var = tk.StringVar()
        if is_exe():
            self.status_var.set(f"🚀 Lite версия готова | Файлы сохраняются в: {os.path.join(DATA_DIR, 'raw')}")
        else:
            self.status_var.set("🚀 Lite версия готова")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=self.small_font,
            bg='#34495e',
            fg='white',
            anchor='w',
            padx=10,
            pady=5
        )
        status_bar.pack(side='bottom', fill='x')
    
    def upload_file(self):
        """Загружает файл в папку data/raw"""
        try:
            # Диалог выбора файла
            file_path = filedialog.askopenfilename(
                title=f"Выберите файл для загрузки (будет сохранен в: {os.path.join(DATA_DIR, 'raw')})",
                filetypes=[
                    ("Все поддерживаемые", "*.json;*.csv;*.txt;*.pdf"),
                    ("JSON файлы", "*.json"),
                    ("CSV файлы", "*.csv"),
                    ("Текстовые файлы", "*.txt"),
                    ("PDF файлы", "*.pdf"),
                    ("Все файлы", "*.*")
                ]
            )
            
            if file_path:
                # Получаем имя файла
                filename = os.path.basename(file_path)
                
                # Путь назначения
                dest_path = os.path.join(DATA_DIR, 'raw', filename)
                
                # Копируем файл
                shutil.copy2(file_path, dest_path)
                
                # Обновляем список файлов
                self.refresh_files_list()
                
                # Показываем сообщение об успехе
                messagebox.showinfo(
                    "Успех",
                    f"Файл '{filename}' успешно загружен!\\n\\n"
                    f"Сохранен в: {dest_path}\\n\\n"
                    f"Теперь вы можете использовать полную версию для работы с ИИ."
                )
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки файла:\\n{e}")
    
    def refresh_files_list(self):
        """Обновляет список файлов"""
        try:
            # Очищаем таблицу
            for item in self.files_tree.get_children():
                self.files_tree.delete(item)
            
            # Получаем список файлов
            raw_dir = os.path.join(DATA_DIR, 'raw')
            if os.path.exists(raw_dir):
                files = os.listdir(raw_dir)
                self.data_files = []
                
                for filename in files:
                    file_path = os.path.join(raw_dir, filename)
                    if os.path.isfile(file_path):
                        # Получаем информацию о файле
                        stat = os.stat(file_path)
                        size = self.format_file_size(stat.st_size)
                        date = datetime.fromtimestamp(stat.st_mtime).strftime('%d.%m.%Y %H:%M')
                        
                        # Добавляем в таблицу
                        self.files_tree.insert('', 'end', values=(filename, size, date))
                        self.data_files.append(filename)
            
            # Обновляем статус
            self.update_status(f"📁 Найдено файлов: {len(self.data_files)}")
            
        except Exception as e:
            print(f"Ошибка обновления списка файлов: {e}")
    
    def format_file_size(self, size_bytes):
        """Форматирует размер файла"""
        if size_bytes < 1024:
            return f"{size_bytes} Б"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} КБ"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} МБ"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} ГБ"
    
    def open_data_folder(self):
        """Открывает папку data/raw в проводнике"""
        try:
            raw_dir = os.path.join(DATA_DIR, 'raw')
            os.makedirs(raw_dir, exist_ok=True)
            os.startfile(raw_dir)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть папку:\\n{e}")
    
    def on_file_double_click(self, event):
        """Обработчик двойного клика на файл"""
        try:
            item = self.files_tree.selection()[0]
            filename = self.files_tree.item(item, 'values')[0]
            self.show_file_info(filename)
        except Exception as e:
            print(f"Ошибка обработки двойного клика: {e}")
    
    def show_file_info(self, filename):
        """Показывает информацию о файле"""
        try:
            file_path = os.path.join(DATA_DIR, 'raw', filename)
            if os.path.exists(file_path):
                stat = os.stat(file_path)
                size = self.format_file_size(stat.st_size)
                date = datetime.fromtimestamp(stat.st_mtime).strftime('%d.%m.%Y %H:%M:%S')
                
                info = f"""📄 Информация о файле:

📁 Имя: {filename}
📏 Размер: {size}
📅 Дата изменения: {date}
📍 Полный путь: {file_path}

📋 Поддерживаемые форматы:
• JSON - структурированные данные
• CSV - табличные данные
• TXT - простой текст
• PDF - документы с текстом
                """
                
                messagebox.showinfo("Информация о файле", info)
            else:
                messagebox.showerror("Ошибка", f"Файл '{filename}' не найден!")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка получения информации о файле:\\n{e}")
    
    def update_status(self, message):
        """Обновляет статус-бар"""
        self.status_var.set(message)
    
    def load_history(self):
        """Загружает историю (заглушка для совместимости)"""
        pass
    
    def run(self):
        """Запускает приложение"""
        self.root.mainloop()

def main():
    """Основная функция"""
    try:
        app = HistoryAILiteApp()
        app.run()
    except Exception as e:
        print(f"Ошибка запуска приложения: {e}")
        input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    main()
'''
    
    # Сохраняем облегченную версию
    lite_path = 'interfaces/windows/windows_interface_lite.py'
    with open(lite_path, 'w', encoding='utf-8') as f:
        f.write(lite_interface)
    
    print(f"✅ Создана облегченная версия: {lite_path}")
    return lite_path

def create_readme_lite():
    """Создает README для Lite версии"""
    readme_content = '''# 🏛️ ИИ для изучения истории - Lite версия

## 🚀 Запуск

Просто запустите файл `ИИ_История_Windows_Lite.exe` - откроется облегченная версия!

## 📦 Что включено в Lite версию

### ✅ Включено:
- **📁 Управление файлами** - загрузка и просмотр файлов
- **📤 Загрузка файлов** - в папку data/raw
- **📋 Список файлов** - с информацией о размере и дате
- **📂 Открытие папок** - прямо из интерфейса
- **ℹ️ Информация о файлах** - подробные данные

### ❌ Исключено (для уменьшения размера):
- **🤖 TensorFlow** (~1-2 ГБ) - тяжелая ML библиотека
- **📊 Pandas** (~200-300 МБ) - анализ данных
- **📈 Matplotlib** (~100-200 МБ) - графики
- **🔬 Scikit-learn** (~200-300 МБ) - машинное обучение
- **📚 Jupyter** (~100-200 МБ) - интерактивные среды
- **🌐 Flask** (~50-100 МБ) - веб-фреймворк
- **🔧 Другие тяжелые библиотеки**

## 🎯 Использование Lite версии

### **1. Загрузка файлов:**
1. Нажмите **"📤 Загрузить файл"**
2. Выберите файл (JSON, CSV, TXT, PDF)
3. Файл сохранится в папку data/raw/
4. Список обновится автоматически

### **2. Просмотр файлов:**
1. Посмотрите список в таблице
2. Дважды кликните на файл для информации
3. Нажмите **"📂 Открыть папку"** для прямого доступа

### **3. Работа с данными:**
1. Загрузите данные через Lite версию
2. Используйте полную версию для работы с ИИ
3. Переобучите модели с новыми данными

## 📊 Сравнение версий

| Функция | Lite версия | Полная версия |
|---------|-------------|---------------|
| **Размер exe** | ~50-100 МБ | ~2-3 ГБ |
| **Загрузка файлов** | ✅ | ✅ |
| **Список файлов** | ✅ | ✅ |
| **Генерация текста** | ❌ | ✅ |
| **Переобучение моделей** | ❌ | ✅ |
| **Настройки ИИ** | ❌ | ✅ |
| **История запросов** | ❌ | ✅ |

## 💡 Когда использовать Lite версию

### **✅ Используйте Lite версию для:**
- Загрузки и управления файлами
- Просмотра списка данных
- Быстрого доступа к папкам
- Когда нужен только файловый менеджер

### **✅ Используйте полную версию для:**
- Генерации текста с ИИ
- Переобучения моделей
- Работы с настройками
- Полноценной работы с ИИ

## 🎉 Преимущества Lite версии

### **Размер:**
- ✅ **В 20-30 раз меньше** полной версии
- ✅ **Быстрая загрузка** и установка
- ✅ **Меньше места** на диске

### **Производительность:**
- ✅ **Быстрый запуск** приложения
- ✅ **Низкое потребление** ресурсов
- ✅ **Стабильная работа**

### **Удобство:**
- ✅ **Простой интерфейс** для файлов
- ✅ **Быстрый доступ** к данным
- ✅ **Легкое управление** файлами

## 🚀 Рекомендации

1. **Начните с Lite версии** для загрузки данных
2. **Используйте полную версию** для работы с ИИ
3. **Комбинируйте обе версии** для максимальной эффективности
4. **Lite версия** идеальна для быстрого управления файлами

---

**🎉 Теперь у вас есть компактная версия для управления файлами!**
'''
    
    with open('README_Windows_Lite.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ Создан README: README_Windows_Lite.md")

def main():
    """Основная функция"""
    print("🏛️ Создание ОПТИМИЗИРОВАННОГО Windows exe файла")
    print("=" * 60)
    print("📉 Цель: уменьшить размер с 2.7 ГБ до ~50-100 МБ")
    print()
    
    # Проверяем наличие необходимых файлов
    required_files = ['interfaces/windows/windows_interface_exe.py']
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ Не найден файл: {file}")
            return
    
    print("✅ Все необходимые файлы найдены")
    
    # Создаем облегченную версию интерфейса
    lite_interface_path = create_lite_interface()
    
    # Обновляем команду сборки для использования lite версии
    print("🔨 Собираем Lite версию...")
    
    # Команда для PyInstaller с lite версией
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "ИИ_История_Windows_Lite",
        "--add-data", "src;src",
        "--add-data", "data;data", 
        "--add-data", "models;models",
        "--hidden-import", "tkinter",
        "--hidden-import", "tkinter.ttk",
        "--hidden-import", "tkinter.scrolledtext",
        "--hidden-import", "tkinter.messagebox",
        "--hidden-import", "tkinter.filedialog",
        lite_interface_path
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Lite exe файл создан!")
        
        # Перемещаем exe в корень проекта
        exe_path = Path("dist/ИИ_История_Windows_Lite.exe")
        if exe_path.exists():
            shutil.move(str(exe_path), "ИИ_История_Windows_Lite.exe")
            print("✅ Lite exe файл перемещен в корень проекта")
        
        # Очищаем временные файлы
        if Path("build").exists():
            shutil.rmtree("build")
        if Path("dist").exists():
            shutil.rmtree("dist")
        if Path("ИИ_История_Windows_Lite.spec").exists():
            os.remove("ИИ_История_Windows_Lite.spec")
        
        print("🧹 Временные файлы очищены")
        
        # Создаем README
        create_readme_lite()
        
        print()
        print("🎉 Lite версия создана успешно!")
        print("📁 Файл: ИИ_История_Windows_Lite.exe")
        print("📖 Инструкция: README_Windows_Lite.md")
        print()
        print("📊 Сравнение размеров:")
        print("   • Полная версия: ~2.7 ГБ")
        print("   • Lite версия: ~50-100 МБ")
        print("   • Экономия: ~95% размера!")
        print()
        print("💡 Используйте Lite версию для управления файлами!")
        print("🤖 Используйте полную версию для работы с ИИ!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка сборки: {e}")

if __name__ == "__main__":
    main()
'''
