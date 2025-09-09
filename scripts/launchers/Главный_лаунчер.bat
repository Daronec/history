@echo off
chcp 65001 >nul
title 🏛️ ИИ для изучения истории - Главный лаунчер
color 0B

:MAIN_MENU
cls
echo.
echo ████████████████████████████████████████████████████████████
echo ██                                                        ██
echo ██  🏛️  ИИ для изучения истории - Главный лаунчер  🏛️  ██
echo ██                                                        ██
echo ████████████████████████████████████████████████████████████
echo.
echo 📁 Структура проекта:
echo    📁 src/           - Исходный код
echo    📁 interfaces/    - Пользовательские интерфейсы
echo    📁 scripts/       - Скрипты и утилиты
echo    📁 docs/          - Документация
echo    📁 data/          - Данные
echo    📁 models/        - Обученные модели
echo.
echo 🚀 Выберите действие:
echo.
echo 1️⃣  🖥️  Windows интерфейс (рекомендуется)
echo 2️⃣  🌐  Веб-интерфейс
echo 3️⃣  📝  Командная строка
echo 4️⃣  🎓  Обучение моделей
echo 5️⃣  🧪  Тестирование
echo 6️⃣  🔨  Сборка приложений
echo 7️⃣  📚  Документация
echo 8️⃣  ⚙️  Настройки
echo 9️⃣  ❓  Помощь
echo 🔟  🚀  Быстрое обучение русской модели
echo 0️⃣  🚪  Выход
echo.
set /p choice="Введите номер (0-9, 10): "

if "%choice%"=="1" goto WINDOWS_INTERFACE
if "%choice%"=="2" goto WEB_INTERFACE
if "%choice%"=="3" goto COMMAND_LINE
if "%choice%"=="4" goto TRAINING
if "%choice%"=="5" goto TESTING
if "%choice%"=="6" goto BUILD
if "%choice%"=="7" goto DOCUMENTATION
if "%choice%"=="8" goto SETTINGS
if "%choice%"=="9" goto HELP
if "%choice%"=="10" goto QUICK_TRAIN_RU
if "%choice%"=="0" goto EXIT
goto INVALID

:WINDOWS_INTERFACE
cls
echo.
echo 🖥️ Запуск Windows интерфейса...
echo.
if exist "..\..\ИИ_История_Windows.exe" (
    echo ✅ Найден exe файл, запускаем...
    start "" "..\..\ИИ_История_Windows.exe"
) else (
    echo 🔄 Запускаем через Python...
    python "..\..\interfaces\windows\windows_interface.py"
)
echo.
pause
goto MAIN_MENU

:WEB_INTERFACE
cls
echo.
echo 🌐 Запуск веб-интерфейса...
echo.
echo 📡 Запускаем сервер на http://localhost:5000
echo 🌐 Откроется в браузере автоматически
echo.
python "..\..\interfaces\web\web_interface.py"
echo.
pause
goto MAIN_MENU

:COMMAND_LINE
cls
echo.
echo 📝 Командная строка для работы с ИИ
echo.
echo 🚀 Выберите модель:
echo 1️⃣  🇷🇺 Русская модель
echo 2️⃣  🇺🇸 Английская модель
echo 3️⃣  🔙 Назад
echo.
set /p model_choice="Введите номер (1-3): "

if "%model_choice%"=="1" (
    echo.
    echo 🇷🇺 Запуск русской модели...
    python "..\..\scripts\testing\test_generation_ru.py"
) else if "%model_choice%"=="2" (
    echo.
    echo 🇺🇸 Запуск английской модели...
    python "..\..\scripts\testing\test_generation.py"
) else if "%model_choice%"=="3" (
    goto MAIN_MENU
) else (
    echo ❌ Неверный выбор
    pause
    goto COMMAND_LINE
)
echo.
pause
goto MAIN_MENU

:TRAINING
cls
echo.
echo 🎓 Обучение моделей
echo.
echo 🚀 Выберите действие:
echo 1️⃣  🇷🇺 Обучение русской модели
echo 2️⃣  🇺🇸 Обучение английской модели
echo 3️⃣  📊 Создание тестовых данных
echo 4️⃣  🔙 Назад
echo.
set /p train_choice="Введите номер (1-4): "

if "%train_choice%"=="1" (
    echo.
    echo 🇷🇺 Обучение русской модели...
    python "..\..\scripts\training\train_model_ru.py"
) else if "%train_choice%"=="2" (
    echo.
    echo 🇺🇸 Обучение английской модели...
    python "..\..\src\train_model.py"
) else if "%train_choice%"=="3" (
    echo.
    echo 📊 Создание тестовых данных...
    python "..\..\scripts\testing\test_formats.py"
) else if "%train_choice%"=="4" (
    goto MAIN_MENU
) else (
    echo ❌ Неверный выбор
    pause
    goto TRAINING
)
echo.
pause
goto MAIN_MENU

:TESTING
cls
echo.
echo 🧪 Тестирование
echo.
echo 🚀 Выберите тест:
echo 1️⃣  🇷🇺 Тест русской модели
echo 2️⃣  🇺🇸 Тест английской модели
echo 3️⃣  📊 Тест форматов данных
echo 4️⃣  🔙 Назад
echo.
set /p test_choice="Введите номер (1-4): "

if "%test_choice%"=="1" (
    echo.
    echo 🇷🇺 Тестирование русской модели...
    python "..\..\scripts\testing\test_generation_ru.py"
) else if "%test_choice%"=="2" (
    echo.
    echo 🇺🇸 Тестирование английской модели...
    python "..\..\scripts\testing\test_generation.py"
) else if "%test_choice%"=="3" (
    echo.
    echo 📊 Тестирование форматов данных...
    python "..\..\scripts\testing\test_formats.py"
) else if "%test_choice%"=="4" (
    goto MAIN_MENU
) else (
    echo ❌ Неверный выбор
    pause
    goto TESTING
)
echo.
pause
goto MAIN_MENU

:BUILD
cls
echo.
echo 🔨 Сборка приложений
echo.
echo 🚀 Выберите сборку:
echo 1️⃣  🖥️  Windows exe файл
echo 2️⃣  🌐  Веб-интерфейс exe
echo 3️⃣  🔙 Назад
echo.
set /p build_choice="Введите номер (1-3): "

if "%build_choice%"=="1" (
    echo.
    echo 🖥️ Создание Windows exe файла...
    python "..\..\scripts\build\build_windows_exe.py"
) else if "%build_choice%"=="2" (
    echo.
    echo 🌐 Создание веб-интерфейса exe...
    python "..\..\scripts\build\build_exe.py"
) else if "%build_choice%"=="3" (
    goto MAIN_MENU
) else (
    echo ❌ Неверный выбор
    pause
    goto BUILD
)
echo.
pause
goto MAIN_MENU

:DOCUMENTATION
cls
echo.
echo 📚 Документация
echo.
echo 📖 Открываем папку с документацией...
start "" "..\..\docs\guides"
echo.
echo 💡 Доступные руководства:
echo    📋 README.md - Основная информация
echo    🚀 QUICK_START.md - Быстрый старт
echo    🎓 TRAINING_GUIDE.md - Обучение моделей
echo    🖥️ WINDOWS_INTERFACE_GUIDE.md - Windows интерфейс
echo    🌐 WEB_INTERFACE_GUIDE.md - Веб-интерфейс
echo.
pause
goto MAIN_MENU

:SETTINGS
cls
echo.
echo ⚙️ Настройки
echo.
echo 🔧 Выберите действие:
echo 1️⃣  📦 Установка зависимостей
echo 2️⃣  🧹 Очистка временных файлов
echo 3️⃣  📊 Статус проекта
echo 4️⃣  🔙 Назад
echo.
set /p settings_choice="Введите номер (1-4): "

if "%settings_choice%"=="1" (
    echo.
    echo 📦 Установка зависимостей...
    pip install -r "..\..\requirements.txt"
) else if "%settings_choice%"=="2" (
    echo.
    echo 🧹 Очистка временных файлов...
    if exist "..\..\build" rmdir /s /q "..\..\build"
    if exist "..\..\dist" rmdir /s /q "..\..\dist"
    if exist "..\..\*.spec" del /q "..\..\*.spec"
    echo ✅ Очистка завершена
) else if "%settings_choice%"=="3" (
    echo.
    echo 📊 Статус проекта:
    echo.
    if exist "..\..\models\history_ai_trained" (
        echo ✅ Английская модель: Обучена
    ) else (
        echo ❌ Английская модель: Не обучена
    )
    if exist "..\..\models\history_ai_ru_trained" (
        echo ✅ Русская модель: Обучена
    ) else (
        echo ❌ Русская модель: Не обучена
    )
    if exist "..\..\ИИ_История_Windows.exe" (
        echo ✅ Windows exe: Создан
    ) else (
        echo ❌ Windows exe: Не создан
    )
) else if "%settings_choice%"=="4" (
    goto MAIN_MENU
) else (
    echo ❌ Неверный выбор
    pause
    goto SETTINGS
)
echo.
pause
goto MAIN_MENU

:HELP
cls
echo.
echo ❓ Помощь
echo.
echo 🎯 Основные функции:
echo    🖥️  Windows интерфейс - нативное приложение
echo    🌐  Веб-интерфейс - через браузер
echo    📝  Командная строка - для разработчиков
echo.
echo 🎓 Обучение:
echo    🇷🇺  Русская модель - для русских промптов
echo    🇺🇸  Английская модель - для английских промптов
echo.
echo 🧪 Тестирование:
echo    📊  Проверка работы моделей
echo    📁  Тестирование форматов данных
echo.
echo 🔨 Сборка:
echo    🖥️  Windows exe - нативное приложение
echo    🌐  Веб exe - веб-приложение
echo.
echo 📚 Документация:
echo    📋  README.md - основная информация
echo    🚀  QUICK_START.md - быстрый старт
echo    🎓  TRAINING_GUIDE.md - обучение
echo.
echo 💡 Советы:
echo    - Начните с Windows интерфейса
echo    - Сначала обучите модели
echo    - Используйте примеры промптов
echo.
pause
goto MAIN_MENU

:QUICK_TRAIN_RU
cls
echo.
echo 🚀 Быстрое обучение русской модели
echo.
echo 📊 Это может занять несколько минут...
echo 💡 Убедитесь, что есть данные в data/raw/
echo.
echo 🚀 Запускаем обучение...
echo.
python "..\..\scripts\training\quick_train_ru.py"
echo.
if errorlevel 1 (
    echo ❌ Ошибка обучения русской модели
    echo.
    echo 💡 Возможные решения:
    echo    1. Проверьте наличие данных в data/raw/
    echo    2. Установите зависимости: pip install -r requirements.txt
    echo    3. Проверьте подключение к интернету
) else (
    echo ✅ Обучение завершено успешно!
    echo 🎉 Теперь можно использовать русскую модель в интерфейсе
)
echo.
pause
goto MAIN_MENU

:INVALID
echo.
echo ❌ Неверный выбор! Попробуйте снова.
pause
goto MAIN_MENU

:EXIT
echo.
echo 👋 До свидания!
echo.
echo 🏛️ Спасибо за использование ИИ для изучения истории!
echo.
pause
exit
