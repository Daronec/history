# 🔧 Решение проблем с UTF-8 кодировкой

## ✅ **Проблема решена!**

### 🐛 **Что было:**
- Batch файлы с русским текстом отображали нечитаемые символы
- Проблема в кодировке UTF-8 в Windows PowerShell/CMD

### 🔧 **Решения:**

## 1. **Английская версия (работает всегда):**
```bash
.\train.bat help
.\train.bat status
.\train.bat sample
```

## 2. **Русская версия с UTF-8 (для PowerShell):**
```bash
# Установить кодировку UTF-8
chcp 65001

# Затем использовать русскую версию
.\train_ru.bat help
.\train_ru.bat status
```

## 3. **Настройка PowerShell для UTF-8:**
```powershell
# В начале сессии PowerShell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# Или добавить в профиль PowerShell
echo '[Console]::OutputEncoding = [System.Text.Encoding]::UTF8' >> $PROFILE
```

## 4. **Использование Makefile (без проблем с кодировкой):**
```bash
make help
make status
make train-sample
```

## 📋 **Доступные варианты:**

| Файл | Язык | Кодировка | Статус |
|------|------|-----------|--------|
| `train.bat` | English | ASCII | ✅ Работает |
| `train_ru.bat` | Русский | UTF-8 | ✅ Работает с chcp 65001 |
| `Makefile` | Русский | UTF-8 | ✅ Работает |

## 🚀 **Рекомендации:**

### **Для быстрого использования:**
```bash
# Английская версия (всегда работает)
.\train.bat help
.\train.bat sample
.\train.bat test
```

### **Для русскоязычного интерфейса:**
```bash
# Настроить кодировку
chcp 65001

# Использовать русскую версию
.\train_ru.bat help
.\train_ru.bat sample
.\train_ru.bat test
```

### **Для разработчиков:**
```bash
# Makefile (кроссплатформенный)
make help
make train-sample
make test-generation
```

## 💡 **Советы:**

1. **Для Windows:** Используйте `train.bat` (английский) - он работает всегда
2. **Для UTF-8:** Используйте `chcp 65001` перед запуском русских скриптов
3. **Для разработки:** Используйте `make` - он работает на всех платформах

## 🎉 **Результат:**

Теперь у вас есть **три рабочих способа** управления проектом:

- **`.\train.bat`** - английский, работает всегда
- **`.\train_ru.bat`** - русский, с настройкой UTF-8
- **`make`** - кроссплатформенный

**Проблема с кодировкой полностью решена! 🎉**
