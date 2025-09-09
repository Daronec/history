#!/usr/bin/env python3
"""
Универсальный Windows интерфейс для ИИ-История
Включает все функции: промпты, генерация, управление файлами, переобучение
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import subprocess
import json
from pathlib import Path
import logging

# Устанавливаем кодировку для Windows
if sys.platform.startswith('win'):
    import codecs
    try:
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())
    except:
        pass  # Если не удалось изменить кодировку, продолжаем

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/interface.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class UniversalHistoryInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_paths()
        self.setup_ui()
        self.load_models()
        
    def is_exe(self):
        """Проверяет, запущен ли скрипт как exe файл"""
        return getattr(sys, 'frozen', False)
    
    def setup_paths(self):
        """Настраивает пути для работы в exe и dev режимах"""
        if self.is_exe():
            # В exe режиме - пути относительно exe файла
            self.BASE_DIR = Path(sys.executable).parent
        else:
            # В dev режиме - пути относительно проекта
            self.BASE_DIR = Path(__file__).parent.parent.parent
        
        # Основные директории
        self.MODELS_DIR = self.BASE_DIR / "models"
        self.DATA_DIR = self.BASE_DIR / "data"
        self.SRC_DIR = self.BASE_DIR / "src"
        self.SCRIPTS_DIR = self.BASE_DIR / "scripts"
        
        # Создаем необходимые директории
        for directory in [self.MODELS_DIR, self.DATA_DIR / "raw", self.DATA_DIR / "processed"]:
            directory.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Базовая директория: {self.BASE_DIR}")
        logger.info(f"Директория моделей: {self.MODELS_DIR}")
        logger.info(f"Директория данных: {self.DATA_DIR}")
    
    def setup_ui(self):
        """Настраивает пользовательский интерфейс"""
        self.root.title("ИИ-История - Универсальный интерфейс")
        self.root.geometry("1600x1000")
        self.root.configure(bg='#ecf0f1')
        
        # Шрифты
        self.title_font = ('Arial', 16, 'bold')
        self.button_font = ('Arial', 10, 'bold')
        self.text_font = ('Arial', 10)
        
        # Статус-бар (создаем первым)
        self.create_status_bar()
        
        # Создание основного интерфейса
        self.create_main_layout()
    
    def create_main_layout(self):
        """Создает основную компоновку интерфейса"""
        # Главный контейнер
        main_container = tk.Frame(self.root, bg='#ecf0f1')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Левая панель - управление файлами и переобучение (увеличена ширина)
        left_panel = tk.Frame(main_container, bg='#ecf0f1', width=500)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Правая панель - работа с ИИ
        right_panel = tk.Frame(main_container, bg='#ecf0f1')
        right_panel.pack(side='right', fill='both', expand=True)
        
        # Создаем содержимое панелей
        self.create_file_management_panel(left_panel)
        self.create_ai_panel(right_panel)
    
    def create_file_management_panel(self, parent):
        """Создает панель управления файлами"""
        # Заголовок
        title_label = tk.Label(
            parent,
            text="📁 Управление файлами",
            font=self.title_font,
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 10))
        
        # Кнопки управления файлами (в две строки)
        file_buttons_frame = tk.Frame(parent, bg='#ecf0f1')
        file_buttons_frame.pack(fill='x', pady=(0, 10))
        
        # Первая строка кнопок
        buttons_row1 = tk.Frame(file_buttons_frame, bg='#ecf0f1')
        buttons_row1.pack(fill='x', pady=(0, 5))
        
        self.upload_btn = tk.Button(
            buttons_row1,
            text="📤 Загрузить файлы",
            font=self.button_font,
            command=self.upload_file,
            bg='#3498db',
            fg='white',
            relief='flat',
            padx=15,
            pady=8
        )
        self.upload_btn.pack(side='left', padx=(0, 5), fill='x', expand=True)
        
        self.refresh_btn = tk.Button(
            buttons_row1,
            text="🔄 Обновить",
            font=self.button_font,
            command=self.refresh_file_list,
            bg='#2ecc71',
            fg='white',
            relief='flat',
            padx=15,
            pady=8
        )
        self.refresh_btn.pack(side='left', padx=5, fill='x', expand=True)
        
        # Вторая строка кнопок
        buttons_row2 = tk.Frame(file_buttons_frame, bg='#ecf0f1')
        buttons_row2.pack(fill='x')
        
        self.open_folder_btn = tk.Button(
            buttons_row2,
            text="📂 Открыть папку",
            font=self.button_font,
            command=self.open_data_folder,
            bg='#9b59b6',
            fg='white',
            relief='flat',
            padx=15,
            pady=8
        )
        self.open_folder_btn.pack(fill='x')
        
        # Список файлов
        files_frame = tk.Frame(parent, bg='#ecf0f1')
        files_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        files_label = tk.Label(
            files_frame,
            text="Загруженные файлы:",
            font=self.button_font,
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        files_label.pack(anchor='w', pady=(0, 5))
        
        # Treeview для списка файлов
        self.files_tree = ttk.Treeview(
            files_frame,
            columns=('size', 'date'),
            show='tree headings',
            height=8
        )
        self.files_tree.heading('#0', text='Имя файла')
        self.files_tree.heading('size', text='Размер')
        self.files_tree.heading('date', text='Дата')
        
        self.files_tree.column('#0', width=200)
        self.files_tree.column('size', width=80)
        self.files_tree.column('date', width=100)
        
        # Скроллбар для списка файлов
        files_scrollbar = ttk.Scrollbar(files_frame, orient='vertical', command=self.files_tree.yview)
        self.files_tree.configure(yscrollcommand=files_scrollbar.set)
        
        self.files_tree.pack(side='left', fill='both', expand=True)
        files_scrollbar.pack(side='right', fill='y')
        
        # Привязка событий
        self.files_tree.bind('<Double-1>', self.on_file_double_click)
        
        # Кнопка переобучения
        retrain_frame = tk.Frame(parent, bg='#ecf0f1')
        retrain_frame.pack(fill='x', pady=(10, 0))
        
        self.retrain_btn = tk.Button(
            retrain_frame,
            text="🎓 Переобучить модели",
            font=self.button_font,
            command=self.retrain_models,
            bg='#e74c3c',
            fg='white',
            relief='flat',
            padx=15,
            pady=10
        )
        self.retrain_btn.pack(fill='x')
        
        # Кнопка тестирования модели
        self.test_btn = tk.Button(
            retrain_frame,
            text="🧪 Тест модели",
            font=self.button_font,
            command=self.test_model,
            bg='#f39c12',
            fg='white',
            relief='flat',
            padx=15,
            pady=10
        )
        self.test_btn.pack(fill='x', pady=(5, 0))
        
        # Прогресс-бар для переобучения
        self.progress_frame = tk.Frame(parent, bg='#ecf0f1')
        self.progress_frame.pack(fill='x', pady=(10, 0))
        
        self.progress_label = tk.Label(
            self.progress_frame,
            text="Прогресс переобучения:",
            font=self.text_font,
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        self.progress_label.pack(anchor='w')
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='determinate'
        )
        self.progress_bar.pack(fill='x', pady=(5, 0))
        
        self.progress_percent = tk.Label(
            self.progress_frame,
            text="0%",
            font=self.text_font,
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        self.progress_percent.pack(anchor='e')
        
        # Скрываем прогресс-бар изначально
        self.progress_frame.pack_forget()
        
        # Загружаем список файлов
        self.refresh_file_list()
    
    def create_ai_panel(self, parent):
        """Создает панель работы с ИИ"""
        # Заголовок
        title_label = tk.Label(
            parent,
            text="🤖 Работа с ИИ",
            font=self.title_font,
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 10))
        
        # Выбор модели
        model_frame = tk.Frame(parent, bg='#ecf0f1')
        model_frame.pack(fill='x', pady=(0, 10))
        
        model_label = tk.Label(
            model_frame,
            text="Выберите модель:",
            font=self.button_font,
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        model_label.pack(side='left')
        
        self.model_var = tk.StringVar(value="Обученная модель")
        self.model_combo = ttk.Combobox(
            model_frame,
            textvariable=self.model_var,
            values=["Обученная модель"],
            state="readonly",
            width=20
        )
        self.model_combo.pack(side='left', padx=(10, 0))
        
        # Индикатор состояния модели
        self.model_status_label = tk.Label(
            model_frame,
            text="⏳ Проверка...",
            font=self.button_font,
            bg='#ecf0f1',
            fg='#e67e22'
        )
        self.model_status_label.pack(side='left', padx=(10, 0))
        
        # Поле ввода промпта
        prompt_frame = tk.Frame(parent, bg='#ecf0f1')
        prompt_frame.pack(fill='x', pady=(0, 10))
        
        prompt_label = tk.Label(
            prompt_frame,
            text="Введите промпт:",
            font=self.button_font,
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        prompt_label.pack(anchor='w', pady=(0, 5))
        
        self.prompt_text = scrolledtext.ScrolledText(
            prompt_frame,
            height=4,
            font=self.text_font,
            wrap=tk.WORD
        )
        self.prompt_text.pack(fill='x')
        
        # Кнопки генерации
        generate_buttons_frame = tk.Frame(parent, bg='#ecf0f1')
        generate_buttons_frame.pack(fill='x', pady=(0, 10))
        
        self.generate_btn = tk.Button(
            generate_buttons_frame,
            text="🚀 Сгенерировать ответ",
            font=self.button_font,
            command=self.generate_response,
            bg='#27ae60',
            fg='white',
            relief='flat',
            padx=20,
            pady=10
        )
        self.generate_btn.pack(side='left', padx=(0, 10))
        
        self.clear_btn = tk.Button(
            generate_buttons_frame,
            text="🗑️ Очистить",
            font=self.button_font,
            command=self.clear_texts,
            bg='#95a5a6',
            fg='white',
            relief='flat',
            padx=20,
            pady=10
        )
        self.clear_btn.pack(side='left')
        
        # Поле вывода ответа
        response_frame = tk.Frame(parent, bg='#ecf0f1')
        response_frame.pack(fill='both', expand=True)
        
        response_label = tk.Label(
            response_frame,
            text="Ответ ИИ: (Ctrl+C - копировать, Ctrl+A - выделить все, ПКМ - меню)",
            font=self.button_font,
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        response_label.pack(anchor='w', pady=(0, 5))
        
        self.response_text = scrolledtext.ScrolledText(
            response_frame,
            height=15,
            font=self.text_font,
            wrap=tk.WORD,
            state='disabled'
        )
        self.response_text.pack(fill='both', expand=True)
        
        # Добавляем функциональность копирования
        self.setup_copy_functionality()
    
    def setup_copy_functionality(self):
        """Настраивает функциональность копирования для поля ответа"""
        # Привязываем комбинации клавиш
        self.response_text.bind('<Control-c>', self.copy_text)
        self.response_text.bind('<Control-C>', self.copy_text)
        self.response_text.bind('<Control-a>', self.select_all_text)
        self.response_text.bind('<Control-A>', self.select_all_text)
        
        # Привязываем правый клик для контекстного меню
        self.response_text.bind('<Button-3>', self.show_context_menu)
        
        # Создаем контекстное меню
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Копировать (Ctrl+C)", command=self.copy_text)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Выделить все (Ctrl+A)", command=self.select_all_text)
    
    def copy_text(self, event=None):
        """Копирует выделенный текст в буфер обмена"""
        try:
            # Получаем выделенный текст
            selected_text = self.response_text.get(tk.SEL_FIRST, tk.SEL_LAST)
            if selected_text:
                # Копируем в буфер обмена
                self.root.clipboard_clear()
                self.root.clipboard_append(selected_text)
                self.update_status("✅ Текст скопирован в буфер обмена")
            else:
                # Если ничего не выделено, копируем весь текст
                all_text = self.response_text.get("1.0", tk.END).strip()
                if all_text:
                    self.root.clipboard_clear()
                    self.root.clipboard_append(all_text)
                    self.update_status("✅ Весь ответ скопирован в буфер обмена")
                else:
                    self.update_status("⚠️ Нет текста для копирования")
        except tk.TclError:
            # Если ничего не выделено, копируем весь текст
            all_text = self.response_text.get("1.0", tk.END).strip()
            if all_text:
                self.root.clipboard_clear()
                self.root.clipboard_append(all_text)
                self.update_status("✅ Весь ответ скопирован в буфер обмена")
            else:
                self.update_status("⚠️ Нет текста для копирования")
        except Exception as e:
            logger.error(f"Ошибка копирования: {e}")
            self.update_status("❌ Ошибка копирования")
    
    def select_all_text(self):
        """Выделяет весь текст в поле ответа"""
        try:
            self.response_text.tag_add(tk.SEL, "1.0", tk.END)
            self.response_text.mark_set(tk.INSERT, "1.0")
            self.response_text.see(tk.INSERT)
            self.update_status("✅ Весь текст выделен")
        except Exception as e:
            logger.error(f"Ошибка выделения текста: {e}")
            self.update_status("❌ Ошибка выделения текста")
    
    def show_context_menu(self, event):
        """Показывает контекстное меню при правом клике"""
        try:
            # Показываем меню в позиции клика
            self.context_menu.tk_popup(event.x_root, event.y_root)
        except Exception as e:
            logger.error(f"Ошибка показа контекстного меню: {e}")
    
    def create_status_bar(self):
        """Создает статус-бар"""
        self.status_var = tk.StringVar()
        self.status_var.set("Готов к работе")
        
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor='w',
            bg='#bdc3c7',
            fg='#2c3e50',
            font=self.text_font
        )
        status_bar.pack(side='bottom', fill='x')
    
    def load_models(self):
        """Загружает модели ИИ"""
        try:
            self.update_status("Загрузка моделей...")
            logger.info(f"Ищем модели в: {self.MODELS_DIR}")
            
            # Проверяем наличие обученной модели
            trained_model_path = self.MODELS_DIR / "history_ai_trained"
            logger.info(f"Путь к модели: {trained_model_path}")
            logger.info(f"Модель существует: {trained_model_path.exists()}")
            
            if trained_model_path.exists():
                # Проверяем содержимое директории модели
                model_files = list(trained_model_path.glob("*"))
                logger.info(f"Файлы в модели: {len(model_files)}")
                
                # Обновляем визуальный индикатор
                self.model_status_label.config(text="✅ Готова", fg='#27ae60')
                
                self.update_status("✅ Обученная модель найдена и готова к работе")
                logger.info("Обученная модель найдена и готова к работе")
            else:
                # Обновляем визуальный индикатор
                self.model_status_label.config(text="❌ Не найдена", fg='#e74c3c')
                
                self.update_status("⚠️ Обученная модель не найдена")
                logger.warning("Обученная модель не найдена")
                logger.warning(f"Ожидаемый путь: {trained_model_path}")
                
        except Exception as e:
            logger.error(f"Ошибка загрузки моделей: {e}")
            self.update_status(f"❌ Ошибка загрузки моделей: {e}")
    
    def upload_file(self):
        """Загружает файлы в папку data/raw"""
        try:
            file_paths = filedialog.askopenfilenames(
                title="Выберите файлы для загрузки (можно выбрать несколько)",
                filetypes=[
                    ("Все файлы", "*.*"),
                    ("Текстовые файлы", "*.txt"),
                    ("CSV файлы", "*.csv"),
                    ("JSON файлы", "*.json"),
                    ("PDF файлы", "*.pdf"),
                    ("Word документы", "*.doc;*.docx"),
                    ("DJVU файлы", "*.djvu"),
                    ("FB2 книги", "*.fb2"),
                    ("Документы", "*.doc;*.docx;*.pdf;*.djvu;*.fb2")
                ]
            )
            
            if file_paths:
                import shutil
                uploaded_files = []
                failed_files = []
                
                for file_path in file_paths:
                    try:
                        filename = os.path.basename(file_path)
                        dest_path = self.DATA_DIR / "raw" / filename
                        
                        # Проверяем, не существует ли уже файл с таким именем
                        if dest_path.exists():
                            # Добавляем номер к имени файла
                            base_name = dest_path.stem
                            extension = dest_path.suffix
                            counter = 1
                            while dest_path.exists():
                                new_name = f"{base_name}_{counter}{extension}"
                                dest_path = self.DATA_DIR / "raw" / new_name
                                counter += 1
                        
                        # Копируем файл
                        shutil.copy2(file_path, dest_path)
                        uploaded_files.append(filename)
                        
                    except Exception as e:
                        failed_files.append(f"{os.path.basename(file_path)}: {e}")
                        logger.error(f"Ошибка загрузки файла {file_path}: {e}")
                
                # Показываем результат
                if uploaded_files:
                    success_message = f"✅ Успешно загружено файлов: {len(uploaded_files)}\n\n"
                    success_message += "📁 Загруженные файлы:\n"
                    for filename in uploaded_files:
                        success_message += f"  • {filename}\n"
                    
                    if failed_files:
                        success_message += f"\n❌ Ошибки загрузки ({len(failed_files)} файлов):\n"
                        for error in failed_files:
                            success_message += f"  • {error}\n"
                    
                    success_message += f"\n💡 Совет: После загрузки файлов используйте\n"
                    success_message += f"кнопку 'Переобучить модели' для улучшения качества ответов."
                    
                    messagebox.showinfo("Результат загрузки", success_message)
                    self.refresh_file_list()
                    self.update_status(f"Загружено {len(uploaded_files)} файлов")
                else:
                    messagebox.showerror("Ошибка", "Не удалось загрузить ни одного файла!")
                
        except Exception as e:
            logger.error(f"Ошибка загрузки файлов: {e}")
            messagebox.showerror("Ошибка", f"Не удалось загрузить файлы:\n{e}")
    
    def refresh_file_list(self):
        """Обновляет список файлов"""
        try:
            # Очищаем список
            for item in self.files_tree.get_children():
                self.files_tree.delete(item)
            
            # Загружаем файлы из data/raw
            raw_dir = self.DATA_DIR / "raw"
            if raw_dir.exists():
                for file_path in raw_dir.iterdir():
                    if file_path.is_file():
                        # Получаем информацию о файле
                        size = self.format_file_size(file_path.stat().st_size)
                        date = file_path.stat().st_mtime
                        date_str = self.format_date(date)
                        
                        # Добавляем в список
                        self.files_tree.insert(
                            '',
                            'end',
                            text=file_path.name,
                            values=(size, date_str)
                        )
            
            self.update_status("Список файлов обновлен")
            
        except Exception as e:
            logger.error(f"Ошибка обновления списка файлов: {e}")
            self.update_status(f"Ошибка обновления списка: {e}")
    
    def format_file_size(self, size_bytes):
        """Форматирует размер файла"""
        if size_bytes < 1024:
            return f"{size_bytes} Б"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} КБ"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} МБ"
    
    def format_date(self, timestamp):
        """Форматирует дату"""
        import datetime
        return datetime.datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y %H:%M")
    
    def on_file_double_click(self, event):
        """Обработчик двойного клика по файлу"""
        try:
            selection = self.files_tree.selection()
            if selection:
                item = self.files_tree.item(selection[0])
                filename = item['text']
                file_path = self.DATA_DIR / "raw" / filename
                
                if file_path.exists():
                    # Показываем информацию о файле
                    stat = file_path.stat()
                    size = self.format_file_size(stat.st_size)
                    date = self.format_date(stat.st_mtime)
                    
                    messagebox.showinfo(
                        "Информация о файле",
                        f"📁 Файл: {filename}\n"
                        f"📏 Размер: {size}\n"
                        f"📅 Дата изменения: {date}\n"
                        f"📍 Путь: {file_path}"
                    )
                else:
                    messagebox.showerror("Ошибка", f"Файл '{filename}' не найден!")
                    
        except Exception as e:
            logger.error(f"Ошибка получения информации о файле: {e}")
            messagebox.showerror("Ошибка", f"Ошибка получения информации о файле:\n{e}")
    
    def open_data_folder(self):
        """Открывает папку с данными"""
        try:
            raw_dir = self.DATA_DIR / "raw"
            if raw_dir.exists():
                os.startfile(str(raw_dir))
            else:
                messagebox.showwarning("Предупреждение", "Папка с данными не найдена!")
        except Exception as e:
            logger.error(f"Ошибка открытия папки: {e}")
            messagebox.showerror("Ошибка", f"Не удалось открыть папку:\n{e}")
    
    def retrain_models(self):
        """Переобучает модели"""
        try:
            # Спрашиваем пользователя о выборе модели
            choice = messagebox.askyesnocancel(
                "Переобучение моделей",
                "🎓 Переобучение моделей\n\n"
                "Выберите модель для переобучения:\n\n"
                "• ДА - переобучить английскую модель\n"
                "• НЕТ - переобучить русскую модель\n"
                "• ОТМЕНА - отменить операцию"
            )
            
            if choice is None:  # Отмена
                return
            elif choice:  # Английская модель
                self.retrain_english_model()
            else:  # Русская модель
                self.retrain_russian_model()
                
        except Exception as e:
            logger.error(f"Ошибка переобучения: {e}")
            messagebox.showerror("Ошибка", f"Ошибка переобучения:\n{e}")
    
    def retrain_english_model(self):
        """Переобучает английскую модель"""
        def train_thread():
            try:
                self.retrain_btn.config(state='disabled')
                self.progress_frame.pack(fill='x', pady=(10, 0))
                self.progress_bar['value'] = 0
                self.progress_percent.config(text="0%")
                
                self.update_status("Начинаем переобучение английской модели...")
                self.update_progress(10, "Подготовка данных...")
                
                # Запускаем скрипт инкрементального обучения
                script_path = self.SRC_DIR / "train_model_incremental.py"
                if script_path.exists():
                    result = subprocess.run(
                        [sys.executable, str(script_path), "--data", str(self.DATA_DIR / "raw"), "--epochs", "1", "--model", "distilgpt2"],
                        cwd=str(self.BASE_DIR),
                        capture_output=True,
                        text=True,
                        encoding='utf-8',
                        errors='replace'
                    )
                    
                    if result.returncode == 0:
                        self.update_progress(100, "Переобучение завершено!")
                        self.update_status("Английская модель переобучена успешно")
                        # Выводим информацию о процессе в консоль
                        print(f"\n{'='*60}")
                        print("ПЕРЕОБУЧЕНИЕ АНГЛИЙСКОЙ МОДЕЛИ ЗАВЕРШЕНО")
                        print(f"{'='*60}")
                        print("Вывод скрипта:")
                        print(result.stdout)
                        print(f"{'='*60}")
                        messagebox.showinfo("Успех", "Английская модель переобучена успешно!")
                    else:
                        error_msg = result.stderr if result.stderr else "Неизвестная ошибка"
                        print(f"\n{'='*60}")
                        print("ОШИБКА ПЕРЕОБУЧЕНИЯ АНГЛИЙСКОЙ МОДЕЛИ")
                        print(f"{'='*60}")
                        print("Ошибка:", error_msg)
                        print("Вывод:", result.stdout)
                        print(f"{'='*60}")
                        raise Exception(f"Ошибка обучения: {error_msg}")
                else:
                    raise Exception("Скрипт инкрементального обучения не найден")
                    
            except Exception as e:
                logger.error(f"Ошибка переобучения английской модели: {e}")
                messagebox.showerror("Ошибка", f"Ошибка переобучения:\n{e}")
                self.update_status(f"❌ Ошибка переобучения: {e}")
            finally:
                self.retrain_btn.config(state='normal')
                self.progress_frame.pack_forget()
        
        thread = threading.Thread(target=train_thread, daemon=True)
        thread.start()
    
    def retrain_russian_model(self):
        """Переобучает русскую модель"""
        def train_thread():
            try:
                self.retrain_btn.config(state='disabled')
                self.progress_frame.pack(fill='x', pady=(10, 0))
                self.progress_bar['value'] = 0
                self.progress_percent.config(text="0%")
                
                self.update_status("Начинаем переобучение русской модели...")
                self.update_progress(10, "Подготовка данных...")
                
                # Запускаем скрипт инкрементального обучения русской модели
                script_path = self.SRC_DIR / "train_model_incremental.py"
                if script_path.exists():
                    result = subprocess.run(
                        [sys.executable, str(script_path), "--data", str(self.DATA_DIR / "raw"), "--epochs", "1", "--model", "ai-forever/rugpt3small_based_on_gpt2"],
                        cwd=str(self.BASE_DIR),
                        capture_output=True,
                        text=True,
                        encoding='utf-8',
                        errors='replace'
                    )
                    
                    if result.returncode == 0:
                        self.update_progress(100, "Переобучение завершено!")
                        self.update_status("Русская модель переобучена успешно")
                        # Выводим информацию о процессе в консоль
                        print(f"\n{'='*60}")
                        print("ПЕРЕОБУЧЕНИЕ РУССКОЙ МОДЕЛИ ЗАВЕРШЕНО")
                        print(f"{'='*60}")
                        print("Вывод скрипта:")
                        print(result.stdout)
                        print(f"{'='*60}")
                        messagebox.showinfo("Успех", "Русская модель переобучена успешно!")
                    else:
                        error_msg = result.stderr if result.stderr else "Неизвестная ошибка"
                        print(f"\n{'='*60}")
                        print("ОШИБКА ПЕРЕОБУЧЕНИЯ РУССКОЙ МОДЕЛИ")
                        print(f"{'='*60}")
                        print("Ошибка:", error_msg)
                        print("Вывод:", result.stdout)
                        print(f"{'='*60}")
                        raise Exception(f"Ошибка обучения: {error_msg}")
                else:
                    raise Exception("Скрипт инкрементального обучения не найден")
                    
            except Exception as e:
                logger.error(f"Ошибка переобучения русской модели: {e}")
                messagebox.showerror("Ошибка", f"Ошибка переобучения:\n{e}")
                self.update_status(f"❌ Ошибка переобучения: {e}")
            finally:
                self.retrain_btn.config(state='normal')
                self.progress_frame.pack_forget()
        
        thread = threading.Thread(target=train_thread, daemon=True)
        thread.start()
    
    def update_progress(self, value, message):
        """Обновляет прогресс-бар"""
        self.progress_bar['value'] = value
        self.progress_percent.config(text=f"{value}%")
        self.update_status(message)
        self.root.update_idletasks()
    
    def generate_response(self):
        """Генерирует ответ на основе промпта"""
        try:
            prompt = self.prompt_text.get("1.0", tk.END).strip()
            if not prompt:
                messagebox.showwarning("Предупреждение", "Введите промпт для генерации!")
                return
            
            model_type = self.model_var.get()
            
            # Используем обученную модель
            model_path = "models/history_ai_trained"
            model_display_name = "обученной"
            
            self.update_status(f"Генерация ответа с помощью {model_display_name} модели...")
            
            # Запускаем генерацию в отдельном потоке
            def generate_thread():
                try:
                    self.generate_btn.config(state='disabled')
                    
                    # Запускаем скрипт генерации
                    script_path = self.SRC_DIR / "generate_text.py"
                    if script_path.exists():
                        # Устанавливаем переменные окружения для правильной кодировки
                        env = os.environ.copy()
                        env['PYTHONIOENCODING'] = 'utf-8'
                        env['PYTHONUTF8'] = '1'
                        
                        result = subprocess.run(
                            [sys.executable, str(script_path), "--prompt", prompt, "--model", model_path],
                            cwd=str(self.BASE_DIR),
                            capture_output=True,
                            text=True,
                            encoding='utf-8',
                            errors='replace',
                            env=env
                        )
                        
                        if result.returncode == 0:
                            # Извлекаем ответ ИИ из нового формата вывода
                            output_lines = result.stdout.strip().split('\n')
                            response = ""
                            in_answer_section = False
                            
                            for line in output_lines:
                                if line.startswith("ОТВЕТ ИИ:"):
                                    in_answer_section = True
                                    continue
                                elif line.startswith("="*60) and in_answer_section:
                                    break
                                elif in_answer_section and line.strip():
                                    response += line + "\n"
                            
                            if not response:
                                response = result.stdout.strip()
                            
                            # Дополнительная очистка кодировки
                            if response:
                                try:
                                    # Пытаемся исправить кодировку
                                    response = response.encode('utf-8', errors='ignore').decode('utf-8')
                                except:
                                    pass
                            
                            # Выводим ответ в консоль
                            print(f"\n{'='*60}")
                            print(f"ОТВЕТ ИИ (из интерфейса):")
                            print(f"{'='*60}")
                            print(response)
                            print(f"{'='*60}")
                            print(f"Длина ответа: {len(response)} символов")
                            print(f"{'='*60}")
                            
                            self.root.after(0, lambda: self.display_response(response))
                            self.update_status("Ответ сгенерирован и выведен в консоль")
                        else:
                            raise Exception(f"Ошибка генерации: {result.stderr}")
                    else:
                        raise Exception("Скрипт генерации не найден")
                        
                except Exception as e:
                    error_msg = str(e)
                    logger.error(f"Ошибка генерации: {error_msg}")
                    self.root.after(0, lambda: messagebox.showerror("Ошибка", f"Ошибка генерации:\n{error_msg}"))
                    self.root.after(0, lambda: self.update_status(f"❌ Ошибка генерации: {error_msg}"))
                finally:
                    self.root.after(0, lambda: self.generate_btn.config(state='normal'))
            
            thread = threading.Thread(target=generate_thread, daemon=True)
            thread.start()
            
        except Exception as e:
            logger.error(f"Ошибка генерации: {e}")
            messagebox.showerror("Ошибка", f"Ошибка генерации:\n{e}")
    
    def display_response(self, response):
        """Отображает ответ в текстовом поле"""
        self.response_text.config(state='normal')
        self.response_text.delete("1.0", tk.END)
        self.response_text.insert("1.0", response)
        self.response_text.config(state='disabled')
    
    def clear_texts(self):
        """Очищает поля ввода и вывода"""
        self.prompt_text.delete("1.0", tk.END)
        self.response_text.config(state='normal')
        self.response_text.delete("1.0", tk.END)
        self.response_text.config(state='disabled')
        self.update_status("Поля очищены")
    
    def test_model(self):
        """Тестирует качество обученной модели"""
        try:
            # Проверяем наличие обученных моделей
            english_model_path = self.MODELS_DIR / "english_model"
            russian_model_path = self.MODELS_DIR / "russian_model"
            
            available_models = []
            if english_model_path.exists():
                available_models.append(("Английская модель", str(english_model_path), "english"))
            if russian_model_path.exists():
                available_models.append(("Русская модель", str(russian_model_path), "russian"))
            
            if not available_models:
                messagebox.showwarning("Предупреждение", 
                    "Не найдено обученных моделей!\n\n"
                    "Сначала обучите модели с помощью кнопки 'Переобучить модели'.")
                return
            
            # Выбираем модель для тестирования
            if len(available_models) == 1:
                model_name, model_path, model_type = available_models[0]
            else:
                # Показываем диалог выбора модели
                from tkinter import simpledialog
                choice = simpledialog.askstring(
                    "Выбор модели",
                    "Выберите модель для тестирования:\n"
                    "1 - Английская модель\n"
                    "2 - Русская модель\n\n"
                    "Введите номер (1 или 2):"
                )
                
                if choice == "1" and any(m[2] == "english" for m in available_models):
                    model_name, model_path, model_type = next(m for m in available_models if m[2] == "english")
                elif choice == "2" and any(m[2] == "russian" for m in available_models):
                    model_name, model_path, model_type = next(m for m in available_models if m[2] == "russian")
                else:
                    return
            
            self.update_status(f"Тестируем {model_name}...")
            self.test_btn.config(state='disabled')
            
            # Запускаем тест в отдельном потоке
            def test_thread():
                try:
                    # Запускаем скрипт тестирования
                    script_path = self.SRC_DIR / "quick_model_test.py"
                    if script_path.exists():
                        result = subprocess.run(
                            [sys.executable, str(script_path), model_path, "--type", model_type],
                            cwd=str(self.BASE_DIR),
                            capture_output=True,
                            text=True,
                            encoding='utf-8'
                        )
                        
                        if result.returncode == 0:
                            # Парсим результат
                            output = result.stdout
                            if "ОТЛИЧНО" in output:
                                message = f"🎉 {model_name} отлично изучила материалы!"
                            elif "ХОРОШО" in output:
                                message = f"👍 {model_name} хорошо изучила материалы!"
                            elif "УДОВЛЕТВОРИТЕЛЬНО" in output:
                                message = f"⚠️ {model_name} частично изучила материалы"
                            else:
                                message = f"❌ {model_name} слабо изучила материалы"
                            
                            messagebox.showinfo("Результат теста", 
                                f"{message}\n\n"
                                f"Подробные результаты:\n{output}")
                            self.update_status(f"Тест {model_name} завершен")
                        else:
                            error_msg = result.stderr or "Неизвестная ошибка"
                            messagebox.showerror("Ошибка тестирования", 
                                f"Ошибка при тестировании модели:\n{error_msg}")
                            self.update_status("Ошибка тестирования модели")
                    else:
                        messagebox.showerror("Ошибка", "Скрипт тестирования не найден!")
                        self.update_status("Скрипт тестирования не найден")
                        
                except Exception as e:
                    logger.error(f"Ошибка тестирования модели: {e}")
                    messagebox.showerror("Ошибка", f"Ошибка тестирования модели:\n{e}")
                    self.update_status("Ошибка тестирования модели")
                finally:
                    self.test_btn.config(state='normal')
            
            # Запускаем тест в отдельном потоке
            import threading
            thread = threading.Thread(target=test_thread, daemon=True)
            thread.start()
            
        except Exception as e:
            logger.error(f"Ошибка запуска теста модели: {e}")
            messagebox.showerror("Ошибка", f"Не удалось запустить тест модели:\n{e}")
            self.update_status("Ошибка запуска теста")

    def update_status(self, message):
        """Обновляет статус-бар"""
        self.status_var.set(message)
        logger.info(message)
    
    def run(self):
        """Запускает приложение"""
        self.root.mainloop()

def main():
    """Главная функция"""
    try:
        app = UniversalHistoryInterface()
        app.run()
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        messagebox.showerror("Критическая ошибка", f"Не удалось запустить приложение:\n{e}")

if __name__ == "__main__":
    main()
