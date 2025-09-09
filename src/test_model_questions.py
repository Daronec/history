#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для тестирования модели на исторических вопросах
"""

import argparse
import sys
from pathlib import Path
import logging

# Добавляем путь к модулям
sys.path.append(str(Path(__file__).parent))

from models.history_ai import HistoryAIModel

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Список тестовых исторических вопросов
HISTORICAL_QUESTIONS = [
    "В истории России важным событием было",
    "Петр I провел важные реформы",
    "Революция 1917 года",
    "Великая Отечественная война началась",
    "Иван Грозный правил",
    "Крещение Руси произошло",
    "Столыпинские реформы включали",
    "Смутное время в России",
    "Екатерина II была известна",
    "Александр II отменил крепостное право"
]

def test_model_questions(model_path: str, max_length: int = 100):
    """
    Тестирует модель на исторических вопросах
    
    Args:
        model_path: Путь к обученной модели
        max_length: Максимальная длина генерируемого текста
    """
    try:
        # Загружаем модель
        logger.info(f"Загружаем модель из {model_path}")
        model = HistoryAIModel()
        model.load_trained_model(model_path, task_type='generation')
        
        print("🧪 Тестирование модели на исторических вопросах")
        print("=" * 60)
        
        for i, question in enumerate(HISTORICAL_QUESTIONS, 1):
            print(f"\n📝 Вопрос {i}: {question}")
            
            # Генерируем ответ
            result = model.generate_text(
                prompt=question,
                max_length=max_length,
                temperature=0.7
            )
            
            print(f"🤖 Ответ: {result}")
            print("-" * 40)
        
        print("\n✅ Тестирование завершено!")
        
    except Exception as e:
        logger.error(f"Ошибка при тестировании модели: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Тестирование модели на исторических вопросах')
    parser.add_argument('--model', type=str, required=True, help='Путь к обученной модели')
    parser.add_argument('--max_length', type=int, default=100, help='Максимальная длина генерируемого текста')
    
    args = parser.parse_args()
    
    test_model_questions(args.model, args.max_length)

if __name__ == "__main__":
    main()
