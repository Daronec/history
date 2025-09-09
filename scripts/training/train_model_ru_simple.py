#!/usr/bin/env python3
"""
Упрощенный скрипт для обучения русской ИИ модели
"""

import os
import sys
import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
import logging
from pathlib import Path

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_and_process_data(data_path):
    """Загружает и обрабатывает данные"""
    try:
        # Импортируем функцию обработки данных
        sys.path.append(str(Path(__file__).parent.parent.parent / "src"))
        from data_processing import process_data_directory, load_file
        
        data_path = Path(data_path)
        
        if data_path.is_dir():
            logger.info("Обрабатываем все файлы в директории")
            texts = process_data_directory(data_path)
        else:
            logger.info("Обрабатываем один файл")
            text = load_file(data_path)
            texts = [text] if text else []
        
        if not texts:
            raise ValueError("Не удалось извлечь тексты из данных")
        
        logger.info(f"Загружено {len(texts)} текстов")
        return texts
        
    except Exception as e:
        logger.error(f"Ошибка загрузки данных: {e}")
        raise

def create_dataset(texts, tokenizer, max_length=512):
    """Создает датасет для обучения"""
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
            padding=True,
            max_length=max_length,
            return_tensors="pt"
        )
        tokenized_data.append({
            "input_ids": tokens["input_ids"].squeeze(),
            "attention_mask": tokens["attention_mask"].squeeze(),
            "labels": tokens["input_ids"].squeeze()
        })
    
    return tokenized_data

def train_russian_model(data_path, model_name="ai-forever/rugpt3small_based_on_gpt2", output_dir="models/russian_model", num_epochs=3):
    """Обучает русскую модель"""
    try:
        logger.info("Начинаем обучение русской модели...")
        
        # Создаем директории
        os.makedirs("models", exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        
        # Загружаем данные
        texts = load_and_process_data(data_path)
        
        # Загружаем токенизатор и модель
        logger.info(f"Загружаем русскую модель: {model_name}")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        
        # Добавляем специальные токены
        special_tokens = {
            "pad_token": "<pad>",
            "eos_token": "<|endoftext|>",
            "bos_token": "<|startoftext|>"
        }
        tokenizer.add_special_tokens(special_tokens)
        model.resize_token_embeddings(len(tokenizer))
        
        # Создаем датасет
        logger.info("Создаем датасет...")
        dataset = create_dataset(texts, tokenizer)
        
        # Настройки обучения
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=num_epochs,
            per_device_train_batch_size=2,  # Меньший batch для русской модели
            per_device_eval_batch_size=2,
            warmup_steps=500,
            weight_decay=0.01,
            logging_dir='logs',
            logging_steps=10,
            save_steps=1000,
            eval_steps=1000,
            evaluation_strategy="no",
            save_strategy="steps",
            load_best_model_at_end=False,
            report_to=None,
            remove_unused_columns=False,
        )
        
        # Создаем тренер
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=tokenizer,
            mlm=False,
        )
        
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=dataset,
            data_collator=data_collator,
        )
        
        # Обучаем модель
        logger.info("Начинаем обучение...")
        trainer.train()
        
        # Сохраняем модель
        logger.info(f"Сохраняем модель в {output_dir}")
        trainer.save_model()
        tokenizer.save_pretrained(output_dir)
        
        logger.info("Обучение русской модели завершено успешно!")
        return True
        
    except Exception as e:
        logger.error(f"Ошибка обучения русской модели: {e}")
        return False

def main():
    """Главная функция"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Обучение русской модели ИИ-История")
    parser.add_argument("data_path", help="Путь к данным (файл или директория)")
    parser.add_argument("--model", default="ai-forever/rugpt3small_based_on_gpt2", help="Название модели")
    parser.add_argument("--output", default="models/russian_model", help="Директория для сохранения")
    parser.add_argument("--epochs", type=int, default=3, help="Количество эпох")
    
    args = parser.parse_args()
    
    # Проверяем путь к данным
    data_path = Path(args.data_path)
    if not data_path.exists():
        logger.error(f"Путь к данным не найден: {data_path}")
        return False
    
    # Обучаем модель
    success = train_russian_model(
        data_path=args.data_path,
        model_name=args.model,
        output_dir=args.output,
        num_epochs=args.epochs
    )
    
    if success:
        logger.info("✅ Обучение русской модели завершено успешно!")
        return True
    else:
        logger.error("❌ Обучение русской модели завершилось с ошибкой!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
