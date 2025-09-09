#!/usr/bin/env python3
"""
Скрипт для автоматической установки и настройки ИИ среды
для проекта изучения истории
"""

import subprocess
import sys
import os
import platform

def run_command(command, description):
    """Выполняет команду и выводит результат"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {description} завершено успешно")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при {description.lower()}:")
        print(f"   {e.stderr}")
        return False

def check_python_version():
    """Проверяет версию Python"""
    version = sys.version_info
    print(f"🐍 Версия Python: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Требуется Python 3.8 или выше!")
        return False
    print("✅ Версия Python подходит")
    return True

def create_virtual_environment():
    """Создает виртуальное окружение"""
    if not os.path.exists("venv"):
        return run_command("python -m venv venv", "Создание виртуального окружения")
    else:
        print("✅ Виртуальное окружение уже существует")
        return True

def activate_and_install():
    """Активирует виртуальное окружение и устанавливает зависимости"""
    if platform.system() == "Windows":
        pip_cmd = "venv\\Scripts\\python.exe -m pip"
    else:
        pip_cmd = "venv/bin/pip"
    
    # Обновляем pip
    if not run_command(f"{pip_cmd} install --upgrade pip", "Обновление pip"):
        return False
    
    # Устанавливаем зависимости
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Установка зависимостей"):
        return False
    
    return True

def create_project_structure():
    """Создает структуру проекта"""
    directories = [
        "data/raw",
        "data/processed", 
        "models",
        "notebooks",
        "src",
        "src/models",
        "src/data",
        "src/utils",
        "logs",
        "configs"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Создана папка: {directory}")
    
    # Создаем .gitignore
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# Jupyter Notebook
.ipynb_checkpoints

# Model files
*.pkl
*.joblib
*.h5
*.pb
models/*.pt
models/*.pth

# Data files
data/raw/*
data/processed/*
!data/raw/.gitkeep
!data/processed/.gitkeep

# Logs
logs/
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
"""
    
    with open(".gitignore", "w", encoding="utf-8") as f:
        f.write(gitignore_content)
    
    # Создаем .gitkeep файлы
    with open("data/raw/.gitkeep", "w") as f:
        pass
    with open("data/processed/.gitkeep", "w") as f:
        pass
    
    print("✅ Структура проекта создана")

def main():
    """Основная функция установки"""
    print("🚀 Начинаем установку ИИ среды для проекта изучения истории")
    print("=" * 60)
    
    # Проверяем Python
    if not check_python_version():
        sys.exit(1)
    
    # Создаем виртуальное окружение
    if not create_virtual_environment():
        print("❌ Не удалось создать виртуальное окружение")
        sys.exit(1)
    
    # Устанавливаем зависимости
    if not activate_and_install():
        print("❌ Не удалось установить зависимости")
        sys.exit(1)
    
    # Создаем структуру проекта
    create_project_structure()
    
    print("\n" + "=" * 60)
    print("🎉 Установка завершена успешно!")
    print("\n📋 Следующие шаги:")
    print("1. Активируйте виртуальное окружение:")
    if platform.system() == "Windows":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("2. Запустите Jupyter Notebook:")
    print("   jupyter notebook")
    print("3. Откройте файл notebooks/getting_started.ipynb")
    print("\n💡 Для обучения модели используйте:")
    print("   python src/train_model.py")

if __name__ == "__main__":
    main()
