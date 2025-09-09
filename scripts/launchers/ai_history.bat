@echo off
chcp 65001 >nul
title ИИ для изучения истории
color 0A

echo.
echo ========================================
echo    🏛️ ИИ для изучения истории
echo ========================================
echo.

:menu
echo Выберите действие:
echo.
echo 1. 🌐 Веб-интерфейс (рекомендуется)
echo 2. 🤖 Тест русской модели
echo 3. 🇺🇸 Тест английской модели
echo 4. 📚 Обучение на примерах
echo 5. 📖 Обучение на PDF данных
echo 6. 🧹 Очистка моделей
echo 7. 📊 Статус проекта
echo 8. ❓ Справка
echo 9. 🚪 Выход
echo.

set /p choice="Введите номер (1-9): "

if "%choice%"=="1" goto web
if "%choice%"=="2" goto test_ru
if "%choice%"=="3" goto test_en
if "%choice%"=="4" goto train_sample
if "%choice%"=="5" goto train_pdf
if "%choice%"=="6" goto clean
if "%choice%"=="7" goto status
if "%choice%"=="8" goto help
if "%choice%"=="9" goto exit
goto menu

:web
echo.
echo 🌐 Запускаем веб-интерфейс...
echo 📱 Откройте в браузере: http://localhost:5000
echo 🛑 Для остановки нажмите Ctrl+C
echo.
python web_interface.py
pause
goto menu

:test_ru
echo.
echo 🇷🇺 Тестируем русскую модель...
echo.
python test_russian_simple.py
pause
goto menu

:test_en
echo.
echo 🇺🇸 Тестируем английскую модель...
echo.
python test_generation.py
pause
goto menu

:train_sample
echo.
echo 📚 Обучаем модель на примерах...
echo.
python src/train_model.py --data sample --task generation --epochs 1 --model distilgpt2
pause
goto menu

:train_pdf
echo.
echo 📖 Обучаем модель на PDF данных...
echo.
python src/train_model.py --data data/processed/pdf_history_data.json --task generation --epochs 1 --model distilgpt2
pause
goto menu

:clean
echo.
echo 🧹 Очищаем модели...
echo.
if exist "models\history_ai_trained" rmdir /s /q "models\history_ai_trained"
if exist "models\history_ai_ru_trained" rmdir /s /q "models\history_ai_ru_trained"
if exist "__pycache__" rmdir /s /q "__pycache__"
if exist "src\__pycache__" rmdir /s /q "src\__pycache__"
echo ✅ Очистка завершена
pause
goto menu

:status
echo.
echo 📊 Статус проекта:
echo ========================================
if exist "venv" (
    echo Виртуальное окружение: ✅ Установлено
) else (
    echo Виртуальное окружение: ❌ Не установлено
)

if exist "models\history_ai_trained" (
    echo Английская модель: ✅ Есть
) else (
    echo Английская модель: ❌ Нет
)

if exist "data\processed\pdf_history_data.json" (
    echo PDF данные: ✅ Есть
) else (
    echo PDF данные: ❌ Нет
)

if exist "data\raw\sample_history_data.json" (
    echo Примеры данных: ✅ Есть
) else (
    echo Примеры данных: ❌ Нет
)
echo.
pause
goto menu

:help
echo.
echo ❓ Справка по ИИ для изучения истории
echo ========================================
echo.
echo 🌐 Веб-интерфейс - самый удобный способ работы
echo    Откройте http://localhost:5000 в браузере
echo.
echo 🤖 Тест моделей - проверка работы ИИ
echo    Русская модель лучше для русских промптов
echo    Английская модель для английских промптов
echo.
echo 📚 Обучение - улучшение качества ответов
echo    Примеры: быстрая проверка
echo    PDF данные: обучение на учебнике
echo.
echo 💡 Примеры промптов:
echo    "В 1812 году произошло"
echo    "Петр I известен тем, что"
echo    "Сталин родился в"
echo    "Революция 1917 года привела к"
echo.
pause
goto menu

:exit
echo.
echo 👋 До свидания!
echo.
pause
exit
