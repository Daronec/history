# 🏛️ ИИ для изучения истории - Makefile
# Универсальная структура проекта

# Переменные
PYTHON = venv/Scripts/python
PIP = venv/Scripts/pip
VENV = venv
SRC_DIR = src
SCRIPTS_DIR = scripts
INTERFACES_DIR = interfaces
DOCS_DIR = docs
DATA_DIR = data
MODELS_DIR = models
UNIVERSAL_INTERFACE = interfaces/windows/windows_interface_universal.py
BUILD_SCRIPT = scripts/build/build_universal_exe.py

# Цвета для вывода (упрощенные для Windows)
GREEN = 
YELLOW = 
RED = 
NC = 

.PHONY: help install setup train test interface build clean status

# Помощь
help:
	@echo "🏛️ ИИ для изучения истории - Универсальный интерфейс"
	@echo "Доступные команды:"
	@echo ""
	@echo "📦 Установка и настройка:"
	@echo "  make install     - Установить зависимости"
	@echo "  make setup       - Полная настройка проекта"
	@echo ""
	@echo "🎓 Обучение моделей:"
	@echo "  make train       - Обучение английской модели"
	@echo "  make train-ru    - Обучение русской модели"
	@echo "  make sample      - Создание тестовых данных"
	@echo ""
	@echo "🧪 Тестирование:"
	@echo "  make test        - Тест английской модели"
	@echo "  make test-ru     - Тест русской модели"
	@echo "  make test-formats - Тест форматов данных"
	@echo ""
	@echo "🖥️ Интерфейсы:"
	@echo "  make interface   - Запуск универсального интерфейса"
	@echo "  make web         - Запуск веб-интерфейса"
	@echo "  make launcher    - Главный лаунчер"
	@echo ""
	@echo "🔨 Сборка:"
	@echo "  make build       - Создание универсального exe"
	@echo "  make build-web   - Создание веб exe"
	@echo ""
	@echo "🧹 Очистка:"
	@echo "  make clean       - Очистка временных файлов"
	@echo "  make status      - Статус проекта"

# Установка зависимостей
install:
	@echo "📦 Установка зависимостей..."
	$(PIP) install -r requirements.txt
	@echo "✅ Зависимости установлены"

# Полная настройка
setup:
	@echo "🚀 Полная настройка проекта..."
	$(PYTHON) setup_ai.py
	@echo "✅ Проект настроен"

# Инкрементальное обучение английской модели
train:
	@echo "🎓 Инкрементальное обучение английской модели..."
	$(PYTHON) $(SRC_DIR)/train_model_incremental.py --data $(DATA_DIR)/raw --epochs 1 --model distilgpt2
	@echo "✅ Английская модель обучена"

# Инкрементальное обучение русской модели
train-ru:
	@echo "🎓 Инкрементальное обучение русской модели..."
	$(PYTHON) $(SRC_DIR)/train_model_incremental.py --data $(DATA_DIR)/raw --epochs 1 --model ai-forever/rugpt3small_based_on_gpt2
	@echo "✅ Русская модель обучена"

# Статистика изученных файлов
stats:
	@echo "📊 Статистика изученных файлов..."
	$(PYTHON) $(SRC_DIR)/train_model_incremental.py --stats
	@echo "✅ Статистика показана"

# Сброс данных обучения
reset-learning:
	@echo "🔄 Сброс данных обучения..."
	$(PYTHON) $(SRC_DIR)/train_model_incremental.py --reset
	@echo "✅ Данные обучения сброшены"

# Запуск универсального интерфейса
interface:
	@echo "🖥️ Запуск универсального интерфейса..."
	@echo "✨ Включает: промпты, файлы, переобучение"
	$(PYTHON) $(UNIVERSAL_INTERFACE)

# Запуск веб-интерфейса
web:
	@echo "🌐 Запуск веб-интерфейса..."
	@echo "📡 Сервер: http://localhost:5000"
	$(PYTHON) $(INTERFACES_DIR)/web/web_interface.py

# Главный лаунчер
launcher:
	@echo "🚀 Запуск главного лаунчера..."
	$(SCRIPTS_DIR)/launchers/Главный_лаунчер.bat

# Создание универсального exe
build:
	@echo "🔨 Создание универсального exe..."
	@echo "📦 Размер: ~9.5 МБ"
	@echo "✨ Функции: все (промпты, файлы, переобучение)"
	$(PYTHON) $(BUILD_SCRIPT)
	@echo "✅ Универсальный exe создан"

# Создание веб exe
build-web:
	@echo "🔨 Создание веб exe..."
	$(PYTHON) $(SCRIPTS_DIR)/build/build_exe.py
	@echo "✅ Веб exe создан"

# Очистка временных файлов
clean:
	@echo "🧹 Очистка временных файлов..."
	@powershell -Command "if (Test-Path 'build') { Remove-Item -Recurse -Force 'build' }"
	@powershell -Command "if (Test-Path 'dist') { Remove-Item -Recurse -Force 'dist' }"
	@powershell -Command "if (Test-Path '*.spec') { Remove-Item -Force '*.spec' }"
	@powershell -Command "if (Test-Path '__pycache__') { Remove-Item -Recurse -Force '__pycache__' }"
	@powershell -Command "if (Test-Path 'src/__pycache__') { Remove-Item -Recurse -Force 'src/__pycache__' }"
	@powershell -Command "if (Test-Path 'src/models/__pycache__') { Remove-Item -Recurse -Force 'src/models/__pycache__' }"
	@echo "✅ Очистка завершена"

# Статус проекта
status:
	@echo "📊 Статус проекта:"
	@echo ""
	@echo "📁 Структура:"
	@echo "  ✅ src/ - Исходный код"
	@echo "  ✅ scripts/ - Скрипты"
	@echo "  ✅ interfaces/ - Интерфейсы"
	@echo "  ✅ docs/ - Документация"
	@echo "  ✅ data/ - Данные"
	@echo "  ✅ models/ - Модели"
	@echo ""
	@echo "🤖 Модели:"
	@echo "  ℹ️  Проверьте папку models/ для статуса обучения"
	@echo "  ℹ️  Используйте 'make stats' для статистики изученных файлов"
	@echo ""
	@echo "🖥️ Приложения:"
	@echo "  ℹ️  Универсальный интерфейс: interfaces/windows/windows_interface_universal.py"
	@echo "  ℹ️  Exe файл: AI-History.exe (если создан)"
	@echo ""
	@echo "📚 Документация:"
	@echo "  ✅ README.md - Основная информация"
	@echo "  ✅ README_Universal_Interface.md - Универсальный интерфейс"

# Быстрый старт
quick-start: install setup sample train train-ru
	@echo "🎉 Быстрый старт завершен!"
	@echo "🚀 Теперь вы можете:"
	@echo "  make interface - Запустить универсальный интерфейс"
	@echo "  make web       - Запустить веб-интерфейс"
	@echo "  make build     - Создать exe файл"
	@echo "  make launcher  - Запустить главный лаунчер"