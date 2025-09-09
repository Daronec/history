#!/usr/bin/env python3
"""
Тестирование генерации текста на русском языке
"""

import sys
import os
sys.path.append('src')

from models.history_ai_ru import HistoryAIModelRU

def test_russian_generation():
    """Тестирует генерацию текста на русском языке"""
    print("🇷🇺 Тестируем генерацию текста на русском языке...")
    print("=" * 60)
    
    try:
        # Загружаем русскую модель
        ai_model = HistoryAIModelRU()
        ai_model.load_model('generation')
        
        # Тестовые промпты на русском языке
        prompts = [
            "В 1812 году произошло важное событие:",
            "Петр I известен тем, что",
            "В истории России важную роль сыграл",
            "Революция 1917 года привела к",
            "Реформы Петра I включали",
            "В XVIII веке в России",
            "Сталин родился в",
            "Великая Отечественная война началась",
            "Крещение Руси произошло в",
            "Иван Грозный правил"
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
        print("Введите свой промпт на русском языке (или 'выход' для завершения):")
        
        while True:
            try:
                user_prompt = input("\nВаш промпт: ").strip()
                if user_prompt.lower() in ['выход', 'exit', 'quit']:
                    break
                
                if user_prompt:
                    result = ai_model.generate_text(user_prompt, max_length=100, temperature=0.7)
                    print(f"Результат: {result}")
            except KeyboardInterrupt:
                print("\n\n👋 До свидания!")
                break
            except Exception as e:
                print(f"❌ Ошибка: {e}")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        print("💡 Попробуйте сначала обучить русскую модель:")
        print("   python train_model_ru.py")

if __name__ == "__main__":
    test_russian_generation()
