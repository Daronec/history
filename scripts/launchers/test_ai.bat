@echo off
chcp 65001 >nul
title Тестирование ИИ модели
color 0D

echo.
echo 🧪 Тестирование ИИ модели
echo ========================================
echo.

echo Выберите тип тестирования:
echo.
echo 1. 🇷🇺 Тест русской модели (рекомендуется)
echo 2. 🇺🇸 Тест английской модели
echo 3. 🎮 Интерактивный режим (русский)
echo 4. 🎮 Интерактивный режим (английский)
echo 5. 📊 Сравнение моделей
echo 6. 🚪 Назад
echo.

set /p choice="Введите номер (1-6): "

if "%choice%"=="1" goto test_russian
if "%choice%"=="2" goto test_english
if "%choice%"=="3" goto interactive_russian
if "%choice%"=="4" goto interactive_english
if "%choice%"=="5" goto compare_models
if "%choice%"=="6" goto exit
goto test_ai

:test_russian
echo.
echo 🇷🇺 Тестируем русскую модель...
echo.
python test_russian_simple.py
pause
goto test_ai

:test_english
echo.
echo 🇺🇸 Тестируем английскую модель...
echo.
python test_generation.py
pause
goto test_ai

:interactive_russian
echo.
echo 🎮 Интерактивный режим (русский)
echo.
echo 💡 Примеры промптов:
echo    "В 1812 году произошло"
echo    "Петр I известен тем, что"
echo    "Сталин родился в"
echo    "Революция 1917 года привела к"
echo.
echo Введите 'выход' для завершения
echo.
python test_russian_simple.py
pause
goto test_ai

:interactive_english
echo.
echo 🎮 Интерактивный режим (английский)
echo.
echo 💡 Example prompts:
echo    "In 1812, Napoleon"
echo    "Peter the Great was known for"
echo    "The Russian Revolution"
echo.
echo Type 'exit' to finish
echo.
python test_generation.py
pause
goto test_ai

:compare_models
echo.
echo 📊 Сравнение моделей...
echo.
echo Тестируем одинаковые промпты на обеих моделях:
echo.

echo Промпт: "В 1812 году произошло"
echo.
echo 🇷🇺 Русская модель:
python -c "import sys; sys.path.append('src'); from models.history_ai_ru import HistoryAIModelRU; model = HistoryAIModelRU(); model.load_model('generation'); print(model.generate_text('В 1812 году произошло', max_length=50))"
echo.
echo 🇺🇸 Английская модель:
python -c "import sys; sys.path.append('src'); from models.history_ai import HistoryAIModel; model = HistoryAIModel(); model.load_trained_model('./models/history_ai_trained'); print(model.generate_text('В 1812 году произошло', max_length=50))"
echo.
pause
goto test_ai

:exit
echo.
echo 👋 До свидания!
echo.
pause
exit
