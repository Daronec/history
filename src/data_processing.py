#!/usr/bin/env python3
"""
Обработка данных для обучения моделей ИИ-История
Поддерживает различные форматы файлов: TXT, CSV, JSON, PDF, DOC, DOCX, DJVU, FB2
"""

import os
import json
import logging
from pathlib import Path

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_txt_file(file_path):
    """Загружает текстовый файл"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # Пробуем другие кодировки
        for encoding in ['cp1251', 'latin1']:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        raise ValueError(f"Не удалось декодировать файл {file_path}")

def load_csv_file(file_path):
    """Загружает CSV файл"""
    try:
        import pandas as pd
        df = pd.read_csv(file_path, encoding='utf-8')
        # Объединяем все текстовые колонки
        text_columns = df.select_dtypes(include=['object']).columns
        return ' '.join(df[text_columns].astype(str).values.flatten())
    except Exception as e:
        logger.error(f"Ошибка загрузки CSV: {e}")
        return ""

def load_json_file(file_path):
    """Загружает JSON файл"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Извлекаем текст из различных структур
        if isinstance(data, dict):
            return ' '.join(str(v) for v in data.values() if isinstance(v, str))
        elif isinstance(data, list):
            return ' '.join(str(item) for item in data if isinstance(item, str))
        else:
            return str(data)
    except Exception as e:
        logger.error(f"Ошибка загрузки JSON: {e}")
        return ""

def load_pdf_file(file_path):
    """Загружает PDF файл"""
    text = ""
    
    # Пробуем pdfplumber (лучше для сложных PDF)
    try:
        import pdfplumber
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except ImportError:
        logger.warning("pdfplumber не установлен, используем PyPDF2")
    except Exception:
        pass
    
    # Fallback на PyPDF2
    if not text:
        try:
            import PyPDF2
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except ImportError:
            logger.warning("PyPDF2 не установлен")
        except Exception as e:
            logger.error(f"Ошибка загрузки PDF: {e}")
    
    return text

def load_doc_file(file_path):
    """Загружает DOC файл (старый формат Microsoft Word)"""
    try:
        # Для старых DOC файлов используем python-docx2txt или antiword
        import subprocess
        import tempfile
        
        # Пробуем использовать antiword (если установлен)
        try:
            result = subprocess.run(['antiword', str(file_path)], 
                                  capture_output=True, text=True, encoding='utf-8')
            if result.returncode == 0:
                return result.stdout
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        # Пробуем использовать catdoc (если установлен)
        try:
            result = subprocess.run(['catdoc', str(file_path)], 
                                  capture_output=True, text=True, encoding='utf-8')
            if result.returncode == 0:
                return result.stdout
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        # Пробуем использовать python-docx2txt
        try:
            import docx2txt
            # docx2txt может работать с некоторыми DOC файлами
            return docx2txt.process(file_path)
        except Exception:
            pass
        
        # Пробуем использовать olefile для извлечения текста
        try:
            import olefile
            if olefile.isOleFile(str(file_path)):
                ole = olefile.OleFileIO(str(file_path))
                # Пытаемся найти текстовые потоки
                for stream_name in ole.listdir():
                    if 'WordDocument' in stream_name or 'Text' in stream_name:
                        try:
                            stream_data = ole.openfile(stream_name).read()
                            # Простое извлечение текста
                            text = stream_data.decode('utf-8', errors='ignore')
                            # Убираем служебные символы
                            import re
                            text = re.sub(r'[^\w\s\u0400-\u04FF\u0500-\u052F\u2DE0-\u2DFF\uA640-\uA69F]', ' ', text)
                            text = re.sub(r'\s+', ' ', text).strip()
                            if len(text) > 100:
                                ole.close()
                                return text
                        except Exception:
                            continue
                ole.close()
        except ImportError:
            pass
        except Exception:
            pass
        
        # Если ничего не работает, пытаемся прочитать как бинарный файл
        # и извлечь текстовые данные (базовый подход)
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                # Простое извлечение текста из DOC файла
                text = content.decode('utf-8', errors='ignore')
                # Убираем служебные символы
                import re
                text = re.sub(r'[^\w\s\u0400-\u04FF\u0500-\u052F\u2DE0-\u2DFF\uA640-\uA69F]', ' ', text)
                text = re.sub(r'\s+', ' ', text).strip()
                if len(text) > 100:  # Минимальная длина для валидного текста
                    return text
        except Exception:
            pass
        
        logger.warning(f"Не удалось извлечь текст из DOC файла: {file_path}")
        return ""
        
    except Exception as e:
        logger.error(f"Ошибка загрузки DOC файла: {e}")
        return ""

def load_docx_file(file_path):
    """Загружает DOCX файл"""
    try:
        from docx import Document
        doc = Document(file_path)
        return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    except ImportError:
        logger.warning("python-docx не установлен, пытаемся использовать docx2txt")
        try:
            import docx2txt
            return docx2txt.process(file_path)
        except ImportError:
            logger.error("Не установлены библиотеки для работы с DOCX файлами")
            return ""
    except Exception as e:
        logger.error(f"Ошибка загрузки DOCX файла: {e}")
        return ""

def load_djvu_file(file_path):
    """Загружает DJVU файл"""
    try:
        # Пытаемся использовать pymupdf для DJVU
        import fitz  # pymupdf
        doc = fitz.open(file_path)
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text() + "\n"
        doc.close()
        return text
    except ImportError:
        logger.warning("pymupdf не установлен для работы с DJVU")
        return ""
    except Exception as e:
        logger.error(f"Ошибка загрузки DJVU файла: {e}")
        return ""

def load_fb2_file(file_path):
    """Загружает FB2 файл (FictionBook 2.0)"""
    try:
        from bs4 import BeautifulSoup
        import zipfile
        import xml.etree.ElementTree as ET
        
        # FB2 файлы могут быть как XML, так и ZIP архивами
        if zipfile.is_zipfile(file_path):
            # FB2 в ZIP формате
            with zipfile.ZipFile(file_path, 'r') as zip_file:
                # Ищем основной файл (обычно с расширением .fb2 или без расширения)
                fb2_files = [f for f in zip_file.namelist() if f.endswith('.fb2') or '.' not in f]
                if not fb2_files:
                    logger.error(f"Не найден FB2 файл в архиве: {file_path}")
                    return ""
                
                # Читаем первый найденный FB2 файл
                with zip_file.open(fb2_files[0]) as fb2_file:
                    content = fb2_file.read()
        else:
            # Обычный FB2 файл
            with open(file_path, 'rb') as f:
                content = f.read()
        
        # Парсим XML
        try:
            # Пробуем декодировать как UTF-8
            xml_content = content.decode('utf-8')
        except UnicodeDecodeError:
            try:
                # Пробуем другие кодировки
                xml_content = content.decode('cp1251')
            except UnicodeDecodeError:
                xml_content = content.decode('latin1')
        
        # Парсим XML с помощью BeautifulSoup для лучшей обработки
        soup = BeautifulSoup(xml_content, 'xml')
        
        # Извлекаем текст из всех элементов <p> (параграфы)
        paragraphs = soup.find_all('p')
        text_parts = []
        
        for p in paragraphs:
            if p.string:
                text_parts.append(p.string.strip())
            else:
                # Если в параграфе есть вложенные элементы, извлекаем весь текст
                text_parts.append(p.get_text().strip())
        
        # Также извлекаем текст из других текстовых элементов
        text_elements = soup.find_all(['section', 'title', 'subtitle', 'epigraph', 'cite'])
        for element in text_elements:
            element_text = element.get_text().strip()
            if element_text:
                text_parts.append(element_text)
        
        # Объединяем все части текста
        full_text = '\n\n'.join(text_parts)
        
        # Очищаем текст от лишних пробелов и переносов
        import re
        full_text = re.sub(r'\n\s*\n\s*\n', '\n\n', full_text)  # Убираем множественные переносы
        full_text = re.sub(r'[ \t]+', ' ', full_text)  # Убираем лишние пробелы
        
        logger.info(f"FB2 файл успешно загружен: {len(full_text)} символов")
        return full_text.strip()
        
    except ImportError as e:
        logger.error(f"Необходимые библиотеки не установлены для FB2: {e}")
        logger.error("Установите: pip install lxml beautifulsoup4")
        return ""
    except Exception as e:
        logger.error(f"Ошибка загрузки FB2 файла: {e}")
        return ""

def load_file(file_path):
    """Загружает файл любого поддерживаемого формата"""
    file_path = Path(file_path)
    extension = file_path.suffix.lower()
    
    logger.info(f"Загружаем файл: {file_path.name} (формат: {extension})")
    
    if extension == '.txt':
        return load_txt_file(file_path)
    elif extension == '.csv':
        return load_csv_file(file_path)
    elif extension == '.json':
        return load_json_file(file_path)
    elif extension == '.pdf':
        return load_pdf_file(file_path)
    elif extension == '.doc':
        return load_doc_file(file_path)
    elif extension == '.docx':
        return load_docx_file(file_path)
    elif extension == '.djvu':
        return load_djvu_file(file_path)
    elif extension == '.fb2':
        return load_fb2_file(file_path)
    else:
        logger.warning(f"Неподдерживаемый формат файла: {extension}")
        return ""

def clean_text(text):
    """Очищает текст для обучения"""
    import re
    
    # Сначала фильтруем метаданные книг
    try:
        from metadata_filter import filter_book_metadata
        text = filter_book_metadata(text)
        logger.info("Применена фильтрация метаданных книг")
    except ImportError:
        logger.warning("Модуль фильтрации метаданных не найден, пропускаем фильтрацию")
    except Exception as e:
        logger.warning(f"Ошибка при фильтрации метаданных: {e}")
    
    # Удаляем лишние пробелы
    text = re.sub(r'\s+', ' ', text)
    
    # Удаляем специальные символы (оставляем пунктуацию)
    text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', '', text)
    
    # Удаляем пустые строки
    text = '\n'.join(line.strip() for line in text.split('\n') if line.strip())
    
    return text.strip()

def split_text_into_chunks(text, chunk_size=512, overlap=50):
    """Разбивает текст на чанки для обучения"""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        if len(chunk.strip()) > 0:
            chunks.append(chunk)
    
    return chunks

def process_data_directory(data_dir, output_file=None):
    """Обрабатывает все файлы в директории"""
    data_dir = Path(data_dir)
    all_text = []
    structured_data = []
    
    if not data_dir.exists():
        logger.error(f"Директория {data_dir} не существует")
        return []
    
    # Поддерживаемые форматы
    supported_extensions = {'.txt', '.csv', '.json', '.pdf', '.doc', '.docx', '.djvu', '.fb2'}
    
    for file_path in data_dir.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            try:
                text = load_file(file_path)
                if text:
                    cleaned_text = clean_text(text)
                    if cleaned_text:
                        all_text.append(cleaned_text)
                        
                        # Создаем структурированные данные для JSON
                        structured_item = {
                            "text": cleaned_text,
                            "source": file_path.suffix.lower()[1:],  # убираем точку
                            "filename": file_path.name,
                            "category": "общее",
                            "period": "неизвестно"
                        }
                        structured_data.append(structured_item)
                        
                        logger.info(f"Обработан файл: {file_path.name} ({len(cleaned_text)} символов)")
            except Exception as e:
                logger.error(f"Ошибка обработки файла {file_path.name}: {e}")
    
    # Сохраняем в обычный текстовый файл
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            for text in all_text:
                f.write(text + '\n\n')
        logger.info(f"Обработанные данные сохранены в: {output_file}")
    
    # Сохраняем в JSON файл для обучения модели
    json_output = data_dir.parent / "processed" / "pdf_history_data.json"
    json_output.parent.mkdir(exist_ok=True)
    
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump(structured_data, f, ensure_ascii=False, indent=2)
    logger.info(f"Структурированные данные сохранены в: {json_output}")
    
    return all_text

def get_supported_formats():
    """Возвращает список поддерживаемых форматов"""
    return {
        'txt': 'Текстовые файлы',
        'csv': 'CSV файлы',
        'json': 'JSON файлы',
        'pdf': 'PDF документы',
        'doc': 'Word документы (старый формат)',
        'docx': 'Word документы (новый формат)',
        'djvu': 'DJVU документы'
    }

if __name__ == "__main__":
    # Тестирование
    import sys
    
    if len(sys.argv) > 1:
        data_dir = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        process_data_directory(data_dir, output_file)
    else:
        print("Использование: python data_processing.py <директория_с_данными> [выходной_файл]")
        print("\nПоддерживаемые форматы:")
        for ext, desc in get_supported_formats().items():
            print(f"  .{ext} - {desc}")
