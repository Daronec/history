@echo off
chcp 65001 >nul
title Создание Windows exe файла
color 0A

echo.
echo 🏛️ Создание Windows exe файла для ИИ интерфейса
echo ========================================
echo.

echo 📦 Устанавливаем PyInstaller...
pip install pyinstaller

echo.
echo 🔨 Создаем Windows exe файл...
echo.

pyinstaller --onefile --windowed --name "ИИ_История_Windows" ^
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
    windows_interface.py

if exist "dist\ИИ_История_Windows.exe" (
    echo.
    echo ✅ Windows exe файл создан успешно!
    echo 📁 Файл: dist\ИИ_История_Windows.exe
    echo.
    echo 🚀 Перемещаем exe в корень проекта...
    move "dist\ИИ_История_Windows.exe" "ИИ_История_Windows.exe"
    
    echo Очищаем временные файлы...
    rmdir /s /q "build"
    rmdir /s /q "dist"
    del "ИИ_История_Windows.spec"
    
    echo.
    echo 🎉 Готово! Файл ИИ_История_Windows.exe создан
    echo 🖥️ Это нативное Windows приложение - никаких браузеров!
    echo.
    echo 💡 Теперь вы можете:
    echo    - Запускать ИИ интерфейс одним кликом
    echo    - Работать без браузера
    echo    - Использовать нативный Windows интерфейс
    echo.
) else (
    echo.
    echo ❌ Ошибка создания Windows exe файла
)

echo.
pause
