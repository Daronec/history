@echo off
chcp 65001 >nul
title 🏛️ ИИ для изучения истории - Windows интерфейс
color 0F

echo.
echo ████████████████████████████████████████████████████████████
echo ██                                                        ██
echo ██  🏛️  ИИ для изучения истории - Windows интерфейс  🏛️  ██
echo ██                                                        ██
echo ██  Нативный Windows интерфейс для работы с ИИ моделью   ██
echo ██                                                        ██
echo ████████████████████████████████████████████████████████████
echo.

echo 🚀 Запускаем Windows интерфейс...
echo.

python windows_interface.py

if errorlevel 1 (
    echo.
    echo ❌ Ошибка запуска Windows интерфейса
    echo.
    echo 💡 Возможные решения:
    echo    1. Убедитесь, что Python установлен
    echo    2. Установите tkinter: pip install tk
    echo    3. Проверьте, что все файлы на месте
    echo.
    pause
) else (
    echo.
    echo 👋 Windows интерфейс закрыт
    echo.
)
