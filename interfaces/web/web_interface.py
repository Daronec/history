#!/usr/bin/env python3
"""
Веб-интерфейс для ИИ модели изучения истории
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime
from models.history_ai import HistoryAIModel
from models.history_ai_ru import HistoryAIModelRU

app = Flask(__name__)

# Глобальные переменные для моделей
english_model = None
russian_model = None

def load_models():
    """Загружает обе модели"""
    global english_model, russian_model
    
    # Получаем абсолютный путь к корню проекта
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    models_path = os.path.join(project_root, 'models')
    
    try:
        # Загружаем английскую модель
        print("🔄 Загружаем английскую модель...")
        english_model = HistoryAIModel()
        english_model.load_trained_model(os.path.join(models_path, 'history_ai_trained'))
        print("✅ Английская модель загружена")
        
        # Загружаем русскую модель (если есть)
        try:
            print("🔄 Загружаем русскую модель...")
            russian_model = HistoryAIModelRU()
            # Сначала пытаемся загрузить обученную модель, если не получается - предобученную
            try:
                russian_model.load_trained_model(os.path.join(models_path, 'history_ai_ru_trained'))
                print("✅ Обученная русская модель загружена")
            except:
                print("🔄 Загружаем предобученную русскую модель...")
                russian_model.load_model('generation')
                print("✅ Предобученная русская модель загружена")
        except Exception as e:
            print(f"⚠️ Русская модель не найдена: {e}")
            russian_model = None
            
    except Exception as e:
        print(f"❌ Ошибка загрузки моделей: {e}")
        english_model = None
        russian_model = None

@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_text():
    """API для генерации текста"""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '').strip()
        language = data.get('language', 'russian')
        max_length = int(data.get('max_length', 100))
        temperature = float(data.get('temperature', 0.7))
        
        if not prompt:
            return jsonify({'error': 'Промпт не может быть пустым'}), 400
        
        # Выбираем модель в зависимости от языка
        if language == 'russian' and russian_model:
            model = russian_model
            model_name = "Русская модель (rugpt3small)"
        elif language == 'english' and english_model:
            model = english_model
            model_name = "Английская модель (distilgpt2)"
        else:
            # Fallback на доступную модель
            if russian_model:
                model = russian_model
                model_name = "Русская модель (rugpt3small)"
            elif english_model:
                model = english_model
                model_name = "Английская модель (distilgpt2)"
            else:
                return jsonify({'error': 'Модели не загружены'}), 500
        
        # Генерируем текст
        result = model.generate_text(
            prompt=prompt,
            max_length=max_length,
            temperature=temperature
        )
        
        # Сохраняем в историю
        history_entry = {
            'timestamp': datetime.now().isoformat(),
            'prompt': prompt,
            'result': result,
            'language': language,
            'model': model_name,
            'parameters': {
                'max_length': max_length,
                'temperature': temperature
            }
        }
        
        save_to_history(history_entry)
        
        return jsonify({
            'success': True,
            'result': result,
            'model': model_name,
            'timestamp': history_entry['timestamp']
        })
        
    except Exception as e:
        return jsonify({'error': f'Ошибка генерации: {str(e)}'}), 500

@app.route('/api/history')
def get_history():
    """Получить историю запросов"""
    try:
        history = load_history()
        return jsonify({'success': True, 'history': history})
    except Exception as e:
        return jsonify({'error': f'Ошибка загрузки истории: {str(e)}'}), 500

@app.route('/api/status')
def get_status():
    """Получить статус моделей"""
    return jsonify({
        'english_model': english_model is not None,
        'russian_model': russian_model is not None,
        'timestamp': datetime.now().isoformat()
    })

def save_to_history(entry):
    """Сохраняет запись в историю"""
    try:
        history_file = '../../web_history.json'
        history = []
        
        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        
        history.append(entry)
        
        # Ограничиваем историю 100 записями
        if len(history) > 100:
            history = history[-100:]
        
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"Ошибка сохранения истории: {e}")

def load_history():
    """Загружает историю запросов"""
    try:
        history_file = '../../web_history.json'
        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Ошибка загрузки истории: {e}")
        return []

if __name__ == '__main__':
    print("🌐 Запуск веб-интерфейса для ИИ модели изучения истории")
    print("=" * 60)
    
    # Создаем папку для шаблонов
    os.makedirs('templates', exist_ok=True)
    
    # Загружаем модели
    load_models()
    
    print("🚀 Веб-сервер запущен!")
    print("📱 Откройте в браузере: http://localhost:5000")
    print("🛑 Для остановки нажмите Ctrl+C")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
