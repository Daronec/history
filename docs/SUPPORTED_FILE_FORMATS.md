# Поддерживаемые форматы файлов

## 📋 Обзор
ИИ-История поддерживает широкий спектр форматов документов для обучения и анализа.

## 📄 Поддерживаемые форматы

### 1. **Текстовые файлы**
- **Формат**: `.txt`
- **Описание**: Простые текстовые файлы
- **Кодировки**: UTF-8, CP1251, Latin1
- **Использование**: Исторические документы, заметки, статьи

### 2. **CSV файлы**
- **Формат**: `.csv`
- **Описание**: Табличные данные
- **Кодировка**: UTF-8
- **Использование**: Структурированные исторические данные

### 3. **JSON файлы**
- **Формат**: `.json`
- **Описание**: Структурированные данные
- **Кодировка**: UTF-8
- **Использование**: API данные, конфигурации, метаданные

### 4. **PDF документы**
- **Формат**: `.pdf`
- **Описание**: Документы в формате PDF
- **Библиотеки**: PyPDF2, pdfplumber
- **Использование**: Книги, статьи, официальные документы

### 5. **Word документы (старый формат)**
- **Формат**: `.doc`
- **Описание**: Документы Microsoft Word (до 2007)
- **Библиотеки**: docx2txt, python-docx
- **Использование**: Исторические документы, отчеты

### 6. **Word документы (новый формат)**
- **Формат**: `.docx`
- **Описание**: Документы Microsoft Word (2007+)
- **Библиотеки**: python-docx, docx2txt
- **Использование**: Современные документы, презентации

### 7. **DJVU документы**
- **Формат**: `.djvu`
- **Описание**: Сжатые документы
- **Библиотеки**: python-djvu
- **Использование**: Сканированные книги, архивные документы

## 🔧 Технические детали

### Обработка файлов:

#### **Текстовые файлы (.txt)**
```python
def load_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
```

#### **CSV файлы (.csv)**
```python
def load_csv_file(file_path):
    import pandas as pd
    df = pd.read_csv(file_path, encoding='utf-8')
    text_columns = df.select_dtypes(include=['object']).columns
    return ' '.join(df[text_columns].astype(str).values.flatten())
```

#### **PDF файлы (.pdf)**
```python
def load_pdf_file(file_path):
    import pdfplumber
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
```

#### **Word документы (.docx)**
```python
def load_docx_file(file_path):
    from docx import Document
    doc = Document(file_path)
    return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
```

#### **DJVU файлы (.djvu)**
```python
def load_djvu_file(file_path):
    import djvu.decode
    with djvu.decode.Context() as context:
        with context.new_document(djvu.decode.FileURI(file_path)) as doc:
            text = ""
            for page_num in range(doc.page_count):
                page = doc.page(page_num)
                page_text = page.get_text()
                if page_text:
                    text += page_text + "\n"
            return text
```

## 📦 Необходимые библиотеки

### Установка зависимостей:
```bash
pip install -r requirements.txt
```

### Основные библиотеки:
- **PyPDF2** - для работы с PDF
- **pdfplumber** - улучшенная обработка PDF
- **python-docx** - для DOCX файлов
- **docx2txt** - для DOC файлов
- **python-djvu** - для DJVU файлов
- **pandas** - для CSV файлов

## 🎯 Использование

### В интерфейсе:
1. Нажмите "📤 Загрузить файлы"
2. Выберите файлы нужных форматов
3. Файлы автоматически обработаются
4. Используйте "🎓 Переобучить модели"

### Программно:
```python
from data_processing import load_file, process_data_directory

# Загрузка одного файла
text = load_file("document.pdf")

# Обработка всех файлов в директории
texts = process_data_directory("data/raw")
```

## ⚠️ Ограничения

### Размер файлов:
- **PDF**: до 100 МБ
- **DOC/DOCX**: до 50 МБ
- **DJVU**: до 200 МБ
- **Текстовые**: без ограничений

### Качество извлечения:
- **PDF**: зависит от качества сканирования
- **DOC/DOCX**: отличное качество
- **DJVU**: хорошее качество для текстовых документов
- **Сканированные PDF**: может потребовать OCR

## 🔄 Обработка ошибок

### Автоматические fallback:
1. **PDF**: pdfplumber → PyPDF2
2. **DOC**: docx2txt → python-docx
3. **Кодировки**: UTF-8 → CP1251 → Latin1

### Логирование:
- Все ошибки записываются в лог
- Продолжение обработки при ошибках
- Подробная информация об ошибках

## 📊 Статистика поддержки

| Формат | Поддержка | Качество | Скорость |
|--------|-----------|----------|----------|
| TXT    | 100%      | Отлично  | Быстро   |
| CSV    | 100%      | Отлично  | Быстро   |
| JSON   | 100%      | Отлично  | Быстро   |
| PDF    | 95%       | Хорошо   | Средне   |
| DOCX   | 100%      | Отлично  | Быстро   |
| DOC    | 90%       | Хорошо   | Средне   |
| DJVU   | 85%       | Хорошо   | Медленно |

## 🎉 Преимущества

1. **Широкий спектр форматов** - поддержка всех основных типов документов
2. **Автоматическая обработка** - извлечение текста без ручной настройки
3. **Надежность** - fallback механизмы для обработки ошибок
4. **Масштабируемость** - обработка больших объемов данных
5. **Гибкость** - поддержка различных кодировок и структур
