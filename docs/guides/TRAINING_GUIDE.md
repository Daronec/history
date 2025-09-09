# 🎓 Руководство по обучению ИИ модели для изучения истории

## 📚 Обзор

Это руководство покажет вам, как обучать ИИ модель для генерации и анализа исторических текстов.

## 🎯 Типы обучения

### 1. **Fine-tuning (Дообучение)**
- Берем предобученную модель (DistilGPT2, GPT-2, etc.)
- Обучаем на исторических данных
- Модель лучше понимает исторический контекст

### 2. **Обучение с нуля**
- Создаем модель с нуля
- Требует больше данных и времени
- Подходит для специализированных задач

## 🚀 Быстрый старт

### Шаг 1: Подготовка данных

```bash
# Убедитесь, что у вас есть данные
ls data/raw/
# Должен быть файл sample_history_data.json
```

### Шаг 2: Базовое обучение

```bash
# Активируйте виртуальное окружение
venv\Scripts\activate

# Обучите модель на примерах (1 эпоха)
python src/train_model.py --data sample --task generation --epochs 1 --model distilgpt2
```

### Шаг 3: Проверка результатов

```bash
# Протестируйте обученную модель
python -c "
from src.models.history_ai import HistoryAIModel
ai = HistoryAIModel()
ai.load_trained_model('./models/history_ai_trained')
result = ai.generate_text('В 1812 году произошло:', max_length=100)
print(result)
"
```

## 📊 Подготовка собственных данных

### Формат данных

Создайте файл `data/raw/my_history_data.json`:

```json
[
  {
    "text": "Ваш исторический текст здесь",
    "category": "война",
    "period": "XIX век",
    "importance": "высокая"
  },
  {
    "text": "Еще один исторический факт",
    "category": "реформы", 
    "period": "XVIII век",
    "importance": "средняя"
  }
]
```

### Категории данных

- **война** - военные конфликты
- **реформы** - государственные реформы
- **политика** - политические события
- **религия** - религиозные события
- **революция** - революционные события
- **культура** - культурные достижения

## ⚙️ Параметры обучения

### Основные параметры

```bash
python src/train_model.py \
  --data data/raw/my_data.json \    # Путь к данным
  --task generation \               # Тип задачи
  --epochs 3 \                     # Количество эпох
  --model distilgpt2               # Модель
```

### Дополнительные параметры

- `--epochs` - количество эпох (1-10)
- `--model` - модель (distilgpt2, gpt2, microsoft/DialoGPT-medium)
- `--task` - тип задачи (generation, classification)

## 🔧 Настройка обучения

### Изменение параметров в коде

Отредактируйте `src/models/history_ai.py`:

```python
training_args = TrainingArguments(
    output_dir="./models/history_ai_trained",
    num_train_epochs=num_epochs,           # Количество эпох
    per_device_train_batch_size=4,         # Размер батча
    per_device_eval_batch_size=4,          # Размер батча для валидации
    warmup_steps=500,                      # Шаги разогрева
    weight_decay=0.01,                     # Регуляризация
    learning_rate=5e-5,                    # Скорость обучения
    logging_dir="./logs",                  # Папка для логов
    logging_steps=10,                      # Частота логирования
    save_steps=1000,                       # Частота сохранения
    save_total_limit=2,                    # Максимум сохранений
)
```

## 📈 Мониторинг обучения

### Логи обучения

```bash
# Просмотр логов
tail -f logs/trainer_state.json

# Или используйте TensorBoard
tensorboard --logdir logs
```

### Метрики качества

- **Loss** - потери модели (меньше = лучше)
- **Perplexity** - сложность текста
- **BLEU Score** - качество генерации

## 🎮 Практические примеры

### Пример 1: Обучение на русской истории

```bash
# Создайте файл data/raw/russian_history.json
python src/train_model.py --data data/raw/russian_history.json --epochs 2
```

### Пример 2: Обучение на конкретном периоде

```bash
# Данные только о XIX веке
python src/train_model.py --data data/raw/19th_century.json --epochs 3
```

### Пример 3: Классификация исторических событий

```bash
# Обучение для классификации
python src/train_model.py --data sample --task classification --epochs 2
```

## 🚨 Решение проблем

### Проблема: "Out of memory"

**Решение:**
```python
# Уменьшите размер батча
per_device_train_batch_size=2  # вместо 4
```

### Проблема: "Model not learning"

**Решение:**
- Увеличьте количество эпох
- Проверьте качество данных
- Уменьшите learning_rate

### Проблема: "Poor text generation"

**Решение:**
- Добавьте больше данных
- Увеличьте max_length в генерации
- Настройте temperature

## 📊 Оценка качества

### Автоматическая оценка

```python
from src.models.history_ai import HistoryAIModel

ai = HistoryAIModel()
ai.load_trained_model('./models/history_ai_trained')

# Тестируем на разных промптах
test_prompts = [
    "В 1812 году произошло:",
    "Петр I известен тем, что:",
    "Революция 1917 года:"
]

for prompt in test_prompts:
    result = ai.generate_text(prompt, max_length=100)
    print(f"Промпт: {prompt}")
    print(f"Результат: {result}")
    print("-" * 50)
```

### Ручная оценка

1. **Релевантность** - соответствует ли текст теме?
2. **Фактическая точность** - правильные ли исторические факты?
3. **Связность** - логично ли построен текст?
4. **Стиль** - подходит ли стиль для исторического текста?

## 🎯 Продвинутые техники

### 1. Transfer Learning

```python
# Загружаем предобученную модель
ai = HistoryAIModel("microsoft/DialoGPT-medium")
ai.load_model("generation")

# Дообучаем на исторических данных
ai.train(historical_dataset, num_epochs=2)
```

### 2. Data Augmentation

```python
# Увеличиваем данные
augmented_texts = []
for text in original_texts:
    # Добавляем вариации
    augmented_texts.append(text)
    augmented_texts.append(text.replace("году", "г."))
    augmented_texts.append(text.replace("произошло", "случилось"))
```

### 3. Multi-task Learning

```python
# Обучение на нескольких задачах одновременно
tasks = ["generation", "classification", "summarization"]
for task in tasks:
    ai.load_model(task)
    ai.train(task_datasets[task])
```

## 📚 Рекомендации

### Для начинающих:
1. Начните с малого количества эпох (1-2)
2. Используйте небольшие модели (DistilGPT2)
3. Тестируйте на простых промптах

### Для продвинутых:
1. Экспериментируйте с архитектурами
2. Используйте большие датасеты
3. Применяйте продвинутые техники

### Общие советы:
- Всегда делайте бэкап данных
- Сохраняйте промежуточные результаты
- Документируйте эксперименты
- Тестируйте на разных данных

## 🎉 Заключение

Обучение ИИ модели для истории - это итеративный процесс. Начните с простого, экспериментируйте и постепенно улучшайте результаты.

**Удачи в изучении истории с ИИ! 🏛️🤖**
