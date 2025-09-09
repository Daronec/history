#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Альтернативная обработка PDF файлов с использованием PyMuPDF
"""

import os
import sys
from pathlib import Path
import logging
from typing import Optional, List

# Добавляем путь к модулям
sys.path.append(str(Path(__file__).parent))

from data_processing import load_file

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_text_with_pymupdf(pdf_path: Path) -> Optional[str]:
    """
    Извлекает текст из PDF с помощью PyMuPDF (fitz)
    
    Args:
        pdf_path: Путь к PDF файлу
        
    Returns:
        Извлеченный текст или None
    """
    try:
        import fitz  # PyMuPDF
        
        logger.info(f"Обрабатываем {pdf_path.name} с помощью PyMuPDF")
        
        doc = fitz.open(pdf_path)
        all_text = []
        
        # Обрабатываем все страницы
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Извлекаем текст
            page_text = page.get_text()
            
            if page_text.strip():
                all_text.append(page_text)
                logger.info(f"Страница {page_num + 1}: {len(page_text)} символов")
            else:
                logger.warning(f"Страница {page_num + 1}: нет текста")
        
        doc.close()
        
        if all_text:
            return '\n\n'.join(all_text)
        else:
            return None
            
    except Exception as e:
        logger.error(f"Ошибка при обработке с PyMuPDF: {e}")
        return None

def extract_text_with_pdfplumber(pdf_path: Path) -> Optional[str]:
    """
    Извлекает текст из PDF с помощью pdfplumber
    
    Args:
        pdf_path: Путь к PDF файлу
        
    Returns:
        Извлеченный текст или None
    """
    try:
        import pdfplumber
        
        logger.info(f"Обрабатываем {pdf_path.name} с помощью pdfplumber")
        
        all_text = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                
                if page_text and page_text.strip():
                    all_text.append(page_text)
                    logger.info(f"Страница {page_num + 1}: {len(page_text)} символов")
                else:
                    logger.warning(f"Страница {page_num + 1}: нет текста")
        
        if all_text:
            return '\n\n'.join(all_text)
        else:
            return None
            
    except Exception as e:
        logger.error(f"Ошибка при обработке с pdfplumber: {e}")
        return None

def alternative_pdf_processing(pdf_path: Path) -> Optional[str]:
    """
    Альтернативная обработка PDF файла с несколькими методами
    
    Args:
        pdf_path: Путь к PDF файлу
        
    Returns:
        Извлеченный текст или None
    """
    logger.info(f"Альтернативная обработка: {pdf_path.name}")
    
    # Метод 1: Обычная обработка
    text1 = load_file(pdf_path)
    logger.info(f"Метод 1 (обычный): {len(text1) if text1 else 0} символов")
    
    # Метод 2: PyMuPDF
    text2 = extract_text_with_pymupdf(pdf_path)
    logger.info(f"Метод 2 (PyMuPDF): {len(text2) if text2 else 0} символов")
    
    # Метод 3: pdfplumber
    text3 = extract_text_with_pdfplumber(pdf_path)
    logger.info(f"Метод 3 (pdfplumber): {len(text3) if text3 else 0} символов")
    
    # Выбираем лучший результат
    texts = [text1, text2, text3]
    best_text = max(texts, key=lambda x: len(x) if x else 0)
    
    if best_text and len(best_text) > 100:
        logger.info(f"✅ Лучший результат: {len(best_text)} символов")
        return best_text
    else:
        logger.warning(f"❌ Не удалось извлечь достаточно текста")
        return None

def process_test_data_alternative():
    """
    Обрабатывает все файлы в test_data альтернативными методами
    """
    test_data_dir = Path("test_data")
    
    if not test_data_dir.exists():
        logger.error("Папка test_data не найдена")
        return
    
    pdf_files = list(test_data_dir.glob("*.pdf"))
    logger.info(f"Найдено PDF файлов: {len(pdf_files)}")
    
    all_texts = []
    
    for pdf_file in pdf_files:
        logger.info(f"\n{'='*60}")
        logger.info(f"Обрабатываем: {pdf_file.name}")
        
        text = alternative_pdf_processing(pdf_file)
        
        if text:
            all_texts.append({
                'filename': pdf_file.name,
                'text': text,
                'length': len(text)
            })
            logger.info(f"✅ Успешно: {len(text):,} символов")
        else:
            logger.warning(f"❌ Не удалось обработать: {pdf_file.name}")
    
    # Сохраняем результаты
    if all_texts:
        output_file = Path("data/processed/alternative_pdf_data.json")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        import json
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_texts, f, ensure_ascii=False, indent=2)
        
        logger.info(f"\n✅ Результаты сохранены в {output_file}")
        logger.info(f"📊 Обработано файлов: {len(all_texts)}")
        logger.info(f"📝 Общий объем текста: {sum(item['length'] for item in all_texts):,} символов")
        
        # Показываем статистику
        for item in all_texts:
            logger.info(f"  - {item['filename']}: {item['length']:,} символов")
    else:
        logger.error("❌ Не удалось обработать ни одного файла")

if __name__ == "__main__":
    process_test_data_alternative()
