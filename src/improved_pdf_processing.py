#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Улучшенная обработка PDF файлов с поддержкой OCR
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

def extract_text_with_ocr(pdf_path: Path) -> Optional[str]:
    """
    Извлекает текст из PDF с помощью OCR (если доступен)
    
    Args:
        pdf_path: Путь к PDF файлу
        
    Returns:
        Извлеченный текст или None
    """
    try:
        import pytesseract
        from PIL import Image
        import fitz  # PyMuPDF
        
        logger.info(f"Пытаемся использовать OCR для {pdf_path.name}")
        
        # Открываем PDF с помощью PyMuPDF
        doc = fitz.open(pdf_path)
        all_text = []
        
        # Обрабатываем первые 5 страниц (чтобы не перегружать систему)
        max_pages = min(5, len(doc))
        
        for page_num in range(max_pages):
            page = doc[page_num]
            
            # Сначала пытаемся извлечь текст обычным способом
            page_text = page.get_text()
            if page_text.strip():
                all_text.append(page_text)
                logger.info(f"Страница {page_num + 1}: извлечен текст ({len(page_text)} символов)")
            else:
                # Если текста нет, пытаемся OCR
                try:
                    # Конвертируем страницу в изображение
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # Увеличиваем разрешение
                    img_data = pix.tobytes("png")
                    
                    # Открываем изображение с помощью PIL
                    import io
                    img = Image.open(io.BytesIO(img_data))
                    
                    # Применяем OCR
                    ocr_text = pytesseract.image_to_string(img, lang='rus+eng')
                    
                    if ocr_text.strip():
                        all_text.append(ocr_text)
                        logger.info(f"Страница {page_num + 1}: OCR извлек текст ({len(ocr_text)} символов)")
                    else:
                        logger.warning(f"Страница {page_num + 1}: OCR не смог извлечь текст")
                        
                except Exception as e:
                    logger.warning(f"Ошибка OCR на странице {page_num + 1}: {e}")
        
        doc.close()
        
        if all_text:
            return '\n\n'.join(all_text)
        else:
            return None
            
    except ImportError:
        logger.warning("OCR библиотеки не установлены. Устанавливаем...")
        return None
    except Exception as e:
        logger.error(f"Ошибка при OCR обработке: {e}")
        return None

def improved_pdf_processing(pdf_path: Path) -> Optional[str]:
    """
    Улучшенная обработка PDF файла
    
    Args:
        pdf_path: Путь к PDF файлу
        
    Returns:
        Извлеченный текст или None
    """
    logger.info(f"Улучшенная обработка: {pdf_path.name}")
    
    # Сначала пытаемся обычную обработку
    text = load_file(pdf_path)
    
    if text and len(text) > 1000:  # Если извлечено достаточно текста
        logger.info(f"Обычная обработка успешна: {len(text)} символов")
        return text
    
    # Если текста мало, пытаемся OCR
    logger.info(f"Мало текста ({len(text) if text else 0} символов), пробуем OCR...")
    ocr_text = extract_text_with_ocr(pdf_path)
    
    if ocr_text and len(ocr_text) > len(text or ""):
        logger.info(f"OCR успешен: {len(ocr_text)} символов")
        return ocr_text
    elif text:
        logger.info(f"Используем обычный текст: {len(text)} символов")
        return text
    else:
        logger.warning(f"Не удалось извлечь текст из {pdf_path.name}")
        return None

def process_test_data_improved():
    """
    Обрабатывает все файлы в test_data с улучшенными методами
    """
    test_data_dir = Path("test_data")
    
    if not test_data_dir.exists():
        logger.error("Папка test_data не найдена")
        return
    
    pdf_files = list(test_data_dir.glob("*.pdf"))
    logger.info(f"Найдено PDF файлов: {len(pdf_files)}")
    
    all_texts = []
    
    for pdf_file in pdf_files:
        logger.info(f"\n{'='*50}")
        logger.info(f"Обрабатываем: {pdf_file.name}")
        
        text = improved_pdf_processing(pdf_file)
        
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
        output_file = Path("data/processed/improved_pdf_data.json")
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
    process_test_data_improved()
