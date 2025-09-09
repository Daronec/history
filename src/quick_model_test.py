#!/usr/bin/env python3
"""
Быстрый тест модели - проверяет, изучила ли модель материалы
"""

import os
import sys
from pathlib import Path
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def quick_test_model(model_path: str, model_type: str = "english"):
    """
    Быстрый тест модели на знание исторических фактов
    
    Args:
        model_path: Путь к обученной модели
        model_type: Тип модели ('english' или 'russian')
    """
    try:
        print("🧪 БЫСТРЫЙ ТЕСТ МОДЕЛИ")
        print("="*50)
        
        # Загружаем модель
        print(f"📥 Загружаем модель из {model_path}...")
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForCausalLM.from_pretrained(model_path)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)
        model.eval()
        print("✅ Модель загружена успешно")
        
        # Тестовые вопросы
        if model_type == "russian":
            test_questions = [
                "Когда произошла Куликовская битва?",
                "Кто был первым русским царем?",
                "Когда произошло крещение Руси?",
                "Кто отменил крепостное право?",
                "Когда началась Отечественная война 1812 года?"
            ]
        else:
            test_questions = [
                "When did the Battle of Kulikovo occur?",
                "Who was the first Russian tsar?",
                "When did the baptism of Rus happen?",
                "Who abolished serfdom in Russia?",
                "When did the Patriotic War of 1812 begin?"
            ]
        
        print(f"\n🎯 Тестируем модель на {len(test_questions)} вопросах...")
        print("="*50)
        
        correct_answers = 0
        total_questions = len(test_questions)
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n❓ Вопрос {i}: {question}")
            
            # Генерируем ответ
            inputs = tokenizer.encode(question, return_tensors="pt").to(device)
            
            with torch.no_grad():
                outputs = model.generate(
                    inputs,
                    max_length=100,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id,
                    eos_token_id=tokenizer.eos_token_id,
                    no_repeat_ngram_size=2
                )
            
            # Декодируем ответ
            generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            if generated_text.startswith(question):
                generated_text = generated_text[len(question):].strip()
            
            print(f"🤖 Ответ модели: {generated_text}")
            
            # Простая проверка качества ответа
            if generated_text and len(generated_text) > 10:
                # Проверяем наличие ключевых слов в зависимости от вопроса
                if i == 1 and ("1380" in generated_text or "куликовская" in generated_text.lower()):
                    correct_answers += 1
                    print("✅ Правильный ответ!")
                elif i == 2 and ("иван" in generated_text.lower() or "грозный" in generated_text.lower()):
                    correct_answers += 1
                    print("✅ Правильный ответ!")
                elif i == 3 and ("988" in generated_text or "владимир" in generated_text.lower()):
                    correct_answers += 1
                    print("✅ Правильный ответ!")
                elif i == 4 and ("александр" in generated_text.lower() or "1861" in generated_text):
                    correct_answers += 1
                    print("✅ Правильный ответ!")
                elif i == 5 and ("1812" in generated_text or "наполеон" in generated_text.lower()):
                    correct_answers += 1
                    print("✅ Правильный ответ!")
                else:
                    print("⚠️  Частично правильный ответ")
            else:
                print("❌ Неправильный или пустой ответ")
        
        # Результаты
        accuracy = (correct_answers / total_questions) * 100
        print("\n" + "="*50)
        print("📊 РЕЗУЛЬТАТЫ ТЕСТА")
        print("="*50)
        print(f"✅ Правильных ответов: {correct_answers}/{total_questions}")
        print(f"🎯 Точность: {accuracy:.1f}%")
        
        # Оценка качества обучения
        if accuracy >= 80:
            print("🎉 ОТЛИЧНО! Модель отлично изучила материалы!")
        elif accuracy >= 60:
            print("👍 ХОРОШО! Модель хорошо изучила материалы!")
        elif accuracy >= 40:
            print("⚠️  УДОВЛЕТВОРИТЕЛЬНО! Модель частично изучила материалы")
        else:
            print("❌ ПЛОХО! Модель слабо изучила материалы")
        
        print("="*50)
        
        return accuracy >= 40  # Считаем успешным если точность >= 40%
        
    except Exception as e:
        logger.error(f"Ошибка тестирования модели: {e}")
        print(f"❌ Ошибка: {e}")
        return False

def main():
    """Главная функция"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Быстрый тест обученной модели")
    parser.add_argument("model_path", help="Путь к обученной модели")
    parser.add_argument("--type", default="english", choices=["english", "russian"], 
                       help="Тип модели")
    
    args = parser.parse_args()
    
    # Проверяем существование модели
    if not Path(args.model_path).exists():
        print(f"❌ Модель не найдена: {args.model_path}")
        return False
    
    # Запускаем тест
    success = quick_test_model(args.model_path, args.type)
    
    if success:
        print("\n✅ Тест завершен успешно!")
        return True
    else:
        print("\n❌ Тест не пройден!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
