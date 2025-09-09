@echo off
chcp 65001 >nul
title Создание exe файла ИИ интерфейса
color 0A

echo.
echo 🏛️ Создание exe файла для ИИ интерфейса
echo ========================================
echo.

echo 📦 Устанавливаем PyInstaller...
pip install pyinstaller

echo.
echo 🔨 Создаем exe файл...
echo.

pyinstaller --onefile --console --name "ИИ_История" ^
    --add-data "templates;templates" ^
    --add-data "src;src" ^
    --add-data "data;data" ^
    --add-data "models;models" ^
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
    web_interface.py

if exist "dist\ИИ_История.exe" (
    echo.
    echo ✅ Exe файл создан успешно!
    echo 📁 Файл: dist\ИИ_История.exe
    echo.
    echo 🚀 Теперь вы можете запускать ИИ интерфейс одним кликом!
    echo.
    
    echo Перемещаем exe в корень проекта...
    move "dist\ИИ_История.exe" "ИИ_История.exe"
    
    echo Очищаем временные файлы...
    rmdir /s /q "build"
    rmdir /s /q "dist"
    del "ИИ_История.spec"
    
    echo.
    echo 🎉 Готово! Файл ИИ_История.exe создан в корне проекта
) else (
    echo.
    echo ❌ Ошибка создания exe файла
)

echo.
pause
