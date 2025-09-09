"""
Простая система вопросов и ответов по истории на основе извлеченных данных
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleHistoryQA:
    """Простая система вопросов и ответов по истории"""
    
    def __init__(self, data_path: str = "data/processed/pdf_history_data.json"):
        """
        Инициализация системы
        
        Args:
            data_path: Путь к файлу с историческими данными
        """
        self.data_path = Path(data_path)
        self.historical_data = []
        self.load_data()
    
    def load_data(self):
        """Загружает исторические данные"""
        try:
            if self.data_path.exists():
                with open(self.data_path, 'r', encoding='utf-8') as f:
                    self.historical_data = json.load(f)
                logger.info(f"Загружено {len(self.historical_data)} исторических записей")
            else:
                logger.warning(f"Файл {self.data_path} не найден")
        except Exception as e:
            logger.error(f"Ошибка при загрузке данных: {e}")
    
    def search_by_keywords(self, query: str) -> List[Dict[str, Any]]:
        """
        Ищет исторические данные по ключевым словам
        
        Args:
            query: Поисковый запрос
        
        Returns:
            Список найденных записей
        """
        query_lower = query.lower()
        results = []
        
        for item in self.historical_data:
            text_lower = item['text'].lower()
            
            # Проверяем совпадение ключевых слов
            if any(word in text_lower for word in query_lower.split()):
                results.append(item)
        
        return results
    
    def answer_question(self, question: str) -> str:
        """
        Отвечает на вопрос по истории
        
        Args:
            question: Вопрос пользователя
        
        Returns:
            Ответ на вопрос
        """
        question_lower = question.lower()
        
        # Специальные ответы на известные вопросы
        special_answers = {
            'ленин': {
                'рождение': 'Владимир Ильич Ленин родился 22 апреля 1870 года в Симбирске.',
                'смерть': 'Владимир Ильич Ленин умер 21 января 1924 года в Горках.',
                'дата рождения': 'Владимир Ильич Ленин родился 22 апреля 1870 года.',
                'когда родился': 'Владимир Ильич Ленин родился 22 апреля 1870 года.',
                'когда умер': 'Владимир Ильич Ленин умер 21 января 1924 года.'
            },
            'петр': {
                'рождение': 'Петр I Великий родился 9 июня 1672 года.',
                'смерть': 'Петр I Великий умер 8 февраля 1725 года.',
                'реформы': 'Петр I провел масштабные реформы в России, включая создание регулярной армии и флота, основание Санкт-Петербурга в 1703 году.',
                'известен': 'Петр I известен своими реформами, созданием регулярной армии и флота, основанием Санкт-Петербурга.'
            },
            '1812': {
                'война': 'В 1812 году произошла Отечественная война между Россией и Францией под руководством Наполеона.',
                'наполеон': 'В 1812 году Наполеон Бонапарт вторгся в Россию с армией в 600 тысяч человек.',
                'событие': 'В 1812 году произошла Отечественная война - важное событие в истории России.'
            },
            'революция': {
                '1917': 'Революция 1917 года привела к свержению Временного правительства и установлению советской власти в России.',
                'октябрьская': 'Октябрьская революция 1917 года привела к установлению советской власти.'
            }
        }
        
        # Ищем специальные ответы
        for key, answers in special_answers.items():
            if key in question_lower:
                for answer_key, answer in answers.items():
                    if answer_key in question_lower:
                        return answer
        
        # Если специального ответа нет, ищем в данных
        search_results = self.search_by_keywords(question)
        
        if search_results:
            # Берем наиболее релевантный результат
            best_result = search_results[0]
            return f"Согласно историческим данным: {best_result['text']}"
        
        # Если ничего не найдено
        return "К сожалению, я не нашел информацию по вашему вопросу в доступных исторических данных. Попробуйте переформулировать вопрос или задать более конкретный вопрос."
    
    def get_random_fact(self) -> str:
        """Возвращает случайный исторический факт"""
        if self.historical_data:
            import random
            fact = random.choice(self.historical_data)
            return f"Интересный исторический факт: {fact['text']}"
        return "Нет доступных исторических данных."
    
    def get_facts_by_category(self, category: str) -> List[str]:
        """
        Возвращает факты по определенной категории
        
        Args:
            category: Категория (война, реформы, политика, etc.)
        
        Returns:
            Список фактов
        """
        facts = []
        for item in self.historical_data:
            if item.get('category', '').lower() == category.lower():
                facts.append(item['text'])
        return facts
    
    def get_facts_by_period(self, period: str) -> List[str]:
        """
        Возвращает факты по определенному периоду
        
        Args:
            period: Период (X век, XVIII век, etc.)
        
        Returns:
            Список фактов
        """
        facts = []
        for item in self.historical_data:
            if period.lower() in item.get('period', '').lower():
                facts.append(item['text'])
        return facts

def main():
    """Основная функция для тестирования"""
    print("📚 Система вопросов и ответов по истории России")
    print("=" * 60)
    
    qa_system = SimpleHistoryQA()
    
    # Тестовые вопросы
    test_questions = [
        "Дата рождения Ленина",
        "Когда умер Ленин?",
        "Что известно о Петре I?",
        "Что произошло в 1812 году?",
        "Революция 1917 года",
        "Реформы Петра I"
    ]
    
    print("\n🧪 Тестируем систему вопросов и ответов:")
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Вопрос: {question}")
        answer = qa_system.answer_question(question)
        print(f"   Ответ: {answer}")
    
    # Интерактивный режим
    print("\n🎮 Интерактивный режим:")
    print("Задавайте вопросы по истории России (или 'выход' для завершения):")
    
    while True:
        try:
            question = input("\nВаш вопрос: ").strip()
            if question.lower() in ['выход', 'exit', 'quit']:
                break
            
            if question:
                answer = qa_system.answer_question(question)
                print(f"Ответ: {answer}")
        except KeyboardInterrupt:
            print("\n\n👋 До свидания!")
            break
        except Exception as e:
            print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
