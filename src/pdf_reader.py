"""
Модуль для чтения и обработки PDF файлов с историческими данными
"""

import pdfplumber
import PyPDF2
import json
import re
from pathlib import Path
from typing import List, Dict, Any
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFHistoryReader:
    """Класс для чтения исторических данных из PDF файлов"""
    
    def __init__(self):
        self.supported_formats = ['.pdf']
    
    def read_pdf(self, pdf_path: str) -> List[Dict[str, Any]]:
        """
        Читает PDF файл и извлекает исторические данные
        
        Args:
            pdf_path: Путь к PDF файлу
        
        Returns:
            Список словарей с историческими данными
        """
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF файл {pdf_path} не найден")
        
        if pdf_path.suffix.lower() != '.pdf':
            raise ValueError(f"Файл {pdf_path} не является PDF")
        
        logger.info(f"Читаем PDF файл: {pdf_path}")
        
        try:
            # Пробуем pdfplumber (лучше для извлечения текста)
            return self._read_with_pdfplumber(pdf_path)
        except Exception as e:
            logger.warning(f"pdfplumber не сработал: {e}, пробуем PyPDF2")
            try:
                return self._read_with_pypdf2(pdf_path)
            except Exception as e2:
                logger.error(f"Оба метода не сработали: {e2}")
                raise
    
    def _read_with_pdfplumber(self, pdf_path: Path) -> List[Dict[str, Any]]:
        """Читает PDF с помощью pdfplumber"""
        historical_data = []
        
        with pdfplumber.open(pdf_path) as pdf:
            logger.info(f"PDF содержит {len(pdf.pages)} страниц")
            
            for page_num, page in enumerate(pdf.pages, 1):
                try:
                    # Извлекаем текст со страницы
                    text = page.extract_text()
                    
                    if text and text.strip():
                        # Разбиваем текст на абзацы
                        paragraphs = self._split_into_paragraphs(text)
                        
                        for paragraph in paragraphs:
                            if self._is_historical_content(paragraph):
                                historical_data.append({
                                    'text': paragraph.strip(),
                                    'source': 'pdf',
                                    'page': page_num,
                                    'category': self._classify_content(paragraph),
                                    'period': self._extract_period(paragraph)
                                })
                        
                        logger.info(f"Страница {page_num}: извлечено {len(paragraphs)} абзацев")
                
                except Exception as e:
                    logger.warning(f"Ошибка при чтении страницы {page_num}: {e}")
                    continue
        
        logger.info(f"Всего извлечено {len(historical_data)} исторических записей")
        return historical_data
    
    def _read_with_pypdf2(self, pdf_path: Path) -> List[Dict[str, Any]]:
        """Читает PDF с помощью PyPDF2 (резервный метод)"""
        historical_data = []
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            logger.info(f"PDF содержит {len(pdf_reader.pages)} страниц")
            
            for page_num, page in enumerate(pdf_reader.pages, 1):
                try:
                    text = page.extract_text()
                    
                    if text and text.strip():
                        paragraphs = self._split_into_paragraphs(text)
                        
                        for paragraph in paragraphs:
                            if self._is_historical_content(paragraph):
                                historical_data.append({
                                    'text': paragraph.strip(),
                                    'source': 'pdf',
                                    'page': page_num,
                                    'category': self._classify_content(paragraph),
                                    'period': self._extract_period(paragraph)
                                })
                
                except Exception as e:
                    logger.warning(f"Ошибка при чтении страницы {page_num}: {e}")
                    continue
        
        return historical_data
    
    def _split_into_paragraphs(self, text: str) -> List[str]:
        """Разбивает текст на абзацы"""
        # Убираем лишние пробелы и переносы строк
        text = re.sub(r'\s+', ' ', text)
        
        # Разбиваем по предложениям (простой подход)
        sentences = re.split(r'[.!?]+', text)
        
        # Объединяем короткие предложения в абзацы
        paragraphs = []
        current_paragraph = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            current_paragraph += sentence + ". "
            
            # Если абзац достаточно длинный, сохраняем его
            if len(current_paragraph) > 100:
                paragraphs.append(current_paragraph.strip())
                current_paragraph = ""
        
        # Добавляем последний абзац
        if current_paragraph.strip():
            paragraphs.append(current_paragraph.strip())
        
        return paragraphs
    
    def _is_historical_content(self, text: str) -> bool:
        """Определяет, является ли текст историческим содержанием"""
        # Ключевые слова для исторического контента
        historical_keywords = [
            'история', 'исторический', 'историческое',
            'году', 'веке', 'период', 'эпоха',
            'война', 'битва', 'сражение',
            'царь', 'князь', 'император',
            'революция', 'реформа', 'реформы',
            'крещение', 'основание', 'создание',
            'россия', 'русь', 'русский', 'русская'
        ]
        
        text_lower = text.lower()
        
        # Проверяем наличие исторических ключевых слов
        keyword_count = sum(1 for keyword in historical_keywords if keyword in text_lower)
        
        # Проверяем наличие дат
        has_dates = bool(re.search(r'\b\d{3,4}\s*году?\b', text))
        
        # Проверяем длину текста (должен быть достаточно информативным)
        is_long_enough = len(text) > 50
        
        return (keyword_count >= 2 or has_dates) and is_long_enough
    
    def _classify_content(self, text: str) -> str:
        """Классифицирует историческое содержание"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['война', 'битва', 'сражение', 'нашествие']):
            return 'война'
        elif any(word in text_lower for word in ['реформа', 'реформы', 'изменение', 'преобразование']):
            return 'реформы'
        elif any(word in text_lower for word in ['царь', 'князь', 'император', 'правитель']):
            return 'политика'
        elif any(word in text_lower for word in ['крещение', 'религия', 'церковь', 'вера']):
            return 'религия'
        elif any(word in text_lower for word in ['революция', 'восстание', 'переворот']):
            return 'революция'
        elif any(word in text_lower for word in ['культура', 'искусство', 'литература', 'наука']):
            return 'культура'
        else:
            return 'общее'
    
    def _extract_period(self, text: str) -> str:
        """Извлекает исторический период из текста"""
        # Ищем века
        century_match = re.search(r'(\d{1,2})\s*веке?', text)
        if century_match:
            century = century_match.group(1)
            return f"{century} век"
        
        # Ищем конкретные годы
        year_match = re.search(r'(\d{3,4})\s*году?', text)
        if year_match:
            year = int(year_match.group(1))
            if year < 1000:
                return "X век"
            elif year < 1100:
                return "XI век"
            elif year < 1200:
                return "XII век"
            elif year < 1300:
                return "XIII век"
            elif year < 1400:
                return "XIV век"
            elif year < 1500:
                return "XV век"
            elif year < 1600:
                return "XVI век"
            elif year < 1700:
                return "XVII век"
            elif year < 1800:
                return "XVIII век"
            elif year < 1900:
                return "XIX век"
            elif year < 2000:
                return "XX век"
            else:
                return "XXI век"
        
        return "неизвестно"
    
    def save_to_json(self, data: List[Dict[str, Any]], output_path: str):
        """Сохраняет извлеченные данные в JSON файл"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Данные сохранены в {output_path}")

def main():
    """Основная функция для тестирования"""
    pdf_path = "data/raw/Учебник_История_России_образование.x90326.pdf"
    
    if not Path(pdf_path).exists():
        print(f"❌ PDF файл не найден: {pdf_path}")
        return
    
    print("📚 Читаем PDF учебник по истории России...")
    print("=" * 60)
    
    try:
        reader = PDFHistoryReader()
        historical_data = reader.read_pdf(pdf_path)
        
        print(f"✅ Успешно извлечено {len(historical_data)} исторических записей")
        
        # Показываем первые несколько записей
        print("\n📖 Примеры извлеченного контента:")
        for i, item in enumerate(historical_data[:3], 1):
            print(f"\n{i}. Страница {item['page']} - {item['category']} - {item['period']}")
            print(f"   {item['text'][:150]}...")
        
        # Сохраняем в JSON
        output_path = "data/processed/pdf_history_data.json"
        reader.save_to_json(historical_data, output_path)
        print(f"\n💾 Данные сохранены в {output_path}")
        
        # Статистика
        categories = {}
        periods = {}
        for item in historical_data:
            cat = item['category']
            period = item['period']
            categories[cat] = categories.get(cat, 0) + 1
            periods[period] = periods.get(period, 0) + 1
        
        print(f"\n📊 Статистика:")
        print(f"Категории: {categories}")
        print(f"Периоды: {periods}")
        
    except Exception as e:
        print(f"❌ Ошибка при чтении PDF: {e}")

if __name__ == "__main__":
    main()
