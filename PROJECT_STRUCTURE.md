# 📁 Структура проекта "ИИ для изучения истории"

## 🎯 **Улучшенная организация**

Проект был реорганизован для лучшей навигации и понимания. Все файлы теперь логично распределены по папкам.

## 📂 **Новая структура**

```
history/
├── 📁 src/                           # Исходный код
│   ├── models/                       # Модели ИИ
│   │   ├── history_ai.py            # Английская модель
│   │   └── history_ai_ru.py         # Русская модель
│   ├── data/                        # Обработка данных
│   ├── utils/                       # Утилиты
│   ├── train_model.py               # Обучение английской модели
│   ├── pdf_reader.py                # Чтение PDF файлов
│   └── simple_history_qa.py         # Простая Q&A система
│
├── 📁 interfaces/                    # Пользовательские интерфейсы
│   ├── web/                         # Веб-интерфейс
│   │   ├── web_interface.py         # Flask приложение
│   │   ├── web_interface_exe.py     # Точка входа для exe
│   │   └── templates/               # HTML шаблоны
│   │       └── index.html           # Главная страница
│   └── windows/                     # Windows интерфейс
│       └── windows_interface.py     # Tkinter приложение
│
├── 📁 scripts/                       # Скрипты и утилиты
│   ├── launchers/                   # Запускающие скрипты
│   │   ├── Главный_лаунчер.bat      # Главное меню
│   │   ├── train.bat                # Обучение и тестирование
│   │   ├── train_ru.bat             # Русские команды
│   │   ├── ИИ_История_Windows.bat   # Windows интерфейс
│   │   ├── ИИ_История.bat           # Основной лаунчер
│   │   ├── start_ai.bat             # Быстрый старт
│   │   ├── train_ai.bat             # Обучение
│   │   └── test_ai.bat              # Тестирование
│   ├── training/                    # Обучение моделей
│   │   └── train_model_ru.py        # Обучение русской модели
│   ├── testing/                     # Тестирование
│   │   ├── test_generation.py       # Тест английской модели
│   │   ├── test_generation_ru.py    # Тест русской модели
│   │   ├── test_russian_simple.py   # Простой тест
│   │   └── test_formats.py          # Тест форматов данных
│   └── build/                       # Сборка приложений
│       ├── build_exe.py             # Сборка веб exe
│       ├── build_windows_exe.py     # Сборка Windows exe
│       ├── create_exe.bat           # Batch для веб exe
│       └── create_windows_exe.bat   # Batch для Windows exe
│
├── 📁 docs/                          # Документация
│   ├── guides/                      # Руководства
│   │   ├── README.md                # Основная информация
│   │   ├── INSTALL.md               # Установка
│   │   ├── QUICK_START.md           # Быстрый старт
│   │   ├── TRAINING_GUIDE.md        # Обучение моделей
│   │   ├── DATA_FORMATS.md          # Форматы данных
│   │   ├── MODEL_INTERACTION_GUIDE.md # Взаимодействие с моделями
│   │   ├── RUSSIAN_MODEL_GUIDE.md   # Русская модель
│   │   ├── WINDOWS_INTERFACE_GUIDE.md # Windows интерфейс
│   │   ├── WEB_INTERFACE_GUIDE.md   # Веб-интерфейс
│   │   ├── JUPYTER_GUIDE.md         # Jupyter Notebook
│   │   ├── MAKEFILE_GUIDE.md        # Makefile
│   │   ├── MAKEFILE_WINDOWS_GUIDE.md # Makefile для Windows
│   │   ├── ENCODING_FIX.md          # Исправление кодировки
│   │   ├── UTF8_SOLUTION.md         # UTF-8 решение
│   │   ├── PDF_ANALYSIS_REPORT.md   # Анализ PDF
│   │   ├── FINAL_GUIDE.md           # Финальное руководство
│   │   ├── FINAL_WEB_GUIDE.md       # Финальное веб руководство
│   │   ├── SUPPORTED_FORMATS.md     # Поддерживаемые форматы
│   │   └── README_Windows_EXE.md    # Windows exe руководство
│   └── examples/                    # Примеры
│       ├── demo.py                  # Демонстрация
│       ├── quick_start.py           # Быстрый старт
│       └── launcher.py              # Лаунчер
│
├── 📁 data/                          # Данные
│   ├── raw/                         # Исходные данные
│   │   ├── sample_history_data.json # Тестовые данные
│   │   ├── Uchebnoe_posobie_Istoria_2017.pdf # Учебник
│   │   └── Учебник_История_России_образование.x90326.pdf # Учебник
│   └── processed/                   # Обработанные данные
│       └── pdf_history_data.json    # Данные из PDF
│
├── 📁 models/                        # Обученные модели
│   └── history_ai_trained/          # Обученная английская модель
│       ├── config.json              # Конфигурация
│       ├── model.safetensors        # Веса модели
│       ├── tokenizer.json           # Токенизатор
│       └── checkpoint-*/            # Чекпоинты
│
├── 📁 notebooks/                     # Jupyter notebooks
│   └── getting_started.ipynb        # Начало работы
│
├── 📁 configs/                       # Конфигурации
├── 📁 logs/                          # Логи обучения
├── 📁 venv/                          # Виртуальное окружение
│
├── 📄 README.md                      # Главный README
├── 📄 PROJECT_STRUCTURE.md           # Этот файл
├── 📄 Makefile                       # Автоматизация
├── 📄 requirements.txt               # Зависимости
├── 📄 setup_ai.py                    # Настройка проекта
│
├── 🖥️ ИИ_История_Windows.exe         # Windows приложение
├── 📄 ИИ_История.spec                # PyInstaller spec
├── 📄 web_history.json               # История веб-интерфейса
└── 📄 windows_history.json           # История Windows интерфейса
```

## 🚀 **Как использовать новую структуру**

### **1. Главный лаунчер (рекомендуется)**
```bash
scripts\launchers\Главный_лаунчер.bat
```

### **2. Прямые команды**
```bash
# Windows интерфейс
python interfaces\windows\windows_interface.py

# Веб-интерфейс
python interfaces\web\web_interface.py

# Обучение
python scripts\training\train_model_ru.py

# Тестирование
python scripts\testing\test_generation_ru.py
```

### **3. Makefile команды**
```bash
make help          # Список команд
make windows       # Windows интерфейс
make web           # Веб-интерфейс
make train-ru      # Обучение русской модели
make test-ru       # Тест русской модели
make build-windows # Создание Windows exe
```

## 🎯 **Преимущества новой структуры**

### **📁 Организация:**
- ✅ Логичное разделение по функциям
- ✅ Легко найти нужный файл
- ✅ Понятная иерархия

### **🚀 Удобство:**
- ✅ Главный лаунчер для всех функций
- ✅ Короткие команды через Makefile
- ✅ Прямой доступ к интерфейсам

### **🔧 Разработка:**
- ✅ Отдельные папки для скриптов
- ✅ Организованная документация
- ✅ Примеры в отдельной папке

### **📚 Документация:**
- ✅ Все руководства в одном месте
- ✅ Примеры использования
- ✅ Техническая документация

## 🎉 **Готовые приложения**

### **🖥️ Windows приложение**
- **Файл:** `ИИ_История_Windows.exe`
- **Запуск:** Двойной клик
- **Особенности:** Нативный интерфейс, офлайн работа

### **🌐 Веб-приложение**
- **Запуск:** `make web` или `python interfaces\web\web_interface.py`
- **Адрес:** http://localhost:5000
- **Особенности:** Кроссплатформенность

## 💡 **Советы по навигации**

### **Для пользователей:**
1. Начните с `scripts\launchers\Главный_лаунчер.bat`
2. Используйте Windows интерфейс для ежедневной работы
3. Читайте документацию в `docs\guides\`

### **Для разработчиков:**
1. Исходный код в `src\`
2. Скрипты в `scripts\`
3. Тестирование в `scripts\testing\`

### **Для документации:**
1. Основная информация в `README.md`
2. Руководства в `docs\guides\`
3. Примеры в `docs\examples\`

## 🎯 **Все способы запуска**

| Способ | Команда | Описание |
|--------|---------|----------|
| **Главный лаунчер** | `scripts\launchers\Главный_лаунчер.bat` | Интерактивное меню |
| **Windows интерфейс** | `ИИ_История_Windows.exe` | Нативное приложение |
| **Веб-интерфейс** | `make web` | Через браузер |
| **Командная строка** | `python scripts\testing\test_generation_ru.py` | Для разработчиков |
| **Makefile** | `make help` | Список всех команд |

---

**🏛️ Теперь проект имеет логичную и понятную структуру!**
