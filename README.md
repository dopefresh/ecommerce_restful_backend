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


## Регистрация пользователя:
1. POST localhost:8000/api/v1/users/ нужную информацию смотрим на localhost:8000/api/schema/swagger-ui/
2. POST localhost:8000/api/v1/jwt/create/ нужную информацию смотрим на localhost:8000/api/schema/swagger-ui/, Получаем access и refresh токены, refresh нужен для обновления access токена, который истекает через 30 минут после создания
3. В view, в которых нужна авторизация используйте access token в header вот такой параметр: Authorization: Bearer <token>

