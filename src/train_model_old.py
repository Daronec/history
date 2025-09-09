"""
Скрипт для обучения ИИ модели на исторических данных
"""

import os
import json
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer
from datasets import Dataset as HFDataset
import logging
from typing import List, Dict, Any
import argparse
from pathlib import Path

# Импортируем нашу модель и обработку данных
from models.history_ai import HistoryAIModel
from data_processing import process_data_directory, get_supported_formats

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HistoryDataset(Dataset):
    """Класс для работы с историческими данными"""
    
    def __init__(self, texts: List[str], labels: List[int] = None, tokenizer=None, max_length: int = 512):
        """
        Args:
            texts: Список текстов
            labels: Список меток (для классификации)
            tokenizer: Токенизатор
            max_length: Максимальная длина последовательности
        """
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.is_classification = labels is not None
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = str(self.texts[idx])
        
        # Токенизируем текст
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt'
        )
        
        result = {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten()
        }
        
        # Добавляем метки для классификации
        if self.is_classification:
            result['labels'] = torch.tensor(self.labels[idx], dtype=torch.long)
        
        return result

def load_historical_data(data_path: str) -> Dict[str, Any]:
    """
    Загружает исторические данные из различных форматов
    
    Args:
        data_path: Путь к файлу или директории с данными
    
    Returns:
        Словарь с данными
    """
    data_path = Path(data_path)
    
    if not data_path.exists():
        raise FileNotFoundError(f"Путь {data_path} не найден")
    
    logger.info(f"Загружаем данные из {data_path}")
    
    # Если это директория, обрабатываем все файлы
    if data_path.is_dir():
        logger.info("Обрабатываем все файлы в директории")
        texts = process_data_directory(data_path)
        data = [{'text': text} for text in texts]
    else:
        # Если это файл, обрабатываем его
        if data_path.suffix.lower() == '.json':
            # Загружаем JSON файл
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Загружен JSON файл с {len(data)} записями")
        else:
            # Обычный файл
            from data_processing import load_file
            text = load_file(data_path)
            if text:
                data = [{'text': text}]
            else:
                data = []
    
    logger.info(f"Загружено {len(data)} записей")
    return data

def prepare_training_data(data: List[Dict], task_type: str = "generation") -> tuple:
    """
    Подготавливает данные для обучения
    
    Args:
        data: Список словарей с данными
        task_type: Тип задачи ('generation', 'classification')
    
    Returns:
        Кортеж с подготовленными данными
    """
    texts = []
    labels = []
    
    for item in data:
        if isinstance(item, dict):
            # Извлекаем текст
            if 'text' in item:
                texts.append(item['text'])
            elif 'content' in item:
                texts.append(item['content'])
            elif 'description' in item:
                texts.append(item['description'])
            else:
                # Берем первое строковое значение
                for key, value in item.items():
                    if isinstance(value, str) and len(value) > 10:
                        texts.append(value)
                        break
            
            # Извлекаем метки для классификации
            if task_type == "classification":
                if 'label' in item:
                    labels.append(item['label'])
                elif 'category' in item:
                    labels.append(item['category'])
                elif 'class' in item:
                    labels.append(item['class'])
                else:
                    labels.append(0)  # По умолчанию
    
    if task_type == "classification" and not labels:
        logger.warning("Метки не найдены, создаем фиктивные метки")
        labels = [0] * len(texts)
    
    return texts, labels if task_type == "classification" else None

def create_sample_data():
    """Создает пример исторических данных для обучения"""
    sample_data = [
        {
            "text": "В 1812 году Наполеон Бонапарт вторгся в Россию с армией в 600 тысяч человек. Это событие стало началом Отечественной войны 1812 года.",
            "category": "война"
        },
        {
            "text": "Петр I Великий провел масштабные реформы в России, включая создание регулярной армии и флота, а также основание Санкт-Петербурга в 1703 году.",
            "category": "реформы"
        },
        {
            "text": "В 988 году князь Владимир крестил Русь, приняв христианство из Византии. Это событие оказало огромное влияние на развитие русской культуры.",
            "category": "религия"
        },
        {
            "text": "Куликовская битва 1380 года стала переломным моментом в борьбе русских княжеств против монголо-татарского ига.",
            "category": "война"
        },
        {
            "text": "Иван IV Грозный был первым русским царем, коронованным в 1547 году. Его правление характеризовалось централизацией власти и опричниной.",
            "category": "политика"
        },
        {
            "text": "Смутное время (1598-1613) было периодом политического кризиса в России, завершившимся избранием на престол династии Романовых.",
            "category": "политика"
        },
        {
            "text": "Александр II отменил крепостное право в 1861 году, что стало важным шагом в модернизации России.",
            "category": "реформы"
        },
        {
            "text": "Октябрьская революция 1917 года привела к свержению Временного правительства и установлению советской власти в России.",
            "category": "революция"
        }
    ]
    
    # Сохраняем пример данных
    os.makedirs("data/raw", exist_ok=True)
    with open("data/raw/sample_history_data.json", "w", encoding="utf-8") as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=2)
    
    logger.info("Создан файл с примером исторических данных: data/raw/sample_history_data.json")
    return sample_data

def train_model(data_path: str = "data/raw", task_type: str = "generation", num_epochs: int = 3, model_name: str = "microsoft/DialoGPT-medium"):
    """
    Основная функция обучения модели
    
    Args:
        data_path: Путь к данным (по умолчанию data/raw)
        task_type: Тип задачи
        num_epochs: Количество эпох
        model_name: Название модели
    """
    try:
        # Создаем директории
        os.makedirs("models", exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        
        # Загружаем данные
        if data_path == "sample":
            data = create_sample_data()
        else:
            data = load_historical_data(data_path)
            
            # Если папка data/raw пуста, выдаем ошибку
            if not data and data_path == "data/raw":
                raise ValueError(
                    "Папка data/raw пуста! Добавьте файлы для обучения модели.\n"
                    "Поддерживаемые форматы: TXT, CSV, JSON, PDF, DOC, DOCX, DJVU"
                )
        
        # Подготавливаем данные
        texts, labels = prepare_training_data(data, task_type)
        
        if not texts:
            raise ValueError("Не удалось извлечь тексты из данных")
        
        logger.info(f"Подготовлено {len(texts)} текстов для обучения")
        
        # Создаем модель
        ai_model = HistoryAIModel(model_name=model_name)
        ai_model.load_model(task_type)
        
        # Создаем датасет
        if task_type == "classification":
            dataset = HistoryDataset(texts, labels, ai_model.tokenizer)
        else:
            dataset = HistoryDataset(texts, None, ai_model.tokenizer)
        
        # Для генерации текста создаем правильный датасет
        if task_type == "generation":
            # Создаем датасет для языкового моделирования
            texts_for_lm = []
            for text in texts:
                # Добавляем специальные токены
                formatted_text = f"<|startoftext|>{text}<|endoftext|>"
                texts_for_lm.append(formatted_text)
            
            # Токенизируем все тексты
            tokenized_texts = []
            for text in texts_for_lm:
                tokens = ai_model.tokenizer(
                    text,
                    truncation=True,
                    padding='max_length',
                    max_length=128,
                    return_tensors='pt'
                )
                tokenized_texts.append({
                    'input_ids': tokens['input_ids'].flatten(),
                    'attention_mask': tokens['attention_mask'].flatten(),
                    'labels': tokens['input_ids'].flatten()  # Для языкового моделирования labels = input_ids
                })
            
            hf_dataset = HFDataset.from_list([
                {
                    'input_ids': item['input_ids'].tolist(),
                    'attention_mask': item['attention_mask'].tolist(),
                    'labels': item['labels'].tolist()
                }
                for item in tokenized_texts
            ])
        else:
            # Для классификации используем старый подход
            hf_dataset = HFDataset.from_list([
                {
                    'input_ids': item['input_ids'].tolist(),
                    'attention_mask': item['attention_mask'].tolist(),
                    **({'labels': item['labels'].item()} if 'labels' in item else {})
                }
                for item in dataset
            ])
        
        # Разделяем на train/eval
        train_size = int(0.8 * len(hf_dataset))
        train_dataset = hf_dataset.select(range(train_size))
        eval_dataset = hf_dataset.select(range(train_size, len(hf_dataset)))
        
        # Обучаем модель
        ai_model.train(train_dataset, eval_dataset, num_epochs)
        
        logger.info("Обучение завершено успешно!")
        
        # Тестируем модель
        if task_type == "generation":
            test_prompt = "В истории России важным событием было:"
            generated = ai_model.generate_text(test_prompt, max_length=100)
            print(f"\n🧪 Тест генерации:")
            print(f"Промпт: {test_prompt}")
            print(f"Результат: {generated}")
        
    except Exception as e:
        logger.error(f"Ошибка при обучении: {e}")
        raise

def main():
    """Главная функция"""
    parser = argparse.ArgumentParser(description="Обучение ИИ модели для изучения истории")
    parser.add_argument("--data", type=str, default="data/raw", 
                       help="Путь к папке с данными (по умолчанию data/raw) или 'sample' для тестовых данных")
    parser.add_argument("--task", type=str, default="generation", 
                       choices=["generation", "classification"],
                       help="Тип задачи")
    parser.add_argument("--epochs", type=int, default=3, 
                       help="Количество эпох обучения")
    parser.add_argument("--model", type=str, default="microsoft/DialoGPT-medium",
                       help="Название предобученной модели")
    
    args = parser.parse_args()
    
    print("🚀 Начинаем обучение ИИ модели для изучения истории")
    print(f"📊 Данные: {args.data}")
    print(f"🎯 Задача: {args.task}")
    print(f"🔄 Эпохи: {args.epochs}")
    print(f"🤖 Модель: {args.model}")
    print("=" * 60)
    
    train_model(args.data, args.task, args.epochs, args.model)

if __name__ == "__main__":
    main()
