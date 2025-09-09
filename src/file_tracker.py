#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Система отслеживания изученных файлов для инкрементального обучения
"""

import json
import hashlib
import os
from pathlib import Path
from typing import Dict, List, Set
import logging

logger = logging.getLogger(__name__)

class FileTracker:
    """
    Класс для отслеживания изученных файлов
    """
    
    def __init__(self, tracking_file: str = "data/processed/learned_files.json"):
        """
        Инициализация трекера файлов
        
        Args:
            tracking_file: Путь к файлу отслеживания
        """
        self.tracking_file = Path(tracking_file)
        self.tracking_file.parent.mkdir(parents=True, exist_ok=True)
        self.learned_files = self._load_tracking_data()
    
    def _load_tracking_data(self) -> Dict:
        """
        Загружает данные отслеживания из файла
        
        Returns:
            Словарь с информацией об изученных файлах
        """
        if self.tracking_file.exists():
            try:
                with open(self.tracking_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logger.info(f"Загружены данные о {len(data.get('files', {}))} изученных файлах")
                    return data
            except Exception as e:
                logger.warning(f"Ошибка загрузки файла отслеживания: {e}")
        
        return {
            "files": {},
            "last_update": None,
            "total_files_learned": 0
        }
    
    def _save_tracking_data(self):
        """
        Сохраняет данные отслеживания в файл
        """
        try:
            with open(self.tracking_file, 'w', encoding='utf-8') as f:
                json.dump(self.learned_files, f, ensure_ascii=False, indent=2)
            logger.info(f"Данные отслеживания сохранены в {self.tracking_file}")
        except Exception as e:
            logger.error(f"Ошибка сохранения файла отслеживания: {e}")
    
    def _get_file_hash(self, file_path: Path) -> str:
        """
        Вычисляет хеш файла для отслеживания изменений
        
        Args:
            file_path: Путь к файлу
            
        Returns:
            MD5 хеш файла
        """
        try:
            with open(file_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
            return file_hash
        except Exception as e:
            logger.error(f"Ошибка вычисления хеша файла {file_path}: {e}")
            return ""
    
    def is_file_learned(self, file_path: Path) -> bool:
        """
        Проверяет, был ли файл уже изучен
        
        Args:
            file_path: Путь к файлу
            
        Returns:
            True если файл уже изучен
        """
        file_key = str(file_path)
        if file_key in self.learned_files["files"]:
            # Проверяем, не изменился ли файл
            current_hash = self._get_file_hash(file_path)
            stored_hash = self.learned_files["files"][file_key]["hash"]
            
            if current_hash == stored_hash:
                logger.info(f"Файл {file_path.name} уже изучен (хеш совпадает)")
                return True
            else:
                logger.info(f"Файл {file_path.name} изменился, требуется переобучение")
                return False
        
        return False
    
    def mark_file_as_learned(self, file_path: Path, text_length: int, processing_method: str):
        """
        Отмечает файл как изученный
        
        Args:
            file_path: Путь к файлу
            text_length: Длина извлеченного текста
            processing_method: Метод обработки файла
        """
        file_key = str(file_path)
        file_hash = self._get_file_hash(file_path)
        
        self.learned_files["files"][file_key] = {
            "filename": file_path.name,
            "hash": file_hash,
            "text_length": text_length,
            "processing_method": processing_method,
            "learned_at": str(Path.cwd()),
            "size": file_path.stat().st_size
        }
        
        self.learned_files["total_files_learned"] = len(self.learned_files["files"])
        self.learned_files["last_update"] = str(Path.cwd())
        
        logger.info(f"Файл {file_path.name} отмечен как изученный ({text_length} символов)")
        self._save_tracking_data()
    
    def get_new_files(self, file_paths: List[Path]) -> List[Path]:
        """
        Возвращает список новых файлов для изучения
        
        Args:
            file_paths: Список всех файлов
            
        Returns:
            Список новых файлов
        """
        new_files = []
        for file_path in file_paths:
            if not self.is_file_learned(file_path):
                new_files.append(file_path)
        
        logger.info(f"Найдено {len(new_files)} новых файлов из {len(file_paths)} общих")
        return new_files
    
    def get_learned_files_info(self) -> Dict:
        """
        Возвращает информацию об изученных файлах
        
        Returns:
            Словарь с информацией
        """
        return {
            "total_files": len(self.learned_files["files"]),
            "total_text_length": sum(
                file_info["text_length"] 
                for file_info in self.learned_files["files"].values()
            ),
            "files": self.learned_files["files"]
        }
    
    def reset_tracking(self):
        """
        Сбрасывает данные отслеживания
        """
        self.learned_files = {
            "files": {},
            "last_update": None,
            "total_files_learned": 0
        }
        self._save_tracking_data()
        logger.info("Данные отслеживания сброшены")
