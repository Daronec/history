@echo off
chcp 65001 >nul
REM Batch файл для обучения ИИ модели на Windows
REM Использование: train_ru.bat <команда>

setlocal enabledelayedexpansion

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="sample" goto train_sample
if "%1"=="pdf" goto train_pdf
if "%1"=="csv" goto train_csv
if "%1"=="txt" goto train_txt
if "%1"=="custom" goto train_custom
if "%1"=="test" goto test_generation
if "%1"=="demo" goto demo
if "%1"=="status" goto status
if "%1"=="clean" goto clean
goto help

:help
echo ========================================
echo    ИИ проект для изучения истории
echo ========================================
echo.
echo Доступные команды:
echo   train_ru.bat sample     - Обучить на примерах (1 эпоха)
echo   train_ru.bat pdf        - Обучить на PDF данных
echo   train_ru.bat csv        - Обучить на CSV данных
echo   train_ru.bat txt        - Обучить на TXT данных
echo   train_ru.bat custom     - Обучить на пользовательских данных
echo   train_ru.bat test       - Тест генерации
echo   train_ru.bat demo       - Демонстрация
echo   train_ru.bat status     - Статус проекта
echo   train_ru.bat clean      - Очистка
echo.
goto end

:train_sample
echo [ОБУЧЕНИЕ] Обучаем модель на примерах...
python src/train_model.py --data sample --task generation --epochs 1 --model distilgpt2
goto end

:train_pdf
echo [ОБУЧЕНИЕ] Обучаем модель на PDF данных...
python src/train_model.py --data data/processed/pdf_history_data.json --task generation --epochs 1 --model distilgpt2
goto end

:train_csv
echo [ОБУЧЕНИЕ] Обучаем модель на CSV данных...
python src/train_model.py --data data/raw/example_history.csv --task generation --epochs 1 --model distilgpt2
goto end

:train_txt
echo [ОБУЧЕНИЕ] Обучаем модель на TXT данных...
python src/train_model.py --data data/raw/example_history.txt --task generation --epochs 1 --model distilgpt2
goto end

:train_custom
echo [ОБУЧЕНИЕ] Обучаем модель на пользовательских данных...
if "%2"=="" (
    echo ОШИБКА: Укажите путь к файлу данных
    echo Пример: train_ru.bat custom data/raw/my_data.json
    goto end
)
python src/train_model.py --data %2 --task generation --epochs 1 --model distilgpt2
goto end

:test_generation
echo [ТЕСТ] Тестируем генерацию текста...
python test_generation.py
goto end

:demo
echo [ДЕМО] Запускаем демонстрацию...
python demo.py
goto end

:status
echo ========================================
echo           СТАТУС ПРОЕКТА
echo ========================================
if exist "venv" (
    echo Виртуальное окружение: [OK] Установлено
) else (
    echo Виртуальное окружение: [NO] Не установлено
)

if exist "models\history_ai_trained" (
    echo Обученная модель: [OK] Есть
) else (
    echo Обученная модель: [NO] Нет
)

if exist "data\processed\pdf_history_data.json" (
    echo PDF данные: [OK] Есть
) else (
    echo PDF данные: [NO] Нет
)

if exist "data\raw\sample_history_data.json" (
    echo Примеры данных: [OK] Есть
) else (
    echo Примеры данных: [NO] Нет
)
goto end

:clean
echo [ОЧИСТКА] Очищаем временные файлы...
if exist "__pycache__" rmdir /s /q "__pycache__"
if exist "src\__pycache__" rmdir /s /q "src\__pycache__"
if exist "src\models\__pycache__" rmdir /s /q "src\models\__pycache__"
if exist "models\history_ai_trained" rmdir /s /q "models\history_ai_trained"
echo [OK] Очистка завершена
goto end

:end
