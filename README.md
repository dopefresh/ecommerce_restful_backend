## Запуск:
1. git clone https://github.com/dopefresh/ecommerce_rest_backend.git
2. curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
2. Если не вышел 2 шаг в PowerShellе вводим: (Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
2. Если снова не вышел 2 шаг: pip install poetry либо pip3 install poetry
3. poetry install
4. poetry shell
5. секретный ключ нужно поменять
6. В PostgreSQL создайте базу данных с любым именем
7. Создайте и заполните файл .env по образцу файла .example.env
8. python manage.py migrate
9. docker-compose up

## Использованные технологии:
1. django
2. django-rest-framework
3. django-rest-framework-simple-jwt
4. drf-spectacular(openapi 3.0 генератор)
5. postgresql database
6. flake8
7. loguru для логгирования

## Функционал:
1. Просмотр пользователем категорий товаров(не требует регистрации и логина)
2. Просморт пользователем подкатегорий товаров(не требует регистрации и логина)
3. Просмотр пользователем списка товаров с фотографией(не требует регистрации и логина)
4. Просмотр пользователем одного товара с фотографией(не требует регистрации и логина)
5. Просмотр корзины(требуется создать аккаунт и получить jwt access токен)
6. Добавление товаров в корзину(требуется создать аккаунт и получить jwt access токен)
7. Изменение количества всех товаров в корзине(требуется создать аккаунт и получить jwt access токен)
8. Удаление одного товара из корзины(требуется создать аккаунт и получить jwt access токен)
9. Регистрация и получение токена пользователем
10. Регистрация и получение токена сотрудником компании

## TODO:
1. Чат с сотрудниками компании по поводу товара

## Непонятно
1. Доставка товара
2. Регистрация компаний

