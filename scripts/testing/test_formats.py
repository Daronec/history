#!/usr/bin/env python3
"""
Тестирование загрузки разных форматов файлов
"""

import sys
import os
sys.path.append('src')
from train_model import load_historical_data

def test_file_formats():
    """Тестирует загрузку разных форматов файлов"""
    print('🧪 Тестируем загрузку разных форматов файлов...')
    print('=' * 60)
    
    # Тестируем JSON
    print('\n1. JSON формат:')
    try:
        json_data = load_historical_data('data/raw/sample_history_data.json')
        print(f'✅ JSON: загружено {len(json_data)} записей')
        print(f'   Первая запись: {json_data[0]["text"][:50]}...')
    except Exception as e:
        print(f'❌ JSON ошибка: {e}')
    
    # Тестируем CSV
    print('\n2. CSV формат:')
    try:
        csv_data = load_historical_data('data/raw/example_history.csv')
        print(f'✅ CSV: загружено {len(csv_data)} записей')
        print(f'   Первая запись: {csv_data[0]["text"][:50]}...')
    except Exception as e:
        print(f'❌ CSV ошибка: {e}')
    
    # Тестируем TXT
    print('\n3. TXT формат:')
    try:
        txt_data = load_historical_data('data/raw/example_history.txt')
        print(f'✅ TXT: загружено {len(txt_data)} записей')
        print(f'   Первая запись: {txt_data[0]["text"][:50]}...')
    except Exception as e:
        print(f'❌ TXT ошибка: {e}')
    
    print('\n🎉 Тестирование завершено!')

if __name__ == "__main__":
    test_file_formats()
