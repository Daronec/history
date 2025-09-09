# 📥 Руководство по установке ИИ для изучения истории

## 🖥️ Системные требования

### Минимальные требования:
- **ОС**: Windows 10/11, macOS 10.14+, Ubuntu 18.04+
- **Python**: 3.8 или выше
- **RAM**: 4GB (рекомендуется 8GB+)
- **Место на диске**: 2GB свободного места

### Рекомендуемые требования:
- **RAM**: 16GB+
- **GPU**: NVIDIA GPU с поддержкой CUDA (для ускорения)
- **SSD**: Для быстрой загрузки моделей

## 🐍 Установка Python

### Windows:
1. Скачайте Python с [python.org](https://www.python.org/downloads/)
2. При установке **обязательно** отметьте "Add Python to PATH"
3. Проверьте установку: `python --version`

### macOS:
```bash
# Через Homebrew
brew install python

# Или скачайте с python.org
```

### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

## 🚀 Автоматическая установка

1. **Скачайте проект**:
   ```bash
   git clone <your-repo-url>
   cd history
   ```

2. **Запустите автоматическую установку**:
   ```bash
   python setup_ai.py
   ```

   Скрипт автоматически:
   - Создаст виртуальное окружение
   - Установит все зависимости
   - Создаст структуру проекта
   - Настроит конфигурацию

## 🔧 Ручная установка

Если автоматическая установка не работает:

### 1. Создайте виртуальное окружение:
```bash
python -m venv venv
```

### 2. Активируйте окружение:

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

### 3. Обновите pip:
```bash
pip install --upgrade pip
```

### 4. Установите зависимости:
```bash
pip install -r requirements.txt
```

### 5. Создайте структуру проекта:
```bash
mkdir -p src/models data/raw data/processed models logs configs notebooks
```

## 🧪 Проверка установки

Запустите тест:
```bash
python quick_start.py
```

Или проверьте вручную:
```python
import torch
import transformers
from src.models.history_ai import HistoryAIModel

print("✅ Установка прошла успешно!")
```

## 🐛 Решение проблем

### Ошибка "Python не найден":
- Убедитесь, что Python добавлен в PATH
- Попробуйте `python3` вместо `python`

### Ошибка при установке PyTorch:
```bash
# Для CPU версии
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Для GPU версии (NVIDIA)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Ошибка "No module named 'transformers'":
```bash
pip install transformers
```

### Проблемы с памятью:
- Закройте другие программы
- Используйте меньшие модели
- Уменьшите batch_size в настройках

### Медленная работа:
- Установите GPU версию PyTorch
- Используйте SSD диск
- Увеличьте RAM

## 🔄 Обновление

Для обновления до новой версии:
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## 🗑️ Удаление

Для полного удаления:
```bash
# Удалите папку проекта
rm -rf history/

# Удалите виртуальное окружение (если создавали отдельно)
rm -rf venv/
```

## 📞 Поддержка

Если у вас возникли проблемы:

1. **Проверьте логи**: Посмотрите на сообщения об ошибках
2. **Обновите зависимости**: `pip install -r requirements.txt --upgrade`
3. **Создайте Issue**: Опишите проблему с подробностями
4. **Напишите в Discord**: Получите помощь от сообщества

## 🎯 Следующие шаги

После успешной установки:

1. **Запустите Jupyter**: `jupyter notebook`
2. **Откройте tutorial**: `notebooks/getting_started.ipynb`
3. **Попробуйте примеры**: `python quick_start.py`
4. **Обучите модель**: `python src/train_model.py --data sample`

---

**Удачи в изучении истории с ИИ! 🏛️🤖**
