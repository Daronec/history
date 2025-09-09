#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для генерации текста с помощью обученной модели
"""

import argparse
import sys
from pathlib import Path
import logging
import os

# Устанавливаем кодировку для Windows
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

# Добавляем путь к модулям
sys.path.append(str(Path(__file__).parent))

# Принудительно перезагружаем модули для обновлений
import importlib
if 'models.history_ai' in sys.modules:
    importlib.reload(sys.modules['models.history_ai'])

from models.history_ai import HistoryAIModel

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Генерация текста с помощью обученной модели')
    parser.add_argument('--model', type=str, required=True, help='Путь к обученной модели')
    parser.add_argument('--prompt', type=str, required=True, help='Промпт для генерации')
    parser.add_argument('--max_length', type=int, default=10000, help='Максимальная длина генерируемого текста')
    parser.add_argument('--temperature', type=float, default=0.1, help='Температура генерации')
    parser.add_argument('--num_return_sequences', type=int, default=1, help='Количество вариантов генерации')
    
    args = parser.parse_args()
    
    try:
        # Загружаем модель
        logger.info(f"Загружаем модель из {args.model}")
        model = HistoryAIModel()
        model.load_trained_model(args.model, task_type='generation')
        logger.info("Модель успешно загружена")
        
        # Генерируем текст
        logger.info(f"Генерируем текст для промпта: {args.prompt}")
        logger.info(f"Параметры генерации: max_length={args.max_length}, temperature={args.temperature}")
        result = model.generate_text(
            prompt=args.prompt,
            max_length=args.max_length,
            temperature=args.temperature
        )
        logger.info(f"Генерация завершена, длина результата: {len(result) if result else 0}")
        
        print(f"\n{'='*60}")
        print(f"ПРОМПТ: {args.prompt}")
        print(f"{'='*60}")
        print(f"ОТВЕТ ИИ:")
        print(f"{'='*60}")
        print(result)
        print(f"{'='*60}")
        print(f"Длина ответа: {len(result)} символов")
        print(f"{'='*60}")
        
    except Exception as e:
        logger.error(f"Ошибка при генерации текста: {e}")
        logger.error(f"Тип ошибки: {type(e).__name__}")
        import traceback
        logger.error(f"Трассировка: {traceback.format_exc()}")
        print(f"ОШИБКА: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
