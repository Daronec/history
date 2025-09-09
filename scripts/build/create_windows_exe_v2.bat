@echo off
chcp 65001 >nul
title Создание исправленного Windows exe файла
color 0A

echo.
echo 🏛️ Создание исправленного Windows exe файла
echo ========================================
echo.

echo 📦 Устанавливаем PyInstaller...
pip install pyinstaller

echo.
echo 🔨 Создаем исправленный Windows exe файл...
echo.

pyinstaller --onefile --windowed --name "ИИ_История_Windows_v2" ^
    --add-data "src;src" ^
    --add-data "data;data" ^
    --add-data "models;models" ^
    --hidden-import tkinter ^
    --hidden-import tkinter.ttk ^
    --hidden-import tkinter.scrolledtext ^
    --hidden-import tkinter.messagebox ^
    --hidden-import tkinter.filedialog ^
    --hidden-import flask ^
    --hidden-import transformers ^
    --hidden-import torch ^
    --hidden-import tensorflow ^
    --hidden-import numpy ^
    --hidden-import pandas ^
    --hidden-import sklearn ^
    --hidden-import matplotlib ^
    --hidden-import seaborn ^
    --hidden-import requests ^
    --hidden-import beautifulsoup4 ^
    --hidden-import lxml ^
    --hidden-import tqdm ^
    --hidden-import jupyter ^
    --hidden-import ipykernel ^
    interfaces\windows\windows_interface_exe.py

if exist "dist\ИИ_История_Windows_v2.exe" (
    echo.
    echo ✅ Исправленный Windows exe файл создан успешно!
    echo 📁 Файл: dist\ИИ_История_Windows_v2.exe
    echo.
    echo 🚀 Перемещаем exe в корень проекта...
    move "dist\ИИ_История_Windows_v2.exe" "ИИ_История_Windows_v2.exe"
    
    echo Очищаем временные файлы...
    rmdir /s /q "build"
    rmdir /s /q "dist"
    del "ИИ_История_Windows_v2.spec"
    
    echo.
    echo 🎉 Готово! Файл ИИ_История_Windows_v2.exe создан
    echo 🖥️ Это исправленная версия с правильными путями!
    echo.
    echo 💡 Исправления:
    echo    - Правильные пути к модулям в exe
    echo    - Fallback на предобученные модели
    echo    - Улучшенная обработка ошибок
    echo    - Поддержка работы без интернета
    echo.
) else (
    echo.
    echo ❌ Ошибка создания исправленного Windows exe файла
)

echo.
pause
