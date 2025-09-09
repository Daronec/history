#!/usr/bin/env python3
"""
Модуль для оценки качества обучения модели
Проверяет, насколько хорошо модель изучила материалы
"""

import os
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import logging
from pathlib import Path
from typing import List, Dict, Any, Tuple
import random

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelEvaluator:
    """Класс для оценки качества обученной модели"""
    
    def __init__(self, model_path: str, model_type: str = "english"):
        """
        Инициализация оценщика модели
        
        Args:
            model_path: Путь к обученной модели
            model_type: Тип модели ('english' или 'russian')
        """
        self.model_path = Path(model_path)
        self.model_type = model_type
        self.tokenizer = None
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    def load_model(self):
        """Загружает обученную модель"""
        try:
            logger.info(f"Загружаем модель из {self.model_path}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_path)
            self.model.to(self.device)
            self.model.eval()
            logger.info("Модель успешно загружена")
            return True
        except Exception as e:
            logger.error(f"Ошибка загрузки модели: {e}")
            return False
    
    def generate_text(self, prompt: str, max_length: int = 200, temperature: float = 0.7) -> str:
        """
        Генерирует текст на основе промпта
        
        Args:
            prompt: Текст-запрос
            max_length: Максимальная длина ответа
            temperature: Температура генерации (0.1-1.0)
        
        Returns:
            Сгенерированный текст
        """
        try:
            # Токенизируем промпт
            inputs = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
            
            # Генерируем текст
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=max_length,
                    temperature=temperature,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    no_repeat_ngram_size=2
                )
            
            # Декодируем результат
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Убираем исходный промпт из результата
            if generated_text.startswith(prompt):
                generated_text = generated_text[len(prompt):].strip()
            
            return generated_text
            
        except Exception as e:
            logger.error(f"Ошибка генерации текста: {e}")
            return ""
    
    def test_knowledge_retention(self, test_questions: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Тестирует сохранение знаний модели
        
        Args:
            test_questions: Список тестовых вопросов и ожидаемых ответов
        
        Returns:
            Результаты тестирования
        """
        if not self.model:
            logger.error("Модель не загружена")
            return {}
        
        results = {
            "total_questions": len(test_questions),
            "correct_answers": 0,
            "partial_answers": 0,
            "incorrect_answers": 0,
            "detailed_results": []
        }
        
        logger.info(f"Начинаем тестирование на {len(test_questions)} вопросах")
        
        for i, question_data in enumerate(test_questions):
            question = question_data["question"]
            expected_keywords = question_data.get("keywords", [])
            expected_answer = question_data.get("expected", "")
            
            logger.info(f"Вопрос {i+1}: {question}")
            
            # Генерируем ответ
            generated_answer = self.generate_text(question, max_length=150)
            
            # Анализируем качество ответа
            quality_score = self._analyze_answer_quality(
                generated_answer, expected_keywords, expected_answer
            )
            
            result = {
                "question": question,
                "generated_answer": generated_answer,
                "expected_keywords": expected_keywords,
                "quality_score": quality_score,
                "status": "correct" if quality_score >= 0.7 else "partial" if quality_score >= 0.4 else "incorrect"
            }
            
            results["detailed_results"].append(result)
            
            # Обновляем счетчики
            if quality_score >= 0.7:
                results["correct_answers"] += 1
            elif quality_score >= 0.4:
                results["partial_answers"] += 1
            else:
                results["incorrect_answers"] += 1
            
            logger.info(f"Качество ответа: {quality_score:.2f} ({result['status']})")
        
        # Вычисляем общий процент
        results["accuracy_percentage"] = (results["correct_answers"] / results["total_questions"]) * 100
        results["partial_accuracy_percentage"] = ((results["correct_answers"] + results["partial_answers"]) / results["total_questions"]) * 100
        
        return results
    
    def _analyze_answer_quality(self, generated_answer: str, expected_keywords: List[str], expected_answer: str) -> float:
        """
        Анализирует качество сгенерированного ответа
        
        Args:
            generated_answer: Сгенерированный ответ
            expected_keywords: Ожидаемые ключевые слова
            expected_answer: Ожидаемый ответ
        
        Returns:
            Оценка качества (0.0 - 1.0)
        """
        if not generated_answer:
            return 0.0
        
        score = 0.0
        generated_lower = generated_answer.lower()
        
        # Проверяем наличие ключевых слов
        if expected_keywords:
            keyword_matches = 0
            for keyword in expected_keywords:
                if keyword.lower() in generated_lower:
                    keyword_matches += 1
            
            keyword_score = keyword_matches / len(expected_keywords)
            score += keyword_score * 0.6  # 60% веса для ключевых слов
        
        # Проверяем длину ответа (должен быть достаточно подробным)
        length_score = min(len(generated_answer) / 100, 1.0)  # Нормализуем к 100 символам
        score += length_score * 0.2  # 20% веса для длины
        
        # Проверяем связность (отсутствие повторений)
        words = generated_answer.split()
        if len(words) > 0:
            unique_words = len(set(words))
            coherence_score = unique_words / len(words)
            score += coherence_score * 0.2  # 20% веса для связности
        
        return min(score, 1.0)
    
    def create_test_questions(self, data_path: str) -> List[Dict[str, str]]:
        """
        Создает тестовые вопросы на основе данных
        
        Args:
            data_path: Путь к данным для создания вопросов
        
        Returns:
            Список тестовых вопросов
        """
        # Импортируем функцию обработки данных
        import sys
        sys.path.append(str(Path(__file__).parent))
        from data_processing import process_data_directory, load_file
        
        data_path = Path(data_path)
        
        # Загружаем данные
        if data_path.is_dir():
            texts = process_data_directory(data_path)
        else:
            text = load_file(data_path)
            texts = [text] if text else []
        
        if not texts:
            logger.warning("Не удалось загрузить данные для создания тестовых вопросов")
            return []
        
        # Создаем тестовые вопросы на основе содержимого
        test_questions = []
        
        # Базовые вопросы для истории России
        basic_questions = [
            {
                "question": "Когда произошла Куликовская битва?",
                "keywords": ["1380", "куликовская", "битва", "дмитрий"],
                "expected": "Куликовская битва произошла в 1380 году"
            },
            {
                "question": "Кто был первым русским царем?",
                "keywords": ["иван", "грозный", "царь", "1547"],
                "expected": "Иван IV Грозный был первым русским царем"
            },
            {
                "question": "Когда произошло крещение Руси?",
                "keywords": ["988", "владимир", "крещение", "христианство"],
                "expected": "Крещение Руси произошло в 988 году"
            },
            {
                "question": "Когда началась Отечественная война 1812 года?",
                "keywords": ["1812", "наполеон", "отечественная", "война"],
                "expected": "Отечественная война 1812 года началась в 1812 году"
            },
            {
                "question": "Кто отменил крепостное право в России?",
                "keywords": ["александр", "второй", "крепостное", "право", "1861"],
                "expected": "Александр II отменил крепостное право в 1861 году"
            }
        ]
        
        # Добавляем базовые вопросы
        test_questions.extend(basic_questions)
        
        # Создаем дополнительные вопросы на основе загруженных данных
        for text in texts[:3]:  # Берем первые 3 текста
            # Извлекаем ключевые даты и события
            words = text.split()
            dates = [word for word in words if word.isdigit() and len(word) == 4 and 800 <= int(word) <= 2024]
            
            if dates:
                date = random.choice(dates)
                question = f"Что происходило в {date} году?"
                test_questions.append({
                    "question": question,
                    "keywords": [date],
                    "expected": f"События {date} года"
                })
        
        logger.info(f"Создано {len(test_questions)} тестовых вопросов")
        return test_questions
    
    def save_evaluation_report(self, results: Dict[str, Any], output_path: str):
        """
        Сохраняет отчет об оценке модели
        
        Args:
            results: Результаты тестирования
            output_path: Путь для сохранения отчета
        """
        try:
            # Создаем директорию если не существует
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Сохраняем отчет
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Отчет сохранен в {output_path}")
            
            # Выводим краткую сводку
            print("\n" + "="*60)
            print("📊 РЕЗУЛЬТАТЫ ОЦЕНКИ МОДЕЛИ")
            print("="*60)
            print(f"📝 Всего вопросов: {results['total_questions']}")
            print(f"✅ Правильных ответов: {results['correct_answers']} ({results['accuracy_percentage']:.1f}%)")
            print(f"⚠️  Частично правильных: {results['partial_answers']}")
            print(f"❌ Неправильных ответов: {results['incorrect_answers']}")
            print(f"🎯 Общая точность: {results['partial_accuracy_percentage']:.1f}%")
            print("="*60)
            
            # Оценка качества обучения
            if results['accuracy_percentage'] >= 70:
                print("🎉 ОТЛИЧНО! Модель хорошо изучила материалы")
            elif results['accuracy_percentage'] >= 50:
                print("👍 ХОРОШО! Модель частично изучила материалы")
            elif results['accuracy_percentage'] >= 30:
                print("⚠️  УДОВЛЕТВОРИТЕЛЬНО! Модель слабо изучила материалы")
            else:
                print("❌ ПЛОХО! Модель практически не изучила материалы")
            
            print("="*60)
            
        except Exception as e:
            logger.error(f"Ошибка сохранения отчета: {e}")

def evaluate_model(model_path: str, data_path: str = "data/raw", model_type: str = "english"):
    """
    Основная функция для оценки модели
    
    Args:
        model_path: Путь к обученной модели
        data_path: Путь к данным для создания тестовых вопросов
        model_type: Тип модели
    """
    try:
        # Создаем оценщик
        evaluator = ModelEvaluator(model_path, model_type)
        
        # Загружаем модель
        if not evaluator.load_model():
            logger.error("Не удалось загрузить модель для оценки")
            return False
        
        # Создаем тестовые вопросы
        test_questions = evaluator.create_test_questions(data_path)
        if not test_questions:
            logger.error("Не удалось создать тестовые вопросы")
            return False
        
        # Проводим тестирование
        results = evaluator.test_knowledge_retention(test_questions)
        
        # Сохраняем отчет
        output_path = f"evaluation_report_{model_type}.json"
        evaluator.save_evaluation_report(results, output_path)
        
        return True
        
    except Exception as e:
        logger.error(f"Ошибка оценки модели: {e}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Оценка качества обученной модели")
    parser.add_argument("model_path", help="Путь к обученной модели")
    parser.add_argument("--data", default="data/raw", help="Путь к данным для создания тестов")
    parser.add_argument("--type", default="english", choices=["english", "russian"], help="Тип модели")
    
    args = parser.parse_args()
    
    success = evaluate_model(args.model_path, args.data, args.type)
    if success:
        print("✅ Оценка модели завершена успешно!")
    else:
        print("❌ Ошибка при оценке модели!")
