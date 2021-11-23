# my_test_tinder

Тестовая задача: приложение для знакомств.

Реализованные задачи:
1. Модель участников. У участника аватарка, пол, имя и фамилия, почта.
2. Эндпоинт регистрации нового участника: /api/clients/create.
3. Обрабатывается аватарка участника при регистрации: накладывается на него водяной знак.
4. Эндпоинт оценивания участником другого участника: /api/clients/{id}/match. В случае, если возникает взаимная симпатия, то ответом выдается почта клиенту и отправляется на почты участников: «Вы понравились <имя>! Почта участника: <почта>».
5. Эндпоинт списка участников: /api/list. Добавлена возможность фильтрации списка по полу, имени, фамилии. Используется библиотека Django-filters.
6. Реализовано определение дистанции между участниками. Добавлено поля долготы и широты.
https://en.wikipedia.org/wiki/Great-circle_distance
7. Проект задеплоен на хостинге Heroku.

Приложение можно посмотреть по адресу https://mytesttinder.herokuapp.com
Документация по API представлена на странице https://mytesttinder.herokuapp.com/swagger/

Иструкция по запуску на локальной машине:
- git clone https://github.com/Hawool/tinder.git
- cd tinder
- docker-compose up -d --build
- docker-compose exec api python manage.py migrate --noinput

Затем можно открыть в браузере http://0.0.0.0:8000

## Несколько запросов для работы с приложением:

### Создание клиента:
- Request method: POST
- URL: https://mytesttinder.herokuapp.com/api/v1/clients/create
- Body:
  - password: password
  - username: username
  - email: email, format: email@gmail.com
  - avatar: avatar, format: file
  - gender: gender
  - longitude: longitude
  - latitude: latitude
- sample CLI command:

curl --location --request POST 'https://mytesttinder.herokuapp.com/api/v1/clients/create' \
--form 'password=... ' \
--form 'username=...' \
--form 'email=...' \
--form 'avatar=...' \
--form 'gender=...' \
--form 'longitude=...' \
--form 'latitude=...'

example body:  
{  
        "password": "Qwerty123",  
        "username": "qwerty",  
        "email": "email@gmail.com",  
        "avatar": "https://mytesttinder.herokuapp.com/media/avatar/1/file.png",  
        "gender": "M",  
        "longitude": 30.5342234,  
        "latitude": 12.945643,  
    },

### Авторизация, получение токена

- Request method: POST
- URL: https://mytesttinder.herokuapp.com/api/v1/clients/login
- Body:
  - password: password
  - username: username
- sample CLI command:

curl --location --request POST 'https://mytesttinder.herokuapp.com/api/v1/clients/login' \
--form 'username=%username' \
--form 'password=%password'

example body:  
{  
        "password": "Qwerty123",  
        "username": "qwerty"  
}

### Просмотр всех пользователей

- Request method: GET
- URL: https://mytesttinder.herokuapp.com/api/v1/clients/all'
- Header: Authorization: Token userToken
- sample CLI command:

curl --location --request GET 'https://mytesttinder.herokuapp.com/api/v1/clients/all' \
--header 'Authorization: Token %userToken'

### Создание оценивания участником другого участника

- Request method: POST
- URL: https://mytesttinder.herokuapp.com/api/v1/clients/{other_client_id}/match
- Header: Authorization: Token userToken
- Body:
  - like: like
- sample CLI command:

curl --location --request POST 'https://mytesttinder.herokuapp.com/api/v1/clients/{other_client_id}/match' \
--header 'Authorization: Token %userToken'
--form 'like=%like'

example body:  
{  
        "like": True,  
}

