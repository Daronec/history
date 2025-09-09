@echo off
chcp 65001 >nul
title 🏛️ ИИ для изучения истории
color 0F

echo.
echo ████████████████████████████████████████████████████████████
echo ██                                                        ██
echo ██  🏛️  ИИ для изучения истории  🏛️                    ██
echo ██                                                        ██
echo ██  Интерактивная система для изучения истории           ██
echo ██  с помощью искусственного интеллекта                  ██
echo ██                                                        ██
echo ████████████████████████████████████████████████████████████
echo.

:main_menu
echo.
echo 🎯 ГЛАВНОЕ МЕНЮ
echo ========================================
echo.
echo 1. 🚀 Быстрый старт (веб-интерфейс)
echo 2. 🤖 Обучение модели
echo 3. 🧪 Тестирование модели
echo 4. 📊 Статус проекта
echo 5. 🛠️ Настройки
echo 6. ❓ Справка
echo 7. 🚪 Выход
echo.

set /p choice="Введите номер (1-7): "

if "%choice%"=="1" goto quick_start
if "%choice%"=="2" goto training_menu
if "%choice%"=="3" goto testing_menu
if "%choice%"=="4" goto status
if "%choice%"=="5" goto settings
if "%choice%"=="6" goto help
if "%choice%"=="7" goto exit
goto main_menu

:quick_start
echo.
echo 🚀 Быстрый старт
echo ========================================
echo.
echo 🌐 Запускаем веб-интерфейс...
echo 📱 Откройте в браузере: http://localhost:5000
echo.
echo 💡 Советы для начала:
echo    - Введите промпт на русском языке
echo    - Выберите "Русский" в настройках
echo    - Попробуйте: "В 1812 году произошло"
echo.
echo 🛑 Для остановки нажмите Ctrl+C
echo.
python web_interface.py
echo.
echo 👋 Веб-интерфейс остановлен
pause
goto main_menu

:training_menu
echo.
echo 🤖 Обучение модели
echo ========================================
echo.
echo Выберите тип обучения:
echo.
echo 1. 📚 Быстрое обучение на примерах
echo 2. 📖 Обучение на PDF учебнике
echo 3. 🇷🇺 Обучение русской модели
echo 4. 🔄 Переобучение всех моделей
echo 5. ⬅️ Назад
echo.

set /p train_choice="Введите номер (1-5): "

if "%train_choice%"=="1" goto quick_train
if "%train_choice%"=="2" goto pdf_train
if "%train_choice%"=="3" goto russian_train
if "%train_choice%"=="4" goto retrain_all
if "%train_choice%"=="5" goto main_menu
goto training_menu

:quick_train
echo.
echo 📚 Быстрое обучение на примерах...
python src/train_model.py --data sample --task generation --epochs 1 --model distilgpt2
echo ✅ Обучение завершено!
pause
goto training_menu

:pdf_train
echo.
echo 📖 Обучение на PDF учебнике...
if not exist "data\processed\pdf_history_data.json" (
    echo ❌ PDF данные не найдены!
    echo 💡 Сначала запустите: python src/pdf_reader.py
    pause
    goto training_menu
)
python src/train_model.py --data data/processed/pdf_history_data.json --task generation --epochs 1 --model distilgpt2
echo ✅ Обучение на PDF завершено!
pause
goto training_menu

:russian_train
echo.
echo 🇷🇺 Обучение русской модели...
python train_model_ru.py
echo ✅ Обучение русской модели завершено!
pause
goto training_menu

:retrain_all
echo.
echo 🔄 Переобучение всех моделей...
if exist "models\history_ai_trained" rmdir /s /q "models\history_ai_trained"
if exist "models\history_ai_ru_trained" rmdir /s /q "models\history_ai_ru_trained"
python src/train_model.py --data sample --task generation --epochs 1 --model distilgpt2
python train_model_ru.py
echo ✅ Все модели переобучены!
pause
goto training_menu

:testing_menu
echo.
echo 🧪 Тестирование модели
echo ========================================
echo.
echo Выберите тип тестирования:
echo.
echo 1. 🇷🇺 Тест русской модели
echo 2. 🇺🇸 Тест английской модели
echo 3. 🎮 Интерактивный режим
echo 4. 📊 Сравнение моделей
echo 5. ⬅️ Назад
echo.

set /p test_choice="Введите номер (1-5): "

if "%test_choice%"=="1" goto test_russian
if "%test_choice%"=="2" goto test_english
if "%test_choice%"=="3" goto interactive_mode
if "%test_choice%"=="4" goto compare_models
if "%test_choice%"=="5" goto main_menu
goto testing_menu

:test_russian
echo.
echo 🇷🇺 Тестируем русскую модель...
python test_russian_simple.py
pause
goto testing_menu

:test_english
echo.
echo 🇺🇸 Тестируем английскую модель...
python test_generation.py
pause
goto testing_menu

:interactive_mode
echo.
echo 🎮 Интерактивный режим
echo.
echo Выберите язык:
echo 1. 🇷🇺 Русский
echo 2. 🇺🇸 Английский
echo.

set /p lang_choice="Введите номер (1-2): "

if "%lang_choice%"=="1" (
    echo.
    echo 💡 Примеры промптов:
    echo    "В 1812 году произошло"
    echo    "Петр I известен тем, что"
    echo    "Сталин родился в"
    echo.
    python test_russian_simple.py
) else if "%lang_choice%"=="2" (
    echo.
    echo 💡 Example prompts:
    echo    "In 1812, Napoleon"
    echo    "Peter the Great was known for"
    echo.
    python test_generation.py
)
pause
goto testing_menu

:compare_models
echo.
echo 📊 Сравнение моделей...
echo.
echo Тестируем промпт: "В 1812 году произошло"
echo.
echo 🇷🇺 Русская модель:
python -c "import sys; sys.path.append('src'); from models.history_ai_ru import HistoryAIModelRU; model = HistoryAIModelRU(); model.load_model('generation'); print(model.generate_text('В 1812 году произошло', max_length=50))"
echo.
echo 🇺🇸 Английская модель:
python -c "import sys; sys.path.append('src'); from models.history_ai import HistoryAIModel; model = HistoryAIModel(); model.load_trained_model('./models/history_ai_trained'); print(model.generate_text('В 1812 году произошло', max_length=50))"
echo.
pause
goto testing_menu

:status
echo.
echo 📊 Статус проекта
echo ========================================
echo.
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
goto main_menu

:settings
echo.
echo 🛠️ Настройки
echo ========================================
echo.
echo 1. 🧹 Очистка моделей
echo 2. 📁 Открыть папку проекта
echo 3. 🔧 Установить зависимости
echo 4. ⬅️ Назад
echo.

set /p settings_choice="Введите номер (1-4): "

if "%settings_choice%"=="1" goto clean_models
if "%settings_choice%"=="2" goto open_folder
if "%settings_choice%"=="3" goto install_deps
if "%settings_choice%"=="4" goto main_menu
goto settings

:clean_models
echo.
echo 🧹 Очищаем модели...
if exist "models\history_ai_trained" rmdir /s /q "models\history_ai_trained"
if exist "models\history_ai_ru_trained" rmdir /s /q "models\history_ai_ru_trained"
if exist "__pycache__" rmdir /s /q "__pycache__"
if exist "src\__pycache__" rmdir /s /q "src\__pycache__"
echo ✅ Очистка завершена
pause
goto settings

:open_folder
echo.
echo 📁 Открываем папку проекта...
explorer .
pause
goto settings

:install_deps
echo.
echo 🔧 Устанавливаем зависимости...
pip install -r requirements.txt
echo ✅ Зависимости установлены
pause
goto settings

:help
echo.
echo ❓ Справка
echo ========================================
echo.
echo 🎯 ОСНОВНЫЕ ВОЗМОЖНОСТИ:
echo.
echo 🌐 Веб-интерфейс - самый удобный способ работы
echo    • Откройте http://localhost:5000 в браузере
echo    • Введите промпт и получите ответ
echo    • Настройте параметры генерации
echo.
echo 🤖 Обучение модели - улучшение качества ответов
echo    • Примеры: быстрая проверка работы
echo    • PDF данные: обучение на учебнике
echo    • Русская модель: для русских промптов
echo.
echo 🧪 Тестирование - проверка работы ИИ
echo    • Русская модель лучше для русских промптов
echo    • Английская модель для английских промптов
echo    • Сравнение результатов
echo.
echo 💡 ПРИМЕРЫ ПРОМПТОВ:
echo    "В 1812 году произошло"
echo    "Петр I известен тем, что"
echo    "Сталин родился в"
echo    "Революция 1917 года привела к"
echo.
echo 🚨 РЕШЕНИЕ ПРОБЛЕМ:
echo    • Если модели не загружаются - обучите их
echo    • Если ответы на английском - используйте русскую модель
echo    • Если веб-интерфейс не открывается - проверьте порт 5000
echo.
pause
goto main_menu

:exit
echo.
echo 👋 Спасибо за использование ИИ для изучения истории!
echo.
echo 🏛️ Удачи в изучении истории! 🏛️
echo.
pause
exit
