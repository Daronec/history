"""
Русская модель ИИ для изучения истории
Использует русские предобученные модели
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import (
    AutoTokenizer, 
    AutoModel, 
    AutoModelForSequenceClassification,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer
)
import numpy as np
import os
from typing import Dict, List, Optional, Union
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HistoryAIModelRU:
    """Русская модель ИИ для изучения истории"""
    
    def __init__(self, model_name: str = "ai-forever/rugpt3small_based_on_gpt2", device: str = "auto"):
        """
        Инициализация русской модели
        
        Args:
            model_name: Название русской предобученной модели
            device: Устройство для вычислений ('cpu', 'cuda', 'auto')
        """
        self.model_name = model_name
        self.device = self._setup_device(device)
        self.tokenizer = None
        self.model = None
        self.is_loaded = False
        
    def _setup_device(self, device: str) -> str:
        """Настройка устройства для вычислений"""
        if device == "auto":
            if torch.cuda.is_available():
                return "cuda"
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                return "mps"
            else:
                return "cpu"
        return device
    
    def load_model(self, task: str = "generation"):
        """
        Загрузка предобученной модели
        
        Args:
            task: Тип задачи ('generation', 'classification', 'embedding')
        """
        try:
            logger.info(f"Загружаем русскую модель {self.model_name} для задачи: {task}")
            
            # Загружаем токенизатор
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            
            # Добавляем специальные токены для русского языка
            special_tokens = {
                'pad_token': '<|pad|>',
                'eos_token': '<|endoftext|>',
                'bos_token': '<|startoftext|>'
            }
            
            # Добавляем токены, если их нет
            for token_type, token_value in special_tokens.items():
                if getattr(self.tokenizer, token_type) is None:
                    self.tokenizer.add_special_tokens({token_type: token_value})
            
            # Загружаем модель в зависимости от задачи
            if task == "generation":
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    pad_token_id=self.tokenizer.pad_token_id
                )
                # Изменяем размер эмбеддингов для новых токенов
                self.model.resize_token_embeddings(len(self.tokenizer))
            elif task == "classification":
                self.model = AutoModelForSequenceClassification.from_pretrained(
                    self.model_name,
                    num_labels=2
                )
            else:  # embedding
                self.model = AutoModel.from_pretrained(self.model_name)
            
            # Перемещаем модель на устройство
            self.model.to(self.device)
            self.is_loaded = True
            
            logger.info(f"Русская модель успешно загружена на устройство: {self.device}")
            
        except Exception as e:
            logger.error(f"Ошибка при загрузке русской модели: {e}")
            raise
    
    def generate_text(self, prompt: str, max_length: int = 100, temperature: float = 0.7) -> str:
        """
        Генерация текста на русском языке
        
        Args:
            prompt: Начальный текст для генерации
            max_length: Максимальная длина генерируемого текста
            temperature: Температура для генерации (контролирует креативность)
            
        Returns:
            Сгенерированный текст
        """
        if not self.is_loaded:
            raise ValueError("Модель не загружена. Сначала вызовите load_model()")
        
        try:
            # Токенизируем входной текст
            inputs = self.tokenizer(
                prompt, 
                return_tensors="pt", 
                padding=True, 
                truncation=True,
                max_length=512
            ).to(self.device)
            
            # Генерируем текст
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs.input_ids,
                    attention_mask=inputs.attention_mask,
                    max_length=max_length,
                    temperature=temperature,
                    do_sample=True,
                    top_p=0.9,
                    top_k=50,
                    repetition_penalty=1.1,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    no_repeat_ngram_size=2
                )
            
            # Декодируем результат
            generated_text = self.tokenizer.decode(
                outputs[0], 
                skip_special_tokens=True,
                clean_up_tokenization_spaces=True
            )
            
            # Убираем исходный промпт из результата
            if generated_text.startswith(prompt):
                generated_text = generated_text[len(prompt):].strip()
            
            # Очищаем результат
            generated_text = self._clean_generated_text(generated_text)
            
            return generated_text
            
        except Exception as e:
            logger.error(f"Ошибка при генерации текста: {e}")
            return f"Ошибка генерации: {e}"
    
    def _clean_generated_text(self, text: str) -> str:
        """Очистка сгенерированного текста"""
        # Убираем лишние пробелы и переносы строк
        text = text.strip()
        
        # Убираем повторяющиеся фразы
        sentences = text.split('.')
        unique_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and sentence not in unique_sentences:
                unique_sentences.append(sentence)
        
        # Объединяем предложения
        cleaned_text = '. '.join(unique_sentences)
        
        # Добавляем точку в конце, если её нет
        if cleaned_text and not cleaned_text.endswith('.'):
            cleaned_text += '.'
        
        return cleaned_text
    
    def train(self, data_path: str, task: str = "generation", epochs: int = 3, 
              learning_rate: float = 5e-5, batch_size: int = 4):
        """
        Обучение русской модели
        
        Args:
            data_path: Путь к данным для обучения
            task: Тип задачи
            epochs: Количество эпох
            learning_rate: Скорость обучения
            batch_size: Размер батча
        """
        if not self.is_loaded:
            self.load_model(task)
        
        try:
            logger.info("Начинаем обучение русской модели...")
            
            # Подготавливаем данные
            from train_model import prepare_training_data
            train_dataset = prepare_training_data(data_path, self.tokenizer, task)
            
            # Настройки обучения
            training_args = TrainingArguments(
                output_dir='./models/history_ai_ru_trained',
                num_train_epochs=epochs,
                per_device_train_batch_size=batch_size,
                per_device_eval_batch_size=batch_size,
                warmup_steps=100,
                weight_decay=0.01,
                logging_dir='./logs',
                logging_steps=10,
                save_steps=500,
                eval_strategy="steps",
                eval_steps=500,
                load_best_model_at_end=True,
                report_to=None
            )
            
            # Создаем тренер
            trainer = Trainer(
                model=self.model,
                args=training_args,
                train_dataset=train_dataset,
                processing_class=self.tokenizer,
            )
            
            # Обучаем модель
            trainer.train()
            
            # Сохраняем модель
            trainer.save_model()
            self.tokenizer.save_pretrained('./models/history_ai_ru_trained')
            
            logger.info("Обучение русской модели завершено. Модель сохранена.")
            
        except Exception as e:
            logger.error(f"Ошибка при обучении русской модели: {e}")
            raise
    
    def load_trained_model(self, model_path: str):
        """Загрузка обученной русской модели"""
        try:
            logger.info(f"Загружаем обученную русскую модель из {model_path}")
            
            # Если локальная модель не найдена, используем предобученную
            if not os.path.exists(model_path):
                logger.info("Локальная модель не найдена, используем предобученную")
                self.load_model('generation')
                return
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModelForCausalLM.from_pretrained(model_path)
            self.model.to(self.device)
            self.is_loaded = True
            
            logger.info("Обученная русская модель успешно загружена")
            
        except Exception as e:
            logger.error(f"Ошибка при загрузке обученной русской модели: {e}")
            # Fallback на предобученную модель
            logger.info("Переключаемся на предобученную русскую модель")
            self.load_model('generation')
