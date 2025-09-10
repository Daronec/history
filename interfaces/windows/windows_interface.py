#!/usr/bin/env python3
"""
Базовый Windows интерфейс для ИИ-История
Упрощенная версия для совместимости с документацией
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
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
        pass

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

class HistoryInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_ui()
        self.load_models()
        
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        self.root.title("ИИ для изучения истории")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Создание основного фрейма
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настройка сетки
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="🏛️ ИИ для изучения истории", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Поле ввода промпта
        ttk.Label(main_frame, text="Введите промпт:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.prompt_entry = tk.Text(main_frame, height=3, width=50)
        self.prompt_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Кнопки
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        self.generate_button = ttk.Button(button_frame, text="Сгенерировать ответ", 
                                         command=self.generate_text)
        self.generate_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_button = ttk.Button(button_frame, text="Очистить", 
                                      command=self.clear_text)
        self.clear_button.pack(side=tk.LEFT)
        
        # Поле результата
        ttk.Label(main_frame, text="Результат:").grid(row=3, column=0, sticky=tk.W, pady=(20, 5))
        self.result_text = scrolledtext.ScrolledText(main_frame, height=15, width=70)
        self.result_text.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Статус
        self.status_label = ttk.Label(main_frame, text="Готов к работе")
        self.status_label.grid(row=5, column=0, columnspan=2, pady=(10, 0))
        
    def load_models(self):
        """Загрузка моделей"""
        self.status_label.config(text="Загрузка моделей...")
        self.root.update()
        
        try:
            # Добавляем путь к src
            sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))
            
            # Импортируем модель
            from models.history_ai import HistoryAIModel
            
            # Загружаем модель
            self.model = HistoryAIModel()
            self.model.load_trained_model('../../models/history_ai_trained')
            
            self.status_label.config(text="✅ Модель загружена и готова к работе")
            logger.info("Модель успешно загружена")
            
        except Exception as e:
            self.status_label.config(text=f"❌ Ошибка загрузки модели: {str(e)}")
            logger.error(f"Ошибка загрузки модели: {e}")
            self.model = None
    
    def generate_text(self):
        """Генерация текста"""
        if not self.model:
            messagebox.showerror("Ошибка", "Модель не загружена!")
            return
            
        prompt = self.prompt_entry.get("1.0", tk.END).strip()
        if not prompt:
            messagebox.showwarning("Предупреждение", "Введите промпт!")
            return
            
        # Показываем статус
        self.status_label.config(text="Генерация текста...")
        self.generate_button.config(state='disabled')
        self.root.update()
        
        def generate():
            try:
                result = self.model.generate_text(prompt, max_length=150, temperature=0.7)
                
                # Обновляем UI в главном потоке
                self.root.after(0, lambda: self.show_result(result))
                
            except Exception as e:
                self.root.after(0, lambda: self.show_error(str(e)))
        
        # Запускаем генерацию в отдельном потоке
        thread = threading.Thread(target=generate)
        thread.daemon = True
        thread.start()
    
    def show_result(self, result):
        """Показ результата"""
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", result)
        self.status_label.config(text="✅ Генерация завершена")
        self.generate_button.config(state='normal')
    
    def show_error(self, error):
        """Показ ошибки"""
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", f"Ошибка: {error}")
        self.status_label.config(text="❌ Ошибка генерации")
        self.generate_button.config(state='normal')
    
    def clear_text(self):
        """Очистка текста"""
        self.prompt_entry.delete("1.0", tk.END)
        self.result_text.delete("1.0", tk.END)
        self.status_label.config(text="Готов к работе")
    
    def run(self):
        """Запуск интерфейса"""
        logger.info("Запуск Windows интерфейса")
        self.root.mainloop()

def main():
    """Главная функция"""
    try:
        # Создаем папку для логов
        os.makedirs('logs', exist_ok=True)
        
        # Запускаем интерфейс
        app = HistoryInterface()
        app.run()
        
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        messagebox.showerror("Критическая ошибка", f"Не удалось запустить приложение: {e}")

if __name__ == "__main__":
    main()
