#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль для фильтрации метаданных книг
Удаляет информацию о тираже, ISBN, издательстве и других служебных данных
"""

import re
import logging
from typing import List, Dict, Set

logger = logging.getLogger(__name__)

class BookMetadataFilter:
    """Фильтр метаданных книг для очистки текста от служебной информации"""
    
    def __init__(self):
        """Инициализация фильтра с паттернами метаданных"""
        self.metadata_patterns = self._init_metadata_patterns()
        self.publisher_keywords = self._init_publisher_keywords()
        self.isbn_patterns = self._init_isbn_patterns()
        self.copyright_patterns = self._init_copyright_patterns()
        
    def _init_metadata_patterns(self) -> List[re.Pattern]:
        """Инициализация паттернов метаданных"""
        patterns = [
            # Тираж
            r'тираж\s*:?\s*\d+[\s\w]*',
            r'тираж\s*\d+[\s\w]*',
            r'тираж\s*—?\s*\d+[\s\w]*',
            r'экземпляров?',
            
            # Год издания
            r'год\s*издания\s*:?\s*\d{4}',
            r'издано\s*в\s*\d{4}',
            r'©\s*\d{4}',
            r'copyright\s*\d{4}',
            
            # Количество страниц
            r'\d+\s*стр\.',
            r'\d+\s*страниц',
            r'\d+\s*с\.',
            r'стр\.\s*\d+',
            
            # Формат
            r'формат\s*:?\s*[\d\w\s×х/]+',
            r'размер\s*:?\s*[\d\w\s×х/]+',
            r'\d+×\d+/\d+',
            
            # Переплет
            r'переплет\s*:?\s*[\w\s]+',
            r'обложка\s*:?\s*[\w\s]+',
            
            # ББК, УДК
            r'ББК\s*:?\s*[\d\.]+',
            r'УДК\s*:?\s*[\d\.]+',
            
            # Серия
            r'серия\s*:?\s*[\w\s«»""]+',
            r'избранное',
            r'библиотека\s*[\w\s]+',
            
            # Дополнительные паттерны
            r'все права защищены',
            r'all rights reserved',
            r'защищено авторским правом',
        ]
        
        return [re.compile(pattern, re.IGNORECASE | re.UNICODE) for pattern in patterns]
    
    def _init_publisher_keywords(self) -> Set[str]:
        """Ключевые слова издательств"""
        return {
            'издательство', 'издатель', 'издано', 'издание', 'издал',
            'publisher', 'published', 'publishing', 'press',
            'эксмо', 'аст', 'дрофа', 'просвещение', 'наука', 'академия',
            'росмэн', 'махаон', 'белый город', 'вече', 'молодая гвардия',
            'художественная литература', 'детская литература',
            'советский писатель', 'современник', 'знание'
        }
    
    def _init_isbn_patterns(self) -> List[re.Pattern]:
        """Паттерны для ISBN"""
        patterns = [
            r'ISBN\s*:?\s*[\d\-X]+',
            r'ISBN\s*[\d\-X]+',
            r'isbn\s*:?\s*[\d\-X]+',
            r'isbn\s*[\d\-X]+',
        ]
        return [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
    
    def _init_copyright_patterns(self) -> List[re.Pattern]:
        """Паттерны авторских прав"""
        patterns = [
            r'©\s*[\d\w\s,\.]+',
            r'copyright\s*[\d\w\s,\.]+',
            r'авторские права\s*[\d\w\s,\.]+',
            r'все права защищены',
            r'all rights reserved',
        ]
        return [re.compile(pattern, re.IGNORECASE | re.UNICODE) for pattern in patterns]
    
    def filter_metadata(self, text: str) -> str:
        """
        Фильтрует метаданные из текста
        
        Args:
            text: Исходный текст
            
        Returns:
            Очищенный от метаданных текст
        """
        if not text:
            return text
            
        # Применяем все фильтры
        filtered_text = text
        
        # Фильтруем по паттернам
        for pattern in self.metadata_patterns:
            filtered_text = pattern.sub('', filtered_text)
        
        # Фильтруем ISBN
        for pattern in self.isbn_patterns:
            filtered_text = pattern.sub('', filtered_text)
        
        # Фильтруем авторские права
        for pattern in self.copyright_patterns:
            filtered_text = pattern.sub('', filtered_text)
        
        # Фильтруем строки с издательствами
        filtered_text = self._filter_publisher_lines(filtered_text)
        
        # Фильтруем служебные строки
        filtered_text = self._filter_service_lines(filtered_text)
        
        # Очищаем результат
        filtered_text = self._clean_result(filtered_text)
        
        return filtered_text
    
    def _filter_publisher_lines(self, text: str) -> str:
        """Фильтрует строки с информацией об издательстве"""
        lines = text.split('\n')
        filtered_lines = []
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Пропускаем строки с ключевыми словами издательств
            if any(keyword in line_lower for keyword in self.publisher_keywords):
                # Проверяем, не является ли это частью основного текста
                if not self._is_content_line(line):
                    continue
            
            filtered_lines.append(line)
        
        return '\n'.join(filtered_lines)
    
    def _is_content_line(self, line: str) -> bool:
        """Проверяет, является ли строка частью основного контента"""
        line = line.strip()
        
        # Слишком короткие строки
        if len(line) < 20:
            return False
        
        # Строки с большим количеством цифр (вероятно метаданные)
        digit_ratio = sum(c.isdigit() for c in line) / len(line)
        if digit_ratio > 0.3:
            return False
        
        # Строки с множественными специальными символами
        special_chars = sum(1 for c in line if c in '.,;:()[]{}')
        if special_chars > len(line) * 0.2:
            return False
        
        return True
    
    def _filter_service_lines(self, text: str) -> str:
        """Фильтрует служебные строки"""
        lines = text.split('\n')
        filtered_lines = []
        
        for line in lines:
            line = line.strip()
            
            # Пропускаем пустые строки
            if not line:
                continue
            
            # Пропускаем строки с только цифрами и символами
            if re.match(r'^[\d\s\-\.:;]+$', line):
                continue
            
            # Пропускаем строки с только заглавными буквами (вероятно заголовки)
            if line.isupper() and len(line) < 50:
                continue
            
            # Пропускаем строки с датами
            if re.match(r'^\d{1,2}[\.\-/]\d{1,2}[\.\-/]\d{2,4}$', line):
                continue
            
            filtered_lines.append(line)
        
        return '\n'.join(filtered_lines)
    
    def _clean_result(self, text: str) -> str:
        """Очищает результат фильтрации"""
        # Убираем множественные пробелы
        text = re.sub(r'\s+', ' ', text)
        
        # Убираем множественные переносы строк
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        
        # Убираем пробелы в начале и конце строк
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join(line for line in lines if line)
        
        return text.strip()
    
    def get_filtered_statistics(self, original_text: str, filtered_text: str) -> Dict[str, int]:
        """Возвращает статистику фильтрации"""
        return {
            'original_length': len(original_text),
            'filtered_length': len(filtered_text),
            'removed_length': len(original_text) - len(filtered_text),
            'removal_percentage': round((len(original_text) - len(filtered_text)) / len(original_text) * 100, 2) if original_text else 0
        }

# Глобальный экземпляр фильтра
metadata_filter = BookMetadataFilter()

def filter_book_metadata(text: str) -> str:
    """
    Удобная функция для фильтрации метаданных книг
    
    Args:
        text: Исходный текст
        
    Returns:
        Очищенный от метаданных текст
    """
    return metadata_filter.filter_metadata(text)

def get_filtering_stats(original_text: str, filtered_text: str) -> Dict[str, int]:
    """
    Возвращает статистику фильтрации
    
    Args:
        original_text: Исходный текст
        filtered_text: Отфильтрованный текст
        
    Returns:
        Словарь со статистикой
    """
    return metadata_filter.get_filtered_statistics(original_text, filtered_text)

# Пример использования
if __name__ == "__main__":
    # Тестовый текст с метаданными
    test_text = """
    История России
    
    Глава 1. Древняя Русь
    
    В древние времена на территории современной России...
    
    Издательство: Эксмо
    Год издания: 2020
    Тираж: 5000 экземпляров
    ISBN: 978-5-699-12345-6
    Формат: 70×100/16
    Переплет: твердый
    ББК: 63.3(2)
    УДК: 94(47)
    
    © 2020 Издательство Эксмо
    Все права защищены
    
    Глава 2. Средневековая Русь
    
    В средние века Русь переживала...
    """
    
    # Фильтруем метаданные
    filtered = filter_book_metadata(test_text)
    
    # Получаем статистику
    stats = get_filtering_stats(test_text, filtered)
    
    print("Исходный текст:")
    print(test_text)
    print("\n" + "="*50 + "\n")
    print("Отфильтрованный текст:")
    print(filtered)
    print("\n" + "="*50 + "\n")
    print("Статистика фильтрации:")
    for key, value in stats.items():
        print(f"{key}: {value}")
