#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для диагностики проблемных PDF файлов
"""

import os
import sys
from pathlib import Path
import logging

# Добавляем путь к модулям
sys.path.append(str(Path(__file__).parent))

from data_processing import load_file

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def diagnose_pdf_file(file_path: Path):
    """
    Диагностирует PDF файл и пытается извлечь текст разными методами
    
    Args:
        file_path: Путь к PDF файлу
    """
    print(f"\n🔍 Диагностика файла: {file_path.name}")
    print("=" * 50)
    
    # Проверяем размер файла
    file_size = file_path.stat().st_size
    print(f"📏 Размер файла: {file_size:,} байт ({file_size/1024/1024:.2f} MB)")
    
    # Пытаемся загрузить файл
    try:
        text = load_file(file_path)
        if text:
            print(f"✅ Успешно извлечен текст: {len(text):,} символов")
            print(f"📝 Первые 200 символов: {text[:200]}...")
        else:
            print("❌ Не удалось извлечь текст")
    except Exception as e:
        print(f"❌ Ошибка при загрузке: {e}")
    
    # Дополнительная диагностика с PyPDF2
    try:
        import PyPDF2
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            print(f"📄 Количество страниц (PyPDF2): {len(pdf_reader.pages)}")
            
            # Пытаемся извлечь текст с первой страницы
            if len(pdf_reader.pages) > 0:
                first_page = pdf_reader.pages[0]
                first_page_text = first_page.extract_text()
                print(f"📝 Текст первой страницы (PyPDF2): {len(first_page_text):,} символов")
                if first_page_text:
                    print(f"📝 Первые 100 символов: {first_page_text[:100]}...")
                else:
                    print("❌ PyPDF2 не смог извлечь текст")
    except Exception as e:
        print(f"❌ Ошибка PyPDF2: {e}")
    
    # Дополнительная диагностика с pdfplumber
    try:
        import pdfplumber
        with pdfplumber.open(file_path) as pdf:
            print(f"📄 Количество страниц (pdfplumber): {len(pdf.pages)}")
            
            # Пытаемся извлечь текст с первой страницы
            if len(pdf.pages) > 0:
                first_page = pdf.pages[0]
                first_page_text = first_page.extract_text()
                print(f"📝 Текст первой страницы (pdfplumber): {len(first_page_text):,} символов")
                if first_page_text:
                    print(f"📝 Первые 100 символов: {first_page_text[:100]}...")
                else:
                    print("❌ pdfplumber не смог извлечь текст")
    except Exception as e:
        print(f"❌ Ошибка pdfplumber: {e}")

def main():
    test_data_dir = Path("test_data")
    
    if not test_data_dir.exists():
        print("❌ Папка test_data не найдена")
        return
    
    print("🔍 Диагностика всех PDF файлов в test_data")
    print("=" * 60)
    
    pdf_files = list(test_data_dir.glob("*.pdf"))
    print(f"📁 Найдено PDF файлов: {len(pdf_files)}")
    
    for pdf_file in pdf_files:
        diagnose_pdf_file(pdf_file)
    
    print("\n✅ Диагностика завершена!")

if __name__ == "__main__":
    main()
