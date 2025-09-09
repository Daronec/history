# 🔧 Решение проблем с моделями

## 🚨 **Частые ошибки загрузки моделей**

### **Ошибка: "Модели не загружены"**

#### **Причины:**
- Отсутствует подключение к интернету
- Модели не обучены
- Проблемы с зависимостями
- Неправильные пути к файлам

#### **Решения:**

**1. Проверьте подключение к интернету**
```bash
# Проверьте интернет
ping google.com
```

**2. Обучите модели**
```bash
# Быстрое обучение русской модели
scripts\launchers\quick_train_ru.bat

# Или через Python
python scripts\training\quick_train_ru.py
```

**3. Установите зависимости**
```bash
pip install -r requirements.txt
```

**4. Проверьте наличие данных**
```bash
# Убедитесь, что есть данные для обучения
dir data\raw
```

## 🎯 **Пошаговое решение**

### **Шаг 1: Проверка структуры**
```bash
# Проверьте наличие папок
dir models
dir data\raw
dir src\models
```

### **Шаг 2: Обучение моделей**
```bash
# Создайте тестовые данные
python scripts\testing\test_formats.py

# Обучите русскую модель
python scripts\training\train_model_ru.py

# Обучите английскую модель
python src\train_model.py
```

### **Шаг 3: Проверка моделей**
```bash
# Проверьте, что модели созданы
dir models\history_ai_trained
dir models\history_ai_ru_trained
```

### **Шаг 4: Тестирование**
```bash
# Тест русской модели
python scripts\testing\test_generation_ru.py

# Тест английской модели
python scripts\testing\test_generation.py
```

## 🔍 **Диагностика проблем**

### **Проверка статуса моделей**
```bash
# Через Makefile
make status

# Или через главный лаунчер
scripts\launchers\Главный_лаунчер.bat
```

### **Проверка логов**
```bash
# Посмотрите логи в папке logs/
dir logs
```

### **Проверка зависимостей**
```bash
# Проверьте установленные пакеты
pip list | findstr torch
pip list | findstr transformers
pip list | findstr flask
```

## 🛠️ **Исправление конкретных ошибок**

### **Ошибка: "ModuleNotFoundError"**
```bash
# Установите недостающие модули
pip install torch transformers flask pandas numpy
```

### **Ошибка: "CUDA out of memory"**
```bash
# Используйте CPU вместо GPU
# В коде установите device='cpu'
```

### **Ошибка: "Connection timeout"**
```bash
# Проверьте интернет
# Попробуйте позже
# Используйте VPN если нужно
```

### **Ошибка: "File not found"**
```bash
# Проверьте пути к файлам
# Убедитесь, что папки существуют
# Создайте недостающие папки
```

## 🎯 **Быстрые решения**

### **Полная переустановка**
```bash
# 1. Удалите виртуальное окружение
rmdir /s /q venv

# 2. Создайте новое
python -m venv venv
venv\Scripts\activate

# 3. Установите зависимости
pip install -r requirements.txt

# 4. Обучите модели
python scripts\training\quick_train_ru.py
```

### **Очистка и перезапуск**
```bash
# Очистите временные файлы
make clean

# Перезапустите интерфейс
python interfaces\windows\windows_interface.py
```

## 📊 **Проверка работоспособности**

### **Тест 1: Базовые импорты**
```python
import torch
import transformers
import flask
print("✅ Все модули импортированы")
```

### **Тест 2: Загрузка моделей**
```python
from src.models.history_ai import HistoryAIModel
model = HistoryAIModel()
print("✅ Модель создана")
```

### **Тест 3: Генерация текста**
```python
result = model.generate_text("Тест")
print(f"✅ Результат: {result}")
```

## 🎉 **Предотвращение проблем**

### **Регулярное обслуживание**
```bash
# Обновляйте зависимости
pip install --upgrade -r requirements.txt

# Очищайте временные файлы
make clean

# Проверяйте статус
make status
```

### **Резервное копирование**
```bash
# Сохраните обученные модели
xcopy models\history_ai_trained backup\ /s /e
xcopy models\history_ai_ru_trained backup\ /s /e
```

### **Мониторинг**
```bash
# Следите за логами
tail -f logs\*.log

# Проверяйте использование диска
dir models /s
```

## 🆘 **Если ничего не помогает**

### **1. Полная диагностика**
```bash
# Соберите информацию о системе
python --version
pip --version
dir models
dir data
```

### **2. Переустановка с нуля**
```bash
# Удалите все и начните заново
rmdir /s /q venv
rmdir /s /q models
rmdir /s /q logs

# Следуйте инструкциям в INSTALL.md
```

### **3. Обращение за помощью**
- Проверьте документацию в `docs/guides/`
- Посмотрите примеры в `docs/examples/`
- Проверьте логи ошибок

## 🎯 **Чек-лист решения проблем**

- [ ] Проверено подключение к интернету
- [ ] Установлены все зависимости
- [ ] Созданы тестовые данные
- [ ] Обучены модели
- [ ] Проверена структура папок
- [ ] Протестирована генерация текста
- [ ] Очищены временные файлы
- [ ] Перезапущен интерфейс

---

**🔧 Следуйте этому руководству для решения проблем с моделями!**
