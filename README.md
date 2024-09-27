# Развертывание и локальный запуск проекта

## Шаг 1: Клонирование проекта
1. Клонируйте проект из репозитория:
   ```bash
   git clone <URL вашего репозитория>
   cd <имя директории вашего проекта>
Шаг 2: Настройка виртуальной среды
Убедитесь, что у вас установлен Python 3.12 или выше. Установите его при необходимости:

sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev
Создайте виртуальную среду:
python3 -m venv env
Активируйте виртуальную среду:
source env/bin/activate
pip install -r requirements.txt
python3 manage.py runserver 0.0.0.0:8000
