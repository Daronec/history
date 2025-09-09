#!/usr/bin/env python3
"""
Обучение русской ИИ модели для изучения истории
"""

import sys
import os
sys.path.append('src')

from models.history_ai_ru import HistoryAIModelRU
from train_model import load_historical_data

def train_russian_model():
    """Обучает русскую модель на исторических данных"""
    print("🇷🇺 Обучение русской ИИ модели для изучения истории")
    print("=" * 60)
    
    try:
        # Создаем русскую модель
        ai_model = HistoryAIModelRU()
        
        # Загружаем данные
        print("📊 Загружаем исторические данные...")
        data = load_historical_data('data/raw')
        
        # Обучаем модель
        print("🤖 Начинаем обучение русской модели...")
        ai_model.train(
            data_path='data/raw',
            task='generation',
            epochs=1,
            learning_rate=5e-5,
            batch_size=2
        )
        
        print("✅ Обучение русской модели завершено!")
        
        # Тестируем результат
        print("\n🧪 Тест генерации на русском языке:")
        ai_model.load_trained_model('./models/history_ai_ru_trained')
        
        test_prompts = [
            "В 1812 году произошло",
            "Петр I известен тем, что",
            "Сталин родился в"
        ]
        
        for prompt in test_prompts:
            result = ai_model.generate_text(prompt, max_length=50, temperature=0.7)
            print(f"Промпт: {prompt}")
            print(f"Результат: {result}")
            print()
        
    except Exception as e:
        print(f"❌ Ошибка при обучении русской модели: {e}")
        print("💡 Убедитесь, что у вас есть данные в data/raw/sample_history_data.json")

if __name__ == "__main__":
    train_russian_model()
