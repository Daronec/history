#!/usr/bin/env python3
"""
Демонстрационный скрипт для ИИ проекта изучения истории
"""

import os
import sys
from pathlib import Path

def main():
    print("🏛️ Добро пожаловать в ИИ проект для изучения истории!")
    print("=" * 60)
    
    # Проверяем установку
    try:
        from src.models.history_ai import HistoryAIModel
        print("✅ ИИ модель готова к работе")
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("Убедитесь, что вы активировали виртуальное окружение:")
        print("venv\\Scripts\\activate")
        return
    
    # Показываем меню
    while True:
        print("\n🎯 Что вы хотите сделать?")
        print("1. 🤖 Протестировать генерацию текста")
        print("2. 📊 Показать примеры исторических данных")
        print("3. 🌐 Открыть Jupyter Notebook")
        print("4. 📁 Показать структуру проекта")
        print("5. ❌ Выход")
        
        choice = input("\nВведите номер (1-5): ").strip()
        
        if choice == "1":
            test_generation()
            
        elif choice == "2":
            show_sample_data()
            
        elif choice == "3":
            print("\n🌐 Открываем Jupyter Notebook...")
            print("Скопируйте и вставьте в браузер:")
            print("http://localhost:8888/tree?token=a8927eac24643dc899a351f3ccda4923c7511f5d08ba7847")
            print("\nИли откройте файл:")
            print("notebooks/getting_started.ipynb")
            
        elif choice == "4":
            show_project_structure()
            
        elif choice == "5":
            print("\n👋 До свидания!")
            break
            
        else:
            print("❌ Неверный выбор. Попробуйте снова.")

def test_generation():
    """Тестирует генерацию текста"""
    print("\n🤖 Тестируем генерацию исторических текстов...")
    print("=" * 50)
    
    try:
        # Создаем модель
        ai_model = HistoryAIModel(model_name="distilgpt2")
        ai_model.load_model("generation")
        
        # Примеры промптов
        prompts = [
            "В 1812 году произошло важное событие:",
            "Петр I известен тем, что",
            "В истории России важную роль сыграл",
            "Революция 1917 года привела к"
        ]
        
        for i, prompt in enumerate(prompts, 1):
            print(f"\n{i}. Промпт: {prompt}")
            try:
                result = ai_model.generate_text(prompt, max_length=80, temperature=0.7)
                print(f"   Результат: {result}")
            except Exception as e:
                print(f"   ❌ Ошибка: {e}")
        
        # Интерактивный режим
        print("\n🎮 Интерактивный режим:")
        print("Введите свой промпт (или 'выход' для завершения):")
        
        while True:
            user_prompt = input("\nВаш промпт: ").strip()
            if user_prompt.lower() in ['выход', 'exit', 'quit']:
                break
            
            if user_prompt:
                try:
                    result = ai_model.generate_text(user_prompt, max_length=100, temperature=0.7)
                    print(f"Результат: {result}")
                except Exception as e:
                    print(f"❌ Ошибка: {e}")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")

def show_sample_data():
    """Показывает примеры исторических данных"""
    print("\n📊 Примеры исторических данных:")
    print("=" * 50)
    
    sample_data = [
        {
            "text": "В 1812 году Наполеон Бонапарт вторгся в Россию с армией в 600 тысяч человек. Это событие стало началом Отечественной войны 1812 года.",
            "period": "XIX век",
            "category": "война"
        },
        {
            "text": "Петр I Великий провел масштабные реформы в России, включая создание регулярной армии и флота, а также основание Санкт-Петербурга в 1703 году.",
            "period": "XVIII век", 
            "category": "реформы"
        },
        {
            "text": "В 988 году князь Владимир крестил Русь, приняв христианство из Византии. Это событие оказало огромное влияние на развитие русской культуры.",
            "period": "X век",
            "category": "религия"
        }
    ]
    
    for i, item in enumerate(sample_data, 1):
        print(f"\n{i}. {item['period']} - {item['category']}")
        print(f"   {item['text']}")
    
    print(f"\n📁 Всего примеров: {len(sample_data)}")
    print("💡 Вы можете добавить свои данные в файл data/raw/sample_history_data.json")

def show_project_structure():
    """Показывает структуру проекта"""
    print("\n📁 Структура проекта:")
    print("=" * 50)
    
    structure = {
        "src/": "Исходный код",
        "├── models/": "Модели ИИ",
        "│   └── history_ai.py": "Основная модель",
        "└── train_model.py": "Скрипт обучения",
        "notebooks/": "Jupyter notebooks",
        "├── getting_started.ipynb": "Интерактивный tutorial",
        "data/": "Данные",
        "├── raw/": "Исходные данные",
        "└── processed/": "Обработанные данные",
        "models/": "Сохраненные модели",
        "logs/": "Логи обучения",
        "requirements.txt": "Зависимости",
        "setup_ai.py": "Скрипт установки",
        "demo.py": "Демонстрационный скрипт"
    }
    
    for path, description in structure.items():
        print(f"{path:<25} - {description}")
    
    print(f"\n📊 Статистика:")
    print(f"Всего файлов: {count_files()}")
    print(f"Размер проекта: {get_project_size()}")

def count_files():
    """Подсчитывает количество файлов в проекте"""
    count = 0
    for root, dirs, files in os.walk("."):
        count += len(files)
    return count

def get_project_size():
    """Получает размер проекта"""
    total_size = 0
    for root, dirs, files in os.walk("."):
        for file in files:
            try:
                total_size += os.path.getsize(os.path.join(root, file))
            except:
                pass
    
    # Конвертируем в MB
    size_mb = total_size / (1024 * 1024)
    return f"{size_mb:.1f} MB"

if __name__ == "__main__":
    main()

