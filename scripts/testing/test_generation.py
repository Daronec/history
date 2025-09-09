#!/usr/bin/env python3
"""
Тестирование генерации текста с правильной кодировкой
"""

import sys
import os
sys.path.append('src')

from models.history_ai import HistoryAIModel

def test_generation():
    """Тестирует генерацию текста"""
    print("🤖 Тестируем улучшенную генерацию текста...")
    print("=" * 60)
    
    try:
        # Загружаем обученную модель
        ai_model = HistoryAIModel()
        ai_model.load_trained_model('./models/history_ai_trained')
        
        # Тестовые промпты
        prompts = [
            "В 1812 году произошло важное событие:",
            "Петр I известен тем, что",
            "В истории России важную роль сыграл",
            "Революция 1917 года привела к",
            "Реформы Петра I включали",
            "В XVIII веке в России"
        ]
        
        for i, prompt in enumerate(prompts, 1):
            print(f"\n{i}. Промпт: {prompt}")
            try:
                result = ai_model.generate_text(prompt, max_length=80, temperature=0.8)
                print(f"   Результат: {result}")
            except Exception as e:
                print(f"   ❌ Ошибка: {e}")
        
        # Интерактивный режим
        print("\n🎮 Интерактивный режим:")
        print("Введите свой промпт (или 'выход' для завершения):")
        
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

if __name__ == "__main__":
    test_generation()
