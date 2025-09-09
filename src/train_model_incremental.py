#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Инкрементальное обучение модели с отслеживанием изученных файлов
"""

import argparse
import sys
import json
from pathlib import Path
import logging
import torch
from typing import List
from datasets import Dataset as HFDataset

# Добавляем путь к модулям
sys.path.append(str(Path(__file__).parent))

from models.history_ai import HistoryAIModel
from incremental_data_processing import IncrementalDataProcessor

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_historical_data(data_path: str) -> list:
    """
    Загружает исторические данные из файла
    
    Args:
        data_path: Путь к данным
        
    Returns:
        Список данных для обучения
    """
    data_file = Path(data_path)
    
    if not data_file.exists():
        raise ValueError(f"Файл данных не найден: {data_path}")
    
    logger.info(f"Загружаем данные из {data_path}")
    
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    logger.info(f"Загружено {len(data)} записей")
    return data

def extract_texts_from_data(data: list) -> list:
    """
    Извлекает тексты из данных
    
    Args:
        data: Список данных
        
    Returns:
        Список текстов
    """
    texts = []
    for item in data:
        if isinstance(item, dict) and 'text' in item:
            texts.append(item['text'])
        elif isinstance(item, str):
            texts.append(item)
    
    logger.info(f"Подготовлено {len(texts)} текстов для обучения")
    return texts

def create_dataset_for_training(texts: List[str], tokenizer, max_length: int = 512):
    """
    Создает датасет для обучения модели
    
    Args:
        texts: Список текстов
        tokenizer: Токенизатор
        max_length: Максимальная длина последовательности
        
    Returns:
        Датасет для обучения
    """
    logger.info("Создаем датасет для обучения...")
    
    # Подготавливаем данные
    formatted_texts = []
    for text in texts:
        # Добавляем специальные токены
        formatted_text = f"<|startoftext|>{text}<|endoftext|>"
        formatted_texts.append(formatted_text)
    
    # Токенизируем
    tokenized_data = []
    for text in formatted_texts:
        tokens = tokenizer(
            text,
            truncation=True,
            padding='max_length',
            max_length=max_length,
            return_tensors="pt"
        )
        tokenized_data.append({
            "input_ids": tokens["input_ids"].squeeze().tolist(),
            "attention_mask": tokens["attention_mask"].squeeze().tolist(),
            "labels": tokens["input_ids"].squeeze().tolist()  # Для языкового моделирования
        })
    
    # Создаем HuggingFace датасет
    hf_dataset = HFDataset.from_list(tokenized_data)
    
    # Устанавливаем формат для PyTorch
    hf_dataset.set_format("torch")
    
    logger.info(f"Создан датасет с {len(hf_dataset)} примерами")
    return hf_dataset

def train_model_incremental(data_path: str, task: str = "generation", epochs: int = 1, 
                          model_name: str = "ai-forever/rugpt3small_based_on_gpt2"):
    """
    Инкрементальное обучение модели
    
    Args:
        data_path: Путь к данным
        task: Тип задачи
        epochs: Количество эпох
        model_name: Название модели
    """
    print("🚀 Начинаем инкрементальное обучение ИИ модели для изучения истории")
    print(f"📊 Данные: {data_path}")
    print(f"🎯 Задача: {task}")
    print(f"🔄 Эпохи: {epochs}")
    print(f"🤖 Модель: {model_name}")
    print("=" * 60)
    
    # Инициализируем процессор данных
    processor = IncrementalDataProcessor()
    
    # Проверяем статистику
    stats = processor.get_processing_stats()
    print(f"📈 Текущая статистика:")
    print(f"  Изучено файлов: {stats['learned_files']}")
    print(f"  Общий объем текста: {stats['total_text_length']:,} символов")
    print(f"  Записей в данных: {stats['total_records']}")
    print()
    
    # Обрабатываем новые файлы
    data_path_obj = Path(data_path)
    new_data = processor.process_new_files(data_path_obj)
    
    if not new_data:
        print("ℹ️ Нет новых файлов для обучения")
        print("🔄 Продолжаем обучение на всех существующих данных...")
    else:
        print(f"🆕 Обработано {len(new_data)} новых файлов:")
        for item in new_data:
            print(f"  - {item['filename']}: {item['processed_length']:,} символов")
        print()
    
    # Загружаем все данные для обучения
    processed_data_file = Path("data/processed/pdf_history_data.json")
    if not processed_data_file.exists():
        raise ValueError("Файл обработанных данных не найден")
    
    data = load_historical_data(str(processed_data_file))
    texts = extract_texts_from_data(data)
    
    if not texts:
        raise ValueError("Не удалось извлечь тексты из данных")
    
    # Инициализируем модель
    logger.info(f"Загружаем модель {model_name} для задачи: {task}")
    model = HistoryAIModel(model_name=model_name)
    model.load_model(task_type=task)
    
    # Создаем датасет для обучения
    logger.info("Создаем датасет для обучения...")
    train_dataset = create_dataset_for_training(texts, model.tokenizer)
    
    # Обучаем модель
    logger.info("Начинаем обучение модели...")
    model.train(train_dataset, num_epochs=epochs)
    
    # Сохраняем модель
    model.save_model("models/history_ai_trained")
    logger.info("Обучение завершено. Модель сохранена.")
    
    print("✅ Инкрементальное обучение завершено успешно!")
    
    # Показываем обновленную статистику
    stats = processor.get_processing_stats()
    print(f"\n📈 Обновленная статистика:")
    print(f"  Изучено файлов: {stats['learned_files']}")
    print(f"  Общий объем текста: {stats['total_text_length']:,} символов")
    print(f"  Записей в данных: {stats['total_records']}")
    
    # Тестируем модель
    print("\n🧪 Тест генерации:")
    test_prompt = "В истории России важным событием было:"
    result = model.generate_text(prompt=test_prompt, max_length=100, temperature=0.7)
    print(f"Промпт: {test_prompt}")
    print(f"Результат: {result}")

def main():
    parser = argparse.ArgumentParser(description='Инкрементальное обучение ИИ модели')
    parser.add_argument('--data', type=str, help='Путь к данным для обучения')
    parser.add_argument('--task', type=str, default='generation', help='Тип задачи (generation)')
    parser.add_argument('--epochs', type=int, default=1, help='Количество эпох обучения')
    parser.add_argument('--model', type=str, default='ai-forever/rugpt3small_based_on_gpt2', 
                       help='Название модели для обучения')
    parser.add_argument('--reset', action='store_true', help='Сбросить данные обучения')
    parser.add_argument('--stats', action='store_true', help='Показать статистику')
    
    args = parser.parse_args()
    
    if args.reset:
        processor = IncrementalDataProcessor()
        processor.reset_learning()
        print("✅ Данные обучения сброшены")
        return
    
    if args.stats:
        processor = IncrementalDataProcessor()
        stats = processor.get_processing_stats()
        print(f"📊 Статистика обучения:")
        print(f"  Изучено файлов: {stats['learned_files']}")
        print(f"  Общий объем текста: {stats['total_text_length']:,} символов")
        print(f"  Записей в данных: {stats['total_records']}")
        print(f"  Файл отслеживания: {stats['tracking_file']}")
        return
    
    if not args.data:
        print("❌ Необходимо указать путь к данным с помощью --data")
        return
    
    try:
        train_model_incremental(
            data_path=args.data,
            task=args.task,
            epochs=args.epochs,
            model_name=args.model
        )
    except Exception as e:
        logger.error(f"Ошибка при обучении: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
