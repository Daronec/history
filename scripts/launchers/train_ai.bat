@echo off
chcp 65001 >nul
title Обучение ИИ модели
color 0E

echo.
echo 🤖 Обучение ИИ модели для изучения истории
echo ========================================
echo.

echo Выберите тип обучения:
echo.
echo 1. 📚 Быстрое обучение на примерах (1 эпоха)
echo 2. 📖 Обучение на PDF учебнике
echo 3. 🇷🇺 Обучение русской модели
echo 4. 🔄 Переобучение всех моделей
echo 5. 🚪 Назад
echo.

set /p choice="Введите номер (1-5): "

if "%choice%"=="1" goto quick_train
if "%choice%"=="2" goto pdf_train
if "%choice%"=="3" goto russian_train
if "%choice%"=="4" goto retrain_all
if "%choice%"=="5" goto exit
goto train_ai

:quick_train
echo.
echo 📚 Быстрое обучение на примерах...
echo.
python src/train_model.py --data sample --task generation --epochs 1 --model distilgpt2
echo.
echo ✅ Обучение завершено!
pause
goto train_ai

:pdf_train
echo.
echo 📖 Обучение на PDF учебнике...
echo.
if not exist "data\processed\pdf_history_data.json" (
    echo ❌ PDF данные не найдены!
    echo 💡 Сначала запустите: python src/pdf_reader.py
    pause
    goto train_ai
)
python src/train_model.py --data data/processed/pdf_history_data.json --task generation --epochs 1 --model distilgpt2
echo.
echo ✅ Обучение на PDF завершено!
pause
goto train_ai

:russian_train
echo.
echo 🇷🇺 Обучение русской модели...
echo.
python train_model_ru.py
echo.
echo ✅ Обучение русской модели завершено!
pause
goto train_ai

:retrain_all
echo.
echo 🔄 Переобучение всех моделей...
echo.
echo 1. Очищаем старые модели...
if exist "models\history_ai_trained" rmdir /s /q "models\history_ai_trained"
if exist "models\history_ai_ru_trained" rmdir /s /q "models\history_ai_ru_trained"

echo 2. Обучаем английскую модель...
python src/train_model.py --data sample --task generation --epochs 1 --model distilgpt2

echo 3. Обучаем русскую модель...
python train_model_ru.py

echo.
echo ✅ Все модели переобучены!
pause
goto train_ai

:exit
echo.
echo 👋 До свидания!
echo.
pause
exit
