# foodgram


- Проект развернут здесь https://foodram.ru

- IP - 158.160.73.228

- доступ к админ-панели
  - логин admin@example.com
  - пароль superadmin
---
![Static Badge](https://img.shields.io/badge/python-%25?style=for-the-badge&logo=python&labelColor=FFC436&color=blue) ![Static Badge](https://img.shields.io/badge/django-%25?style=for-the-badge&logo=django&labelColor=116D6E&color=47A992) ![Static Badge](https://img.shields.io/badge/rest_api-%25?style=for-the-badge&logo=rest_api&labelColor=9BABB8&color=9BABB8) ![Static Badge](https://img.shields.io/badge/postgresql-%25?style=for-the-badge&logo=postgresql&labelColor=F5F5F5&color=F5F5F5) ![Static Badge](https://img.shields.io/badge/nginx-%25?style=for-the-badge&logo=nginx&labelColor=16FF00&color=F5F5F5) ![Static Badge](https://img.shields.io/badge/docker-%25?style=for-the-badge&logo=docker&color=2F58CD)





### Описание

Foodgram - продуктовый помощник, где зарегистрированные пользователи могут публиковать свои рецепты. Все опубликованные рецепты доступны на главной странице всем пользователям. Есть возможность подписаться на автора рецепта, после чего все рецепты избранного автора появляются на странице подписок. Также рецепты можно добавить в избранное. Авторизованный пользователь может добавить ингредиенты любого рецепта в список покупок. Количество ингредиентов суммируется. Список можно скачать файлом в формате txt

---
### Инструцкия по запуску

###### Запуск бэкенда
Если в вашей ОС отсутствует Postgres, то перед запуском перейдите в файл `foodgram/settings.py` и найдите блок с закомментированным `DATABASE`. Нужно чтобы выглядело вот так:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('POSTGRES_DB', 'django'),
#         'USER': os.getenv('POSTGRES_USER', 'django'),
#         'PASSWORD': os.getenv('POSTGRES_PASSWORD', ''),
#         'HOST': os.getenv('DB_HOST', ''),
#         'PORT': os.getenv('DB_PORT', 5432)
#     }
# }
```
Затем перейдите в каталог backend и выполните следующие команды
```bash
cd backend/
python3 -m venv venv  # устанавливаем виртуальное окружение
source venv/bin/activate  # активируем виртульное окружение
python -m pip install --upgrade pip  # обновляем pip
pip install -r requirements.txt  # устанавливаем зависимости
python manage.py migrate  # проводим миграции
python manage.py runserver  # запускаем проект
```
После выполненных команд вы сможете выполнять запросы к `http://localhost:8000`, например через [Postman](https://www.postman.com/)


### Примеры запросов и их ответов

```json
GET localhost:8000/api/recipes/  

Ответ:
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "tags": [
                {
                    "id": 1,
                    "name": "завтрак",
                    "color": "#E26C2D",
                    "slug": "breakfast"
                }
            ],
            "author": {
                "email": "user@example.com",
                "id": 9,
                "username": "string",
                "first_name": "string",
                "last_name": "string",
                "is_subscribed": false
            },
            "ingredients": [
                {
                    "id": 1,
                    "name": "string",
                    "measurement_unit": "г",
                    "amount": 123
                },
            ],
            "name": "string",
            "image": "/media/recipes/images/temp_vwWkwMf.jpeg",
            "text": "string",
            "cooking_time": 123
        },
    ]



POST localhost:8000/api/recipes/

Тело запроса:
{
    "ingredients": [
        {
            "id": 5,
            "amount": 123
        }
  ],
    "tags": [
        1
    ],
    "image": "data:image/jpeg;base64,<base64code>",
    "name": "string",
    "text": "string",
    "cooking_time": 123
}

Ответ:
{
    "id": 1,
    "tags": [
        {
            "id": 1,
            "name": "завтрак",
            "color": "#E26C2D",
            "slug": "breakfast"
        }
    ],
    "author": {
        "email": "user@example.com",
        "id": 1,
        "username": "string",
        "first_name": "string",
        "last_name": "string",
        "is_subscribed": true
    },
    "ingredients": [
        {
            "id": 1,
            "name": "string",
            "measurement_unit": "г",
            "amount": 123
        }
    ],
    "name": "string",
    "image": "/media/recipes/images/temp_cHzKsbd.jpeg",
    "text": "string",
    "cooking_time": 5

}



POST http://localhost:8000/api/users/

Тело запроса:
{
    "email": "user@example.com",
    "username": "string",
    "first_name": "string",
    "last_name": "string",
    "password": "string"
}

Ответ:
{
    "email": "user@gmail.com",
    "id": 1,
    "username": "string",
    "first_name": "string",
    "last_name": "string"
}



POST http://localhost:8000/api/auth/token/login/

Тело запроса:
{
    "password": "string",
    "email": "user@example.com"
}

Ответ:
{
    "auth_token": "3b1a9136050e2cb3c92280c013ab39c90b273915"
}
```

---
Для следующих команд нужен установленный в вашей ОС [Docker](https://www.docker.com/)

```bash
docker compose up  # разворачивам проект на локальном сервере
docker compose exec backend python manage.py migrate  # выполяем миграции
docker compose exec backend python manage.py collectstatic  # собираем статику для админки
docker compose exec backend python manage.py createsuperuser  # создаем учетную запись администратора
```

Для того, чтобы остановить сеть и удалить контейнеры выполните
```bash
docker compose down -v  # флаг -v нужен, если вы хотите удалить созданные volumes
```
---
  