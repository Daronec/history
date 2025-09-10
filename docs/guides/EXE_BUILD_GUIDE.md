# 🔧 Руководство по сборке EXE файлов

## 📦 Обзор

Это руководство покажет, как собрать исполняемые файлы (.exe) для проекта ИИ-История.

## 🎯 Типы EXE файлов

### 1. **Полная версия** - `ИИ_История_Windows.exe`
- Включает все ML библиотеки
- Полная функциональность
- Размер: ~2-3 ГБ

### 2. **Веб-версия** - `ИИ_История_Веб.exe`
- Веб-интерфейс в exe
- Запускает локальный сервер
- Размер: ~2-3 ГБ

### 3. **Минимальная версия** - `ИИ_История_Мини.exe`
- Только управление файлами
- Без ML библиотек
- Размер: ~50-100 МБ

## 🚀 Быстрая сборка

### **Способ 1: Через batch файлы**

```bash
# Полная версия
scripts\build\create_windows_exe.bat

# Веб-версия
scripts\build\create_exe.bat

# Минимальная версия
scripts\build\create_minimal_exe.bat
```

### **Способ 2: Через Makefile**

```bash
# Полная версия
make build

# Веб-версия
make build-web
```

## 📋 Требования

### **Системные требования:**
- Windows 10/11
- Python 3.8+
- 8+ ГБ RAM
- 10+ ГБ свободного места

### **Python библиотеки:**
```bash
pip install pyinstaller
pip install -r requirements.txt
```

## 🔧 Детальная сборка

### **1. Подготовка**

```bash
# Активируйте виртуальное окружение
venv\Scripts\activate

# Установите PyInstaller
pip install pyinstaller

# Проверьте зависимости
pip list | findstr pyinstaller
```

### **2. Сборка полной версии**

```bash
pyinstaller --onefile ^
    --windowed ^
    --name "ИИ_История_Windows" ^
    --icon=icon.ico ^
    --add-data "models;models" ^
    --add-data "data;data" ^
    --add-data "configs;configs" ^
    --hidden-import=torch ^
    --hidden-import=transformers ^
    --hidden-import=tensorflow ^
    --hidden-import=tkinter ^
    --hidden-import=PIL ^
    --hidden-import=pdfplumber ^
    --hidden-import=PyPDF2 ^
    --hidden-import=pymupdf ^
    --hidden-import=docx2txt ^
    --hidden-import=python-docx ^
    interfaces/windows/windows_interface_universal.py
```

### **3. Сборка веб-версии**

```bash
pyinstaller --onefile ^
    --console ^
    --name "ИИ_История_Веб" ^
    --icon=icon.ico ^
    --add-data "models;models" ^
    --add-data "data;data" ^
    --add-data "configs;configs" ^
    --add-data "interfaces/web/templates;templates" ^
    --hidden-import=flask ^
    --hidden-import=torch ^
    --hidden-import=transformers ^
    --hidden-import=tensorflow ^
    --hidden-import=werkzeug ^
    --hidden-import=jinja2 ^
    interfaces/web/web_interface.py
```

### **4. Сборка минимальной версии**

```bash
pyinstaller --onefile ^
    --windowed ^
    --name "ИИ_История_Мини" ^
    --icon=icon.ico ^
    --add-data "data;data" ^
    --add-data "configs;configs" ^
    --exclude-module=torch ^
    --exclude-module=transformers ^
    --exclude-module=tensorflow ^
    --exclude-module=numpy ^
    --exclude-module=pandas ^
    --exclude-module=matplotlib ^
    --exclude-module=seaborn ^
    --exclude-module=jupyter ^
    --exclude-module=flask ^
    --exclude-module=streamlit ^
    --hidden-import=tkinter ^
    --hidden-import=PIL ^
    --hidden-import=pdfplumber ^
    --hidden-import=PyPDF2 ^
    --hidden-import=pymupdf ^
    --hidden-import=docx2txt ^
    --hidden-import=python-docx ^
    interfaces/windows/windows_interface_universal.py
```

## ⚙️ Параметры PyInstaller

### **Основные параметры:**

- `--onefile` - создать один exe файл
- `--windowed` - без консоли (для GUI)
- `--console` - с консолью (для веб-версии)
- `--name` - имя exe файла
- `--icon` - иконка файла
- `--add-data` - добавить файлы/папки
- `--hidden-import` - скрытые импорты
- `--exclude-module` - исключить модули

### **Оптимизация размера:**

```bash
# Исключить ненужные модули
--exclude-module=matplotlib
--exclude-module=seaborn
--exclude-module=jupyter
--exclude-module=notebook

# Исключить тесты
--exclude-module=test
--exclude-module=tests
--exclude-module=pytest
```

## 🎯 Специальные настройки

### **1. Иконка приложения**

Создайте файл `icon.ico` в корне проекта:
- Размер: 256x256 пикселей
- Формат: ICO
- Стиль: в соответствии с тематикой

### **2. Версия приложения**

Создайте файл `version.txt`:
```
1.0.0
ИИ для изучения истории
```

### **3. Манифест**

Создайте файл `app.manifest`:
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity version="1.0.0.0" processorArchitecture="*" name="AI_History" type="win32"/>
  <description>ИИ для изучения истории</description>
  <dependency>
    <dependentAssembly>
      <assemblyIdentity type="win32" name="Microsoft.Windows.Common-Controls" version="6.0.0.0" processorArchitecture="*" publicKeyToken="6595b64144ccf1df" language="*"/>
    </dependentAssembly>
  </dependency>
</assembly>
```

## 🚨 Решение проблем

### **Проблема: "ModuleNotFoundError"**

**Решение:**
```bash
# Добавьте скрытые импорты
--hidden-import=torch
--hidden-import=transformers
--hidden-import=tensorflow
```

### **Проблема: "FileNotFoundError"**

**Решение:**
```bash
# Добавьте необходимые файлы
--add-data "models;models"
--add-data "data;data"
--add-data "configs;configs"
```

### **Проблема: "EXE слишком большой"**

**Решение:**
```bash
# Исключите ненужные модули
--exclude-module=matplotlib
--exclude-module=seaborn
--exclude-module=jupyter
```

### **Проблема: "EXE не запускается"**

**Решение:**
1. Проверьте зависимости
2. Запустите с консолью: `--console`
3. Проверьте логи в папке `logs/`

## 📊 Оптимизация

### **Уменьшение размера:**

1. **Исключите ненужные модули:**
```bash
--exclude-module=matplotlib
--exclude-module=seaborn
--exclude-module=jupyter
--exclude-module=notebook
```

2. **Используйте UPX сжатие:**
```bash
# Установите UPX
# Скачайте с https://upx.github.io/
# Добавьте в PATH

# Используйте сжатие
pyinstaller --onefile --upx-dir=C:\upx ...
```

3. **Оптимизируйте импорты:**
```python
# В коде используйте условные импорты
try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
```

## 🎯 Готовые команды

### **Сборка всех версий:**

```bash
# Создайте batch файл build_all.bat
@echo off
echo Сборка всех версий ИИ-История...

echo 1. Полная версия...
call scripts\build\create_windows_exe.bat

echo 2. Веб-версия...
call scripts\build\create_exe.bat

echo 3. Минимальная версия...
call scripts\build\create_minimal_exe.bat

echo ✅ Все версии собраны!
pause
```

## 📁 Структура после сборки

```
dist/
├── ИИ_История_Windows.exe      # Полная версия
├── ИИ_История_Веб.exe          # Веб-версия
└── ИИ_История_Мини.exe         # Минимальная версия

build/                          # Временные файлы сборки
spec/                           # Файлы спецификации PyInstaller
```

## 🎉 Готово!

Теперь у вас есть все необходимые инструменты для сборки EXE файлов:

- ✅ **Batch файлы** для быстрой сборки
- ✅ **Подробные инструкции** по настройке
- ✅ **Решение проблем** и оптимизация
- ✅ **Готовые команды** для всех версий

**Удачи в сборке EXE файлов! 🔧📦**
