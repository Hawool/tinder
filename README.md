# my_test_tinder

Бекэнд для сайта (приложения) знакомств.

Задачи:
1. Создать модель участников. У участника должна быть аватарка, пол, имя и фамилия, почта.
2. Создать эндпоинт регистрации нового участника: /api/clients/create (не забываем о пароле и совместимости с авторизацией модели участника).
3. При регистрации нового участника необходимо обработать его аватарку: наложить на него водяной знак (в качестве водяного знака можете взять любую картинку).
4. Создать эндпоинт оценивания участником другого участника: /api/clients/{id}/match. В случае, если возникает взаимная симпатия, то ответом выдаем почту клиенту и отправляем на почты участников: «Вы понравились <имя>! Почта участника: <почта>».
5. Создать эндпоинт списка участников: /api/list. Должна быть возможность фильтрации списка по полу, имени, фамилии. Советую использовать библиотеку Django-filters.
6. Реализовать определение дистанции между участниками. Добавить поля долготы и широты. В api списка добавить дополнительный фильтр, который бы показывал участников в пределах заданной дистанции. Не забывайте об оптимизации запросов к базе данных
https://en.wikipedia.org/wiki/Great-circle_distance
7. Задеплоить проект на любом удобном для вас хостинге, сервисах PaaS (Heroku) и т.п. Должна быть возможность просмотреть реализацию всех задач. Если есть какие-то особенности по тестированию, написать в Readme. Там же оставить ссылку/ссылки на АПИ проекта

Приложение можно посмотреть по адресу https://mytesttinder.herokuapp.com
Документация по API представлена на странице https://mytesttinder.herokuapp.com/swagger/

Иструкция по запуску на локальной машине:
- git clone https://gitlab.com/Hawool/tinder.git
- cd tinder
- docker build -t tinder_img .
- docker run --rm --name tinder_container -p 8000:8000 tinder_img

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

