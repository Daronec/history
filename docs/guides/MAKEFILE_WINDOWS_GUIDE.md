# 🪟 Руководство по Makefile для Windows

## ✅ **Makefile теперь работает на Windows!**

### 🚀 **Основные команды:**

```bash
# Справка по командам
make help

# Статус проекта
make status

# Обучение модели
make train-sample
make train-pdf

# Тестирование
make test-generation

# Демонстрация
make demo

# Очистка
make clean
```

## 📋 **Полный список команд:**

| Команда | Описание |
|---------|----------|
| `make help` | Показать справку по командам |
| `make install` | Установить зависимости |
| `make setup` | Настроить проект |
| `make train-sample` | Обучить модель на примерах |
| `make train-sample-long` | Обучить модель на примерах (3 эпохи) |
| `make train-pdf` | Обучить модель на PDF данных |
| `make train-csv` | Обучить модель на CSV данных |
| `make train-txt` | Обучить модель на TXT данных |
| `make train-custom DATA=путь` | Обучить на пользовательских данных |
| `make test-generation` | Протестировать генерацию текста |
| `make test-qa` | Протестировать систему вопросов и ответов |
| `make test-formats` | Протестировать форматы файлов |
| `make pdf-analysis` | Проанализировать PDF учебник |
| `make demo` | Запустить демонстрацию |
| `make jupyter` | Запустить Jupyter Notebook |
| `make quick-start` | Быстрый старт (настройка + обучение) |
| `make clean` | Очистить временные файлы |
| `make clean-models` | Удалить обученные модели |
| `make status` | Показать статус проекта |
| `make dev-install` | Установить зависимости для разработки |
| `make format` | Форматировать код |
| `make lint` | Проверить код на ошибки |
| `make experiment-1` | Эксперимент 1: Сравнение данных |
| `make experiment-2` | Эксперимент 2: Влияние эпох |
| `make info` | Показать информацию о проекте |

## 🎯 **Типичный рабочий процесс:**

### **1. Первый запуск:**
```bash
# Проверяем статус
make status

# Обучаем модель
make train-sample

# Тестируем результат
make test-generation
```

### **2. Обучение на PDF учебнике:**
```bash
# Сначала анализируем PDF
make pdf-analysis

# Затем обучаем модель
make train-pdf

# Тестируем
make test-generation
```

### **3. Эксперименты:**
```bash
# Очищаем старые модели
make clean-models

# Обучаем заново
make train-sample

# Тестируем
make test-generation
```

## 🧪 **Тестирование результатов:**

### **Генерация текста:**
```bash
make test-generation
```

### **Система вопросов и ответов:**
```bash
make test-qa
```

### **Демонстрация:**
```bash
make demo
```

### **Jupyter Notebook:**
```bash
make jupyter
# Откройте в браузере: http://localhost:8888
```

## 🔧 **Решение проблем:**

### **Проблема: "make не найден"**
```bash
# Установите make для Windows
# Или используйте train.bat вместо make
.\train.bat help
```

### **Проблема: "Модель не обучается"**
```bash
# Очистите и попробуйте снова
make clean-models
make train-sample
```

### **Проблема: "Нет данных"**
```bash
# Проверьте статус
make status

# Если нет PDF данных, создайте их
make pdf-analysis
```

## 🎮 **Примеры использования:**

### **Быстрое обучение:**
```bash
make train-sample
```

### **Обучение на своих данных:**
```bash
# Создайте файл data/raw/my_data.json
make train-custom DATA=data/raw/my_data.json
```

### **Полный цикл:**
```bash
# 1. Очистка
make clean

# 2. Обучение
make train-sample

# 3. Тестирование
make test-generation

# 4. Демонстрация
make demo
```

### **Эксперименты:**
```bash
# Эксперимент 1: Сравнение разных источников данных
make experiment-1

# Эксперимент 2: Влияние количества эпох
make experiment-2
```

## 💡 **Советы:**

1. **Всегда активируйте виртуальное окружение** перед использованием
2. **Начните с `make train-sample`** для первого теста
3. **Используйте `make status`** для проверки состояния
4. **Очищайте модели** перед переобучением: `make clean-models`
5. **Тестируйте результаты** после обучения: `make test-generation`

## 🆚 **Makefile vs train.bat:**

| Функция | Makefile | train.bat |
|---------|----------|-----------|
| **Совместимость** | Linux/Mac/Windows | Только Windows |
| **Команды** | `make <команда>` | `.\train.bat <команда>` |
| **Функциональность** | Полная | Основная |
| **Сложность** | Средняя | Простая |

## 🎉 **Готово!**

Теперь у вас есть два способа управления проектом:

- **`make <команда>`** - для Linux/Mac/Windows
- **`.\train.bat <команда>`** - для Windows (проще)

**Удачи в изучении истории с ИИ! 🏛️🤖**
