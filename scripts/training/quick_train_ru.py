#!/usr/bin/env python3
"""
Быстрое обучение русской модели
"""

import sys
import os
sys.path.append('../../src')

def main():
    """Основная функция"""
    print("🇷🇺 Быстрое обучение русской модели")
    print("=" * 50)
    
    try:
        # Импортируем модуль обучения
        from train_model_ru import main as train_main
        
        print("🚀 Начинаем обучение русской модели...")
        print("📊 Это может занять несколько минут...")
        print()
        
        # Запускаем обучение
        train_main()
        
        print()
        print("✅ Обучение русской модели завершено!")
        print("🎉 Теперь можно использовать русскую модель в интерфейсе")
        
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("💡 Убедитесь, что все зависимости установлены")
        print("   pip install -r requirements.txt")
        
    except Exception as e:
        print(f"❌ Ошибка обучения: {e}")
        print("💡 Проверьте наличие данных в папке data/raw/")

if __name__ == "__main__":
    main()
