#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для тестирования фильтрации метаданных на реальных данных
"""

import sys
import os
from pathlib import Path

# Добавляем путь к модулям
sys.path.append(str(Path(__file__).parent.parent / "src"))

from metadata_filter import filter_book_metadata, get_filtering_stats
from data_processing import load_file
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_metadata_filtering():
    """Тестирует фильтрацию метаданных на реальных файлах"""
    
    # Путь к данным
    data_dir = Path("data/raw")
    
    if not data_dir.exists():
        logger.error(f"Директория {data_dir} не существует")
        return
    
    # Поддерживаемые форматы
    supported_extensions = {'.txt', '.pdf', '.doc', '.docx'}
    
    total_original = 0
    total_filtered = 0
    files_processed = 0
    
    print("🧪 Тестирование фильтрации метаданных книг")
    print("=" * 60)
    
    for file_path in data_dir.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            try:
                print(f"\n📄 Обрабатываем файл: {file_path.name}")
                
                # Загружаем файл
                original_text = load_file(file_path)
                
                if not original_text:
                    print("   ⚠️ Файл пустой или не удалось загрузить")
                    continue
                
                # Фильтруем метаданные
                filtered_text = filter_book_metadata(original_text)
                
                # Получаем статистику
                stats = get_filtering_stats(original_text, filtered_text)
                
                # Выводим результаты
                print(f"   📊 Статистика:")
                print(f"      Исходный размер: {stats['original_length']:,} символов")
                print(f"      После фильтрации: {stats['filtered_length']:,} символов")
                print(f"      Удалено: {stats['removed_length']:,} символов ({stats['removal_percentage']}%)")
                
                # Обновляем общую статистику
                total_original += stats['original_length']
                total_filtered += stats['filtered_length']
                files_processed += 1
                
                # Показываем примеры удаленного контента
                if stats['removal_percentage'] > 10:
                    print(f"   ✅ Значительная фильтрация метаданных")
                elif stats['removal_percentage'] > 5:
                    print(f"   ⚠️ Умеренная фильтрация")
                else:
                    print(f"   ℹ️ Минимальная фильтрация")
                
            except Exception as e:
                logger.error(f"Ошибка при обработке файла {file_path}: {e}")
                continue
    
    # Общая статистика
    print("\n" + "=" * 60)
    print("📈 ОБЩАЯ СТАТИСТИКА")
    print("=" * 60)
    print(f"Обработано файлов: {files_processed}")
    print(f"Общий исходный размер: {total_original:,} символов")
    print(f"Общий размер после фильтрации: {total_filtered:,} символов")
    
    if total_original > 0:
        total_removal_percentage = round((total_original - total_filtered) / total_original * 100, 2)
        print(f"Общий процент удаления: {total_removal_percentage}%")
        print(f"Сэкономлено места: {total_original - total_filtered:,} символов")
    
    print("\n🎯 РЕКОМЕНДАЦИИ:")
    if total_original > 0:
        if total_removal_percentage > 20:
            print("✅ Отличная фильтрация! Много метаданных удалено")
        elif total_removal_percentage > 10:
            print("✅ Хорошая фильтрация метаданных")
        elif total_removal_percentage > 5:
            print("⚠️ Умеренная фильтрация, возможно нужно улучшить паттерны")
        else:
            print("⚠️ Слабая фильтрация, проверьте качество данных")
    
    print("\n💡 СОВЕТЫ:")
    print("- Фильтрация метаданных улучшает качество обучения модели")
    print("- Удаление служебной информации делает текст более чистым")
    print("- Меньше шума = лучше качество генерации")

if __name__ == "__main__":
    test_metadata_filtering()
