"""
Модель ИИ для изучения истории
Поддерживает различные типы задач: классификация, генерация текста, анализ
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
from typing import Dict, List, Optional, Union
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HistoryAIModel:
    """Базовый класс для ИИ модели изучения истории"""
    
    def __init__(self, model_name: str = "microsoft/DialoGPT-medium", device: str = "auto"):
        """
        Инициализация модели
        
        Args:
            model_name: Название предобученной модели
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
    
    def load_model(self, task_type: str = "generation"):
        """
        Загружает модель в зависимости от типа задачи
        
        Args:
            task_type: Тип задачи ('generation', 'classification', 'embedding')
        """
        try:
            logger.info(f"Загружаем модель {self.model_name} для задачи: {task_type}")
            
            # Загружаем токенизатор
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            
            # Добавляем специальные токены если их нет
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Добавляем специальные токены для языкового моделирования
            special_tokens = {
                'pad_token': '<|pad|>',
                'eos_token': '<|endoftext|>',
                'bos_token': '<|startoftext|>'
            }
            
            # Добавляем токены если их нет
            for token_type, token_value in special_tokens.items():
                if getattr(self.tokenizer, token_type) is None:
                    self.tokenizer.add_special_tokens({token_type: token_value})
            
            # Расширяем размер словаря если добавили новые токены
            if len(self.tokenizer) != self.tokenizer.vocab_size:
                self.tokenizer.resize_token_embeddings(len(self.tokenizer))
            
            # Загружаем модель в зависимости от задачи
            if task_type == "generation":
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    pad_token_id=self.tokenizer.pad_token_id
                )
                
                # Изменяем размер эмбеддингов если добавили новые токены
                if len(self.tokenizer) != self.tokenizer.vocab_size:
                    self.model.resize_token_embeddings(len(self.tokenizer))
            elif task_type == "classification":
                self.model = AutoModelForSequenceClassification.from_pretrained(
                    self.model_name,
                    num_labels=2,  # Можно настроить
                    pad_token_id=self.tokenizer.eos_token_id
                )
            elif task_type == "embedding":
                self.model = AutoModel.from_pretrained(self.model_name)
            else:
                raise ValueError(f"Неподдерживаемый тип задачи: {task_type}")
            
            # Перемещаем модель на устройство
            self.model.to(self.device)
            self.is_loaded = True
            
            logger.info(f"Модель успешно загружена на устройство: {self.device}")
            
        except Exception as e:
            logger.error(f"Ошибка при загрузке модели: {e}")
            raise
    
    def generate_text(self, prompt: str, max_length: int = 100, temperature: float = 0.7) -> str:
        """
        Генерирует текст на основе промпта
        
        Args:
            prompt: Начальный текст
            max_length: Максимальная длина генерируемого текста
            temperature: Температура для генерации (контролирует креативность)
        
        Returns:
            Сгенерированный текст
        """
        if not self.is_loaded:
            raise RuntimeError("Модель не загружена. Вызовите load_model() сначала.")
        
        try:
            # Токенизируем входной текст с правильной кодировкой
            inputs = self.tokenizer(
                prompt, 
                return_tensors="pt", 
                padding=True, 
                truncation=True,
                max_length=512
            ).to(self.device)
            
            # Генерируем текст с улучшенными параметрами
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
            
            # Проверяем, что модель сгенерировала текст
            if outputs is None or len(outputs) == 0:
                logger.warning("Модель не сгенерировала текст")
                return "Извините, не удалось сгенерировать ответ. Попробуйте изменить промпт."
            
            # Проверяем размер вывода
            if outputs.shape[0] == 0:
                logger.warning("Модель вернула пустой вывод")
                return "Извините, не удалось сгенерировать ответ. Попробуйте изменить промпт."
            
            # Декодируем результат с правильной кодировкой
            generated_text = self.tokenizer.decode(
                outputs[0], 
                skip_special_tokens=True,
                clean_up_tokenization_spaces=True
            )
            
            # Убираем исходный промпт из результата
            if generated_text.startswith(prompt):
                generated_text = generated_text[len(prompt):].strip()
            
            # Проверяем, что после обработки остался текст
            if not generated_text or len(generated_text.strip()) < 10:
                logger.warning("Сгенерированный текст слишком короткий или пустой")
                return "Извините, не удалось сгенерировать содержательный ответ. Попробуйте изменить промпт или параметры генерации."
            
            # Очищаем текст от артефактов
            generated_text = self._clean_generated_text(generated_text)
            
            return generated_text
            
        except Exception as e:
            logger.error(f"Ошибка при генерации текста: {e}")
            # Возвращаем понятное сообщение об ошибке вместо исключения
            return f"Произошла ошибка при генерации текста: {str(e)}. Попробуйте изменить промпт или параметры."
    
    def _clean_generated_text(self, text: str) -> str:
        """Очищает сгенерированный текст от артефактов"""
        # Убираем повторяющиеся символы
        import re
        
        # Убираем множественные пробелы
        text = re.sub(r'\s+', ' ', text)
        
        # Убираем странные символы
        text = re.sub(r'[^\w\s\.\,\!\?\:\;\-\(\)\"\']', '', text)
        
        # Убираем повторяющиеся слова
        words = text.split()
        cleaned_words = []
        prev_word = ""
        
        for word in words:
            if word != prev_word:
                cleaned_words.append(word)
                prev_word = word
        
        return ' '.join(cleaned_words).strip()
    
    def get_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Получает эмбеддинги для списка текстов
        
        Args:
            texts: Список текстов для обработки
        
        Returns:
            Массив эмбеддингов
        """
        if not self.is_loaded:
            raise RuntimeError("Модель не загружена. Вызовите load_model() сначала.")
        
        try:
            embeddings = []
            
            for text in texts:
                # Токенизируем текст
                inputs = self.tokenizer(
                    text, 
                    return_tensors="pt", 
                    padding=True, 
                    truncation=True, 
                    max_length=512
                ).to(self.device)
                
                # Получаем эмбеддинги
                with torch.no_grad():
                    outputs = self.model(**inputs)
                    # Используем среднее значение последнего скрытого слоя
                    embedding = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
                    embeddings.append(embedding[0])
            
            return np.array(embeddings)
            
        except Exception as e:
            logger.error(f"Ошибка при получении эмбеддингов: {e}")
            raise
    
    def train(self, train_dataset, eval_dataset=None, num_epochs: int = 3):
        """
        Обучает модель на предоставленных данных
        
        Args:
            train_dataset: Обучающий датасет
            eval_dataset: Валидационный датасет (опционально)
            num_epochs: Количество эпох обучения
        """
        if not self.is_loaded:
            raise RuntimeError("Модель не загружена. Вызовите load_model() сначала.")
        
        try:
            # Настройки обучения
            training_args = TrainingArguments(
                output_dir="./models/history_ai_trained",
                num_train_epochs=num_epochs,
                per_device_train_batch_size=4,
                per_device_eval_batch_size=4,
                warmup_steps=500,
                weight_decay=0.01,
                logging_dir="./logs",
                logging_steps=10,
                eval_strategy="steps" if eval_dataset else "no",
                eval_steps=500 if eval_dataset else None,
                save_steps=1000,
                save_total_limit=2,
            )
            
            # Создаем тренер
            trainer = Trainer(
                model=self.model,
                args=training_args,
                train_dataset=train_dataset,
                eval_dataset=eval_dataset,
                tokenizer=self.tokenizer,
            )
            
            # Начинаем обучение
            logger.info("Начинаем обучение модели...")
            trainer.train()
            
            # Сохраняем модель
            trainer.save_model()
            self.tokenizer.save_pretrained("./models/history_ai_trained")
            
            logger.info("Обучение завершено. Модель сохранена.")
            
        except Exception as e:
            logger.error(f"Ошибка при обучении модели: {e}")
            raise
    
    def save_model(self, path: str):
        """Сохраняет модель по указанному пути"""
        if not self.is_loaded:
            raise RuntimeError("Модель не загружена.")
        
        try:
            self.model.save_pretrained(path)
            self.tokenizer.save_pretrained(path)
            logger.info(f"Модель сохранена в {path}")
        except Exception as e:
            logger.error(f"Ошибка при сохранении модели: {e}")
            raise
    
    def load_trained_model(self, path: str, task_type: str = "generation"):
        """Загружает предобученную модель"""
        try:
            # Проверяем, существует ли путь
            from pathlib import Path
            model_path = Path(path)
            if not model_path.exists():
                logger.error(f"Путь к модели не существует: {path}")
                raise FileNotFoundError(f"Модель не найдена по пути: {path}")
            
            self.model_name = path
            self.load_model(task_type)
            
            # Проверяем, что модель действительно загружена
            if not self.is_loaded or self.model is None or self.tokenizer is None:
                logger.error("Модель не загружена корректно")
                raise RuntimeError("Модель не загружена корректно")
            
            logger.info(f"Предобученная модель загружена из {path}")
        except Exception as e:
            logger.error(f"Ошибка при загрузке предобученной модели: {e}")
            raise

# Пример использования
if __name__ == "__main__":
    # Создаем экземпляр модели
    ai_model = HistoryAIModel()
    
    # Загружаем модель для генерации текста
    ai_model.load_model("generation")
    
    # Генерируем текст
    prompt = "В 1812 году произошло важное историческое событие:"
    generated = ai_model.generate_text(prompt, max_length=150)
    print(f"Промпт: {prompt}")
    print(f"Сгенерированный текст: {generated}")
