@echo off
REM Batch file for AI model training on Windows
REM Usage: train.bat <command>

setlocal enabledelayedexpansion

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="sample" goto train_sample
if "%1"=="pdf" goto train_pdf
if "%1"=="csv" goto train_csv
if "%1"=="txt" goto train_txt
if "%1"=="custom" goto train_custom
if "%1"=="test" goto test_generation
if "%1"=="train_ru" goto train_ru
if "%1"=="test_ru" goto test_ru
if "%1"=="web" goto web
if "%1"=="demo" goto demo
if "%1"=="status" goto status
if "%1"=="clean" goto clean
goto help

:help
echo ========================================
echo    AI History Learning Project
echo ========================================
echo.
echo Available commands:
echo   train.bat sample     - Train on examples (1 epoch)
echo   train.bat pdf        - Train on PDF data
echo   train.bat csv        - Train on CSV data
echo   train.bat txt        - Train on TXT data
echo   train.bat custom     - Train on custom data
echo   train.bat test       - Test generation (English)
echo   train.bat train_ru   - Train Russian model
echo   train.bat test_ru    - Test Russian generation
echo   train.bat web        - Start web interface
echo   train.bat demo       - Demo
echo   train.bat status     - Project status
echo   train.bat clean      - Cleanup
echo.
goto end

:train_sample
echo [TRAINING] Training model on examples...
python src/train_model.py --data sample --task generation --epochs 1 --model distilgpt2
goto end

:train_pdf
echo [TRAINING] Training model on PDF data...
python src/train_model.py --data data/processed/pdf_history_data.json --task generation --epochs 1 --model distilgpt2
goto end

:train_csv
echo [TRAINING] Training model on CSV data...
python src/train_model.py --data data/raw/example_history.csv --task generation --epochs 1 --model distilgpt2
goto end

:train_txt
echo [TRAINING] Training model on TXT data...
python src/train_model.py --data data/raw/example_history.txt --task generation --epochs 1 --model distilgpt2
goto end

:train_custom
echo [TRAINING] Training model on custom data...
if "%2"=="" (
    echo ERROR: Please specify data file path
    echo Example: train.bat custom data/raw/my_data.json
    goto end
)
python src/train_model.py --data %2 --task generation --epochs 1 --model distilgpt2
goto end

:test_generation
echo [TEST] Testing text generation...
python test_generation.py
goto end

:train_ru
echo [TRAINING] Training Russian model...
python train_model_ru.py
goto end

:test_ru
echo [TEST] Testing Russian text generation...
python test_generation_ru.py
goto end

:web
echo [WEB] Starting web interface...
python web_interface.py
goto end

:demo
echo [DEMO] Starting demonstration...
python demo.py
goto end

:status
echo ========================================
echo           PROJECT STATUS
echo ========================================
if exist "venv" (
    echo Virtual environment: [OK] Installed
) else (
    echo Virtual environment: [NO] Not installed
)

if exist "models\history_ai_trained" (
    echo Trained model: [OK] Available
) else (
    echo Trained model: [NO] Not available
)

if exist "data\processed\pdf_history_data.json" (
    echo PDF data: [OK] Available
) else (
    echo PDF data: [NO] Not available
)

if exist "data\raw\sample_history_data.json" (
    echo Sample data: [OK] Available
) else (
    echo Sample data: [NO] Not available
)
goto end

:clean
echo [CLEANUP] Cleaning temporary files...
if exist "__pycache__" rmdir /s /q "__pycache__"
if exist "src\__pycache__" rmdir /s /q "src\__pycache__"
if exist "src\models\__pycache__" rmdir /s /q "src\models\__pycache__"
if exist "models\history_ai_trained" rmdir /s /q "models\history_ai_trained"
echo [OK] Cleanup completed
goto end

:end