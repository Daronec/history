# 🏛️ ИИ для изучения истории

Проект по изучению истории с помощью искусственного интеллекта. Включает в себя обучение моделей на исторических данных, генерацию текстов и анализ исторических документов.

## 🚀 Быстрый старт

### 1. Установка

```bash
# Клонируйте репозиторий
git clone <your-repo-url>
cd history

# Запустите автоматическую установку
python setup_ai.py
```

### 2. Активация виртуального окружения

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Запуск Jupyter Notebook

```bash
jupyter notebook
```

Откройте файл `notebooks/getting_started.ipynb` для интерактивного изучения.

## 📁 Структура проекта

```
history/
├── src/                    # Исходный код
│   ├── models/            # Модели ИИ
│   │   └── history_ai.py  # Основная модель
│   └── train_model.py     # Скрипт обучения
├── notebooks/             # Jupyter notebooks
│   └── getting_started.ipynb
├── data/                  # Данные
│   ├── raw/              # Исходные данные
│   └── processed/        # Обработанные данные
├── models/               # Сохраненные модели
├── logs/                 # Логи обучения
├── configs/              # Конфигурационные файлы
├── requirements.txt      # Зависимости
└── setup_ai.py          # Скрипт установки
```

## 🤖 Возможности

### Генерация текста
- Создание исторических текстов на основе промптов
- Настройка параметров генерации (температура, длина)
- Поддержка различных исторических периодов

### Анализ данных
- Обработка исторических документов
- Классификация по периодам и категориям
- Визуализация исторических данных

### Обучение моделей
- Fine-tuning предобученных моделей
- Поддержка различных типов задач
- Автоматическое сохранение результатов

## 📚 Примеры использования

### Базовое использование

```python
from src.models.history_ai import HistoryAIModel

# Создаем модель
ai_model = HistoryAIModel()
ai_model.load_model("generation")

# Генерируем текст
prompt = "В 1812 году произошло важное событие:"
result = ai_model.generate_text(prompt, max_length=150)
print(result)
```

### Обучение модели

```bash
# Обучение на примерах данных
python src/train_model.py --data sample --task generation --epochs 3

# Обучение на собственных данных
python src/train_model.py --data data/raw/my_data.json --task classification
```

## 🛠️ Требования

- Python 3.8+
- 8GB+ RAM (рекомендуется)
- GPU (опционально, для ускорения обучения)

## 📖 Документация

- [Руководство по установке](docs/installation.md)
- [API документация](docs/api.md)
- [Примеры использования](docs/examples.md)
- [FAQ](docs/faq.md)

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте feature branch
3. Внесите изменения
4. Создайте Pull Request

## 📄 Лицензия

MIT License - см. файл [LICENSE](LICENSE)

## 🆘 Поддержка

Если у вас возникли вопросы:
- Создайте [Issue](https://github.com/your-repo/issues)
- Напишите на email: your-email@example.com
- Присоединяйтесь к нашему [Discord](https://discord.gg/your-server)

## 🎯 Планы развития

- [ ] Поддержка больше языков
- [ ] Веб-интерфейс
- [ ] API для интеграции
- [ ] Мобильное приложение
- [ ] Расширенная аналитика

---

**Сделано с ❤️ для изучения истории**