#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Инкрементальная обработка данных с отслеживанием изученных файлов
"""

import os
import sys
import json
from pathlib import Path
import logging
from typing import List, Dict, Optional, Union

# Добавляем путь к модулям
sys.path.append(str(Path(__file__).parent))

from data_processing import load_file, process_data_directory
from file_tracker import FileTracker

logger = logging.getLogger(__name__)

class IncrementalDataProcessor:
    """
    Класс для инкрементальной обработки данных
    """
    
    def __init__(self, tracking_file: str = "data/processed/learned_files.json"):
        """
        Инициализация процессора
        
        Args:
            tracking_file: Путь к файлу отслеживания
        """
        self.tracker = FileTracker(tracking_file)
        self.processed_data_file = Path("data/processed/pdf_history_data.json")
        self.processed_data_file.parent.mkdir(parents=True, exist_ok=True)
    
    def process_new_files(self, data_path: Union[Path, str, List[Path]]) -> List[Dict]:
        """
        Обрабатывает только новые файлы
        
        Args:
            data_path: Путь к данным (файл, директория или список файлов)
            
        Returns:
            Список новых обработанных данных
        """
        logger.info(f"Начинаем инкрементальную обработку: {data_path}")
        
        # Получаем список всех файлов
        if isinstance(data_path, list):
            # Если передан список файлов
            all_files = data_path
        elif isinstance(data_path, (str, Path)):
            data_path = Path(data_path)
            if data_path.is_dir():
                all_files = list(data_path.glob("*"))
                # Фильтруем только поддерживаемые форматы
                supported_extensions = {'.pdf', '.txt', '.doc', '.docx', '.djvu', '.fb2'}
                all_files = [f for f in all_files if f.suffix.lower() in supported_extensions]
            else:
                all_files = [data_path]
        else:
            raise ValueError(f"Неподдерживаемый тип data_path: {type(data_path)}")
        
        # Получаем только новые файлы
        new_files = self.tracker.get_new_files(all_files)
        
        if not new_files:
            logger.info("Нет новых файлов для обработки")
            return []
        
        logger.info(f"Обрабатываем {len(new_files)} новых файлов")
        
        new_data = []
        for file_path in new_files:
            try:
                logger.info(f"Обрабатываем новый файл: {file_path.name}")
                
                # Обрабатываем файл
                text = load_file(file_path)
                
                # Улучшенная валидация текста
                if text:
                    # Убираем лишние пробелы и проверяем длину
                    cleaned_text = text.strip()
                    
                    if len(cleaned_text) > 200:  # Увеличиваем минимальную длину
                        # Дополнительная очистка текста
                        from data_processing import clean_text
                        final_text = clean_text(cleaned_text)
                        
                        if final_text and len(final_text.strip()) > 100:
                            # Создаем запись данных
                            data_entry = {
                                'filename': file_path.name,
                                'text': final_text,
                                'original_length': len(text),
                                'processed_length': len(final_text),
                                'file_path': str(file_path)
                            }
                            new_data.append(data_entry)
                            
                            # Отмечаем файл как изученный
                            self.tracker.mark_file_as_learned(
                                file_path, 
                                len(final_text), 
                                "incremental_processing"
                            )
                            
                            logger.info(f"✅ Файл {file_path.name} обработан: {len(final_text)} символов (исходно: {len(text)})")
                        else:
                            logger.warning(f"⚠️ Файл {file_path.name} содержит мало текста после очистки: {len(final_text) if final_text else 0} символов")
                    else:
                        logger.warning(f"⚠️ Файл {file_path.name} содержит мало текста: {len(cleaned_text)} символов")
                else:
                    logger.warning(f"⚠️ Файл {file_path.name} не содержит текста или не удалось его извлечь")
                    
            except Exception as e:
                logger.error(f"❌ Ошибка обработки файла {file_path.name}: {e}")
        
        # Обновляем основной файл данных
        if new_data:
            self._update_processed_data_file(new_data)
        
        return new_data
    
    def _update_processed_data_file(self, new_data: List[Dict]):
        """
        Обновляет основной файл обработанных данных
        
        Args:
            new_data: Новые данные для добавления
        """
        try:
            # Загружаем существующие данные
            existing_data = []
            if self.processed_data_file.exists():
                with open(self.processed_data_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            
            # Добавляем новые данные
            existing_data.extend(new_data)
            
            # Сохраняем обновленные данные
            with open(self.processed_data_file, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Файл {self.processed_data_file} обновлен: добавлено {len(new_data)} записей")
            
        except Exception as e:
            logger.error(f"Ошибка обновления файла данных: {e}")
    
    def get_processing_stats(self) -> Dict:
        """
        Возвращает статистику обработки
        
        Returns:
            Словарь со статистикой
        """
        learned_info = self.tracker.get_learned_files_info()
        
        # Загружаем данные из основного файла
        total_records = 0
        if self.processed_data_file.exists():
            try:
                with open(self.processed_data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    total_records = len(data)
            except:
                pass
        
        return {
            "learned_files": learned_info["total_files"],
            "total_text_length": learned_info["total_text_length"],
            "total_records": total_records,
            "tracking_file": str(self.tracker.tracking_file)
        }
    
    def reset_learning(self):
        """
        Сбрасывает данные обучения
        """
        self.tracker.reset_tracking()
        if self.processed_data_file.exists():
            self.processed_data_file.unlink()
        logger.info("Данные обучения сброшены")

def main():
    """
    Основная функция для тестирования
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Инкрементальная обработка данных')
    parser.add_argument('--data', type=str, required=True, help='Путь к данным')
    parser.add_argument('--reset', action='store_true', help='Сбросить данные обучения')
    parser.add_argument('--stats', action='store_true', help='Показать статистику')
    
    args = parser.parse_args()
    
    # Настройка логирования
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    processor = IncrementalDataProcessor()
    
    if args.reset:
        processor.reset_learning()
        return
    
    if args.stats:
        stats = processor.get_processing_stats()
        print(f"📊 Статистика обработки:")
        print(f"  Изучено файлов: {stats['learned_files']}")
        print(f"  Общий объем текста: {stats['total_text_length']:,} символов")
        print(f"  Записей в данных: {stats['total_records']}")
        return
    
    data_path = Path(args.data)
    if not data_path.exists():
        logger.error(f"Путь не найден: {data_path}")
        return
    
    # Обрабатываем новые файлы
    new_data = processor.process_new_files(data_path)
    
    if new_data:
        print(f"✅ Обработано {len(new_data)} новых файлов")
        for item in new_data:
            print(f"  - {item['filename']}: {item['processed_length']:,} символов")
    else:
        print("ℹ️ Нет новых файлов для обработки")

if __name__ == "__main__":
    main()
