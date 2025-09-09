#!/usr/bin/env python3
"""
Простое тестирование русской модели
"""

import sys
import os
sys.path.append('src')

def test_russian_model():
    """Тестирует русскую модель с предобученными весами"""
    print("🇷🇺 Тестируем русскую модель...")
    print("=" * 50)
    
    try:
        from models.history_ai_ru import HistoryAIModelRU
        
        # Создаем модель
        model = HistoryAIModelRU()
        
        # Загружаем предобученную модель
        print("🔄 Загружаем предобученную русскую модель...")
        model.load_model('generation')
        print("✅ Модель загружена!")
        
        # Тестовые промпты
        test_prompts = [
            "В 1812 году произошло",
            "Петр I известен тем, что",
            "Сталин родился в",
            "Революция 1917 года привела к"
        ]
        
        print("\n🧪 Тестируем генерацию:")
        for i, prompt in enumerate(test_prompts, 1):
            print(f"\n{i}. Промпт: {prompt}")
            try:
                result = model.generate_text(prompt, max_length=50, temperature=0.7)
                print(f"   Результат: {result}")
            except Exception as e:
                print(f"   ❌ Ошибка: {e}")
        
        print("\n🎮 Интерактивный режим:")
        print("Введите свой промпт (или 'выход' для завершения):")
        
        while True:
            try:
                user_prompt = input("\nВаш промпт: ").strip()
                if user_prompt.lower() in ['выход', 'exit', 'quit']:
                    break
                
                if user_prompt:
                    result = model.generate_text(user_prompt, max_length=100, temperature=0.7)
                    print(f"Результат: {result}")
            except KeyboardInterrupt:
                print("\n\n👋 До свидания!")
                break
            except Exception as e:
                print(f"❌ Ошибка: {e}")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("💡 Возможные решения:")
        print("   1. Проверьте подключение к интернету")
        print("   2. Убедитесь, что установлены все зависимости")
        print("   3. Попробуйте позже")

if __name__ == "__main__":
    test_russian_model()
