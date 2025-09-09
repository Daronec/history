# 🚀 Быстрый старт - ИИ для изучения истории

## 🎯 **Самые простые команды для обучения модели:**

### **Windows (PowerShell/CMD):**
```bash
# Обучение на примерах
.\train.bat sample

# Обучение на PDF учебнике
.\train.bat pdf

# Тестирование
.\train.bat test

# Демонстрация
.\train.bat demo

# Статус проекта
.\train.bat status
```

### **Linux/Mac (Makefile):**
```bash
# Обучение на примерах
make train-sample

# Обучение на PDF учебнике
make train-pdf

# Тестирование
make test-generation

# Демонстрация
make demo

# Статус проекта
make status
```

## 📋 **Полный список команд train.bat:**

| Команда | Описание |
|---------|----------|
| `.\train.bat sample` | Обучить на примерах (1 эпоха) |
| `.\train.bat pdf` | Обучить на PDF данных |
| `.\train.bat csv` | Обучить на CSV данных |
| `.\train.bat txt` | Обучить на TXT данных |
| `.\train.bat custom <путь>` | Обучить на пользовательских данных |
| `.\train.bat test` | Тест генерации текста |
| `.\train.bat demo` | Демонстрация |
| `.\train.bat status` | Статус проекта |
| `.\train.bat clean` | Очистка временных файлов |
| `.\train.bat help` | Справка |

## 🎮 **Типичный рабочий процесс:**

### **1. Первый запуск:**
```bash
# Проверяем статус
.\train.bat status

# Обучаем модель
.\train.bat sample

# Тестируем результат
.\train.bat test
```

### **2. Обучение на PDF учебнике:**
```bash
# Сначала анализируем PDF (если еще не делали)
python src/pdf_reader.py

# Затем обучаем модель
.\train.bat pdf

# Тестируем
.\train.bat test
```

### **3. Эксперименты:**
```bash
# Очищаем старые модели
.\train.bat clean

# Обучаем заново
.\train.bat sample

# Тестируем
.\train.bat test
```

## 🧪 **Тестирование результатов:**

### **Интерактивное тестирование:**
```bash
.\train.bat test
```

### **Демонстрация:**
```bash
.\train.bat demo
```

### **Jupyter Notebook:**
```bash
jupyter notebook
# Откройте notebooks/getting_started.ipynb
```

## 📊 **Проверка статуса:**

```bash
.\train.bat status
```

Покажет:
- ✅ Виртуальное окружение установлено
- ✅ Обученная модель есть
- ✅ PDF данные есть
- ✅ Примеры данных есть

## 🔧 **Решение проблем:**

### **Проблема: "train.bat не найден"**
```bash
# Используйте полный путь
.\train.bat help
```

### **Проблема: "Модель не обучается"**
```bash
# Очистите и попробуйте снова
.\train.bat clean
.\train.bat sample
```

### **Проблема: "Нет данных"**
```bash
# Проверьте статус
.\train.bat status

# Если нет PDF данных, создайте их
python src/pdf_reader.py
```

## 🎯 **Примеры использования:**

### **Быстрое обучение:**
```bash
.\train.bat sample
```

### **Обучение на своих данных:**
```bash
# Создайте файл data/raw/my_data.json
.\train.bat custom data/raw/my_data.json
```

### **Полный цикл:**
```bash
# 1. Очистка
.\train.bat clean

# 2. Обучение
.\train.bat sample

# 3. Тестирование
.\train.bat test

# 4. Демонстрация
.\train.bat demo
```

## 💡 **Советы:**

1. **Всегда активируйте виртуальное окружение** перед использованием
2. **Начните с `.\train.bat sample`** для первого теста
3. **Используйте `.\train.bat status`** для проверки состояния
4. **Очищайте модели** перед переобучением: `.\train.bat clean`
5. **Тестируйте результаты** после обучения: `.\train.bat test`

## 🎉 **Готово!**

Теперь у вас есть простая система для обучения ИИ модели изучения истории:

- **`.\train.bat sample`** - быстрое обучение
- **`.\train.bat test`** - тестирование
- **`.\train.bat demo`** - демонстрация

**Удачи в изучении истории с ИИ! 🏛️🤖**
