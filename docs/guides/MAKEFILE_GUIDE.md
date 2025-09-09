# 🛠️ Руководство по использованию Makefile

## 🎯 **Основные команды для обучения модели:**

### **Быстрый старт:**
```bash
make quick-start    # Настройка + обучение на примерах
```

### **Обучение на разных данных:**
```bash
make train-sample      # На примерах (1 эпоха)
make train-sample-long # На примерах (3 эпохи)
make train-pdf         # На данных из PDF учебника
make train-csv         # На CSV данных
make train-txt         # На TXT данных
```

### **Обучение на пользовательских данных:**
```bash
make train-custom DATA=data/raw/my_data.json
```

## 🧪 **Тестирование:**

```bash
make test-generation   # Тест генерации текста
make test-qa          # Тест системы вопросов и ответов
make test-formats     # Тест загрузки форматов
```

## 📚 **Анализ данных:**

```bash
make pdf-analysis     # Анализ PDF учебника
make demo            # Демонстрация
make jupyter         # Запуск Jupyter Notebook
```

## 🔧 **Управление проектом:**

```bash
make setup           # Настройка проекта
make install         # Установка зависимостей
make clean           # Очистка временных файлов
make clean-models    # Удаление обученных моделей
make status          # Статус проекта
```

## 📊 **Информация:**

```bash
make help            # Справка по всем командам
make info            # Информация о проекте
```

## 🎮 **Примеры использования:**

### **1. Первый запуск:**
```bash
make quick-start
```

### **2. Обучение на PDF учебнике:**
```bash
make pdf-analysis    # Сначала извлекаем данные
make train-pdf       # Затем обучаем модель
```

### **3. Эксперименты:**
```bash
make train-sample    # 1 эпоха
make train-sample-long  # 3 эпохи
make test-generation    # Тестируем результат
```

### **4. Очистка и переобучение:**
```bash
make clean-models    # Удаляем старые модели
make train-sample    # Обучаем заново
```

## 🚀 **Продвинутые команды:**

### **Для разработки:**
```bash
make dev-install     # Зависимости для разработки
make format          # Форматирование кода
make lint            # Проверка кода
```

### **Эксперименты:**
```bash
make experiment-1    # Сравнение источников данных
make experiment-2    # Влияние количества эпох
```

## 💡 **Советы:**

1. **Всегда активируйте виртуальное окружение** перед использованием команд
2. **Используйте `make status`** для проверки состояния проекта
3. **Начните с `make quick-start`** для первого запуска
4. **Используйте `make clean-models`** перед переобучением
5. **Проверяйте результаты** с помощью `make test-generation`

## 🎯 **Типичный рабочий процесс:**

```bash
# 1. Настройка
make setup

# 2. Обучение
make train-sample

# 3. Тестирование
make test-generation

# 4. Если нужно переобучить
make clean-models
make train-sample-long

# 5. Демонстрация
make demo
```

---

**Теперь обучение модели стало намного проще! 🎉**
