#!/usr/bin/env python3
"""
Быстрый старт для ИИ проекта изучения истории
"""

import os
import sys
from pathlib import Path

def main():
    print("🏛️ Добро пожаловать в ИИ проект для изучения истории!")
    print("=" * 60)
    
    # Проверяем, установлены ли зависимости
    try:
        import torch
        import transformers
        print("✅ Основные библиотеки уже установлены")
    except ImportError:
        print("❌ Необходимо установить зависимости")
        print("Запустите: python setup_ai.py")
        return
    
    # Проверяем структуру проекта
    required_dirs = ["src", "notebooks", "data", "models"]
    missing_dirs = [d for d in required_dirs if not os.path.exists(d)]
    
    if missing_dirs:
        print(f"❌ Отсутствуют папки: {', '.join(missing_dirs)}")
        print("Запустите: python setup_ai.py")
        return
    
    print("✅ Структура проекта готова")
    
    # Показываем меню
    while True:
        print("\n🎯 Что вы хотите сделать?")
        print("1. 🚀 Запустить Jupyter Notebook")
        print("2. 🤖 Обучить модель на примерах")
        print("3. 📝 Сгенерировать исторический текст")
        print("4. 📊 Показать структуру проекта")
        print("5. ❌ Выход")
        
        choice = input("\nВведите номер (1-5): ").strip()
        
        if choice == "1":
            print("\n🚀 Запускаем Jupyter Notebook...")
            os.system("jupyter notebook notebooks/getting_started.ipynb")
            
        elif choice == "2":
            print("\n🤖 Обучаем модель на примерах...")
            os.system("python src/train_model.py --data sample --task generation --epochs 2")
            
        elif choice == "3":
            print("\n📝 Генерируем исторический текст...")
            try:
                from src.models.history_ai import HistoryAIModel
                
                print("Загружаем модель...")
                ai_model = HistoryAIModel()
                ai_model.load_model("generation")
                
                prompt = input("Введите промпт (например: 'В 1812 году произошло'): ")
                if not prompt:
                    prompt = "В истории России важным событием было"
                
                result = ai_model.generate_text(prompt, max_length=150)
                print(f"\n🎯 Промпт: {prompt}")
                print(f"📝 Результат: {result}")
                
            except Exception as e:
                print(f"❌ Ошибка: {e}")
                
        elif choice == "4":
            print("\n📊 Структура проекта:")
            for root, dirs, files in os.walk("."):
                level = root.replace(".", "").count(os.sep)
                indent = " " * 2 * level
                print(f"{indent}{os.path.basename(root)}/")
                subindent = " " * 2 * (level + 1)
                for file in files[:5]:  # Показываем только первые 5 файлов
                    print(f"{subindent}{file}")
                if len(files) > 5:
                    print(f"{subindent}... и еще {len(files) - 5} файлов")
                    
        elif choice == "5":
            print("\n👋 До свидания!")
            break
            
        else:
            print("❌ Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
