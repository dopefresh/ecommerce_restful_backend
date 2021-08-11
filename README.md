## Запуск:
1. git clone https://github.com/dopefresh/ecommerce_rest_backend-Django-Rest-Framework-JWT-Authentication-by-djoser-.git
2. curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
2. Если не вышел 2 шаг в PowerShellе вводим: (Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
2. Если снова не вышел 2 шаг: pip install poetry либо pip3 install poetry
3. poetry install
4. poetry shell
5. секретный ключ нужно поменять
6. в psql, с указанными в файле .env настройками вводим: CREATE DATABASE ecommerce_db;
7. python manage.py migrate
8. docker-compose up или python(3 на линуксе) manage.py runserver
