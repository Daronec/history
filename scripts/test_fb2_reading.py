#!/usr/bin/env python3
"""
Тестирование чтения FB2 файлов
"""

import sys
import os
from pathlib import Path

# Добавляем путь к src для импорта модулей
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data_processing import load_fb2_file, load_file
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_fb2_reading():
    """Тестирует чтение FB2 файлов"""
    logger.info("🧪 Тестирование чтения FB2 файлов")
    logger.info("=" * 50)
    
    # Проверяем, есть ли FB2 файлы в data/raw
    data_dir = Path("data/raw")
    if not data_dir.exists():
        logger.error(f"Директория {data_dir} не найдена")
        return
    
    # Ищем FB2 файлы
    fb2_files = list(data_dir.glob("*.fb2"))
    
    if not fb2_files:
        logger.warning("FB2 файлы не найдены в data/raw")
        logger.info("Создаем тестовый FB2 файл...")
        create_test_fb2_file()
        fb2_files = list(data_dir.glob("*.fb2"))
    
    if not fb2_files:
        logger.error("Не удалось создать тестовый FB2 файл")
        return
    
    # Тестируем каждый найденный FB2 файл
    for fb2_file in fb2_files:
        logger.info(f"\n📖 Тестируем файл: {fb2_file.name}")
        logger.info("-" * 30)
        
        try:
            # Тестируем прямое чтение FB2
            text = load_fb2_file(fb2_file)
            
            if text:
                logger.info(f"✅ FB2 файл успешно прочитан")
                logger.info(f"📊 Размер текста: {len(text):,} символов")
                logger.info(f"📝 Первые 200 символов:")
                logger.info(f"   {text[:200]}...")
                
                # Тестируем через общую функцию load_file
                text_via_load_file = load_file(fb2_file)
                if text_via_load_file == text:
                    logger.info("✅ Функция load_file работает корректно")
                else:
                    logger.warning("⚠️ Различие между load_fb2_file и load_file")
            else:
                logger.error("❌ Не удалось прочитать FB2 файл")
                
        except Exception as e:
            logger.error(f"❌ Ошибка при чтении FB2 файла: {e}")
    
    logger.info("\n" + "=" * 50)
    logger.info("✅ Тестирование FB2 завершено")

def create_test_fb2_file():
    """Создает тестовый FB2 файл"""
    test_fb2_content = '''<?xml version="1.0" encoding="utf-8"?>
<FictionBook xmlns="http://www.gribuser.ru/xml/fictionbook/2.0" xmlns:l="http://www.w3.org/1999/xlink">
<description>
    <title-info>
        <genre>history</genre>
        <author>
            <first-name>Тестовый</first-name>
            <last-name>Автор</last-name>
        </author>
        <book-title>Тестовая историческая книга</book-title>
        <annotation>
            <p>Это тестовая книга для проверки чтения FB2 файлов в системе ИИ-История.</p>
        </annotation>
        <date value="2024-01-01">2024</date>
        <lang>ru</lang>
    </title-info>
</description>
<body>
    <title>
        <p>Глава 1. Введение в историю</p>
    </title>
    <section>
        <title>
            <p>1.1. Древние времена</p>
        </title>
        <p>История — это наука, изучающая прошлое человечества. Она помогает нам понять, как развивалось общество, какие события происходили в разные эпохи.</p>
        <p>Древние цивилизации оставили нам множество артефактов и письменных источников. Археологи и историки изучают эти материалы, чтобы восстановить картину прошлого.</p>
        
        <title>
            <p>1.2. Средние века</p>
        </title>
        <p>Средние века — это период европейской истории с V по XV век. В это время происходили важные изменения в политике, экономике и культуре.</p>
        <p>Феодальная система, крестовые походы, развитие городов — все это характеризовало средневековую эпоху.</p>
        
        <title>
            <p>1.3. Новое время</p>
        </title>
        <p>Новое время началось с эпохи Возрождения и продолжалось до конца XVIII века. Это время великих географических открытий, научных революций и политических изменений.</p>
        <p>Реформация, Просвещение, промышленная революция — все эти процессы изменили мир и подготовили почву для современной эпохи.</p>
    </section>
    
    <section>
        <title>
            <p>Глава 2. Современная история</p>
        </title>
        <p>Современная история охватывает период с XIX века до наших дней. Это время бурного развития науки, техники и общества.</p>
        <p>Две мировые войны, холодная война, глобализация — все эти события сформировали современный мир.</p>
    </section>
</body>
</FictionBook>'''
    
    test_file_path = Path("data/raw/test_history_book.fb2")
    test_file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.write(test_fb2_content)
    
    logger.info(f"✅ Создан тестовый FB2 файл: {test_file_path}")

if __name__ == "__main__":
    test_fb2_reading()
