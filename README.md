
## Социальная сеть для размещения отзывов


## Технологии:

[![Python](https://img.shields.io/badge/python-3.10-blue?logo=python)](https://www.python.org/)
[![DjangoRestFramework](https://img.shields.io/badge/DjangoRestFramework-black?logo=django)](https://www.django-rest-framework.org/)
[![SQLite](https://img.shields.io/badge/SQLite-blue?logo=sqlite)](https://www.sqlite.org/index.html)


## Оглавление
1. [Описание](#описание)
2. [Стек технологий](##стек-технологий)
3. [Как запустить проект](##как-запустить-проект)
4. [Автор проекта](##автор-проекта)


## Описание работы

Проект собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведениям присваиваются категории, жанры и рейтинг. Список категорий и жанров может быть расширен, но правами на добавление новых жанров, категорий и произведений обладает только администратор. 
Для авторизации пользователей используется код подтверждения.
Для аутентификации пользователей используются JWT-токены.

## Стек технологий

- проект написан на Python с использованием Django REST Framework
- библиотека Simple JWT - работа с JWT-токеном
- библиотека django-filter - фильтрация запросов
- базы данны - SQLite3
- система контроля версий - git

## Как запустить проект

- Клонируйте репозитоий
```
git clone https://github.com/ZebraHr/api_yamdb.git
```
- Перейдите в папку проекта
```
cd api_yamdb
```
- Создайте и активируйте виртуальное окружение:
```
python -m venv venv
source venv/Scripts/activate
```
```
python3 -m pip install --upgrade pip
```
- Установите зависимости:
```
pip install -r requirements.txt
```
- Сделайте миграции:
```
cd api_yamdb
python manage.py migrate
```
- Запустите проект:
```
python manage.py runserver
```
Для управления через систему администратора создайте superuser:
```
python manage.py createsuperuser
```
### Примеры запросов
Пример GET-запроса получение всех произведений
```
GET .../api/v1/titles/
http://127.0.0.1:8000/api/v1/titles/?category=movie
```
Ответ
```
{
    "count": 0,
    "next": "http://127.0.0.1:8000/api/v1/titles/?page=2",
    "previous": null,
    "results": [
        {
            "id": 0,
            "name": "string",
            "year": 0,
            "rating": 0,
            "description": null,
            "genre": [],
            "category": {
                "name": "string",
                "slug": "string"
            }
        }
```
Пример POST-запроса добавление нового произведения
```
POST .../api/v1/titles/
```
```
{
"name": "string",
"year": 0,
"description": "string",
"genre": [
"string"
],
"category": "string"
}
```
Ответ
```
{
"id": 0,
"name": "string",
"year": 0,
"rating": 0,
"description": "string",
"genre": [
{}
],
"category": {
"name": "string",
"slug": "string"
}
}
```
Пример GET-запроса получения комментария по id
```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
Ответ
```
{
"count": 0,
"next": "string",
"previous": "string",
"results": [
{}
]
}
```
##### Весь доступный функционал API:
```
/redoc/
```
### Автор
[Ольга Викторова](https://github.com/vikolga)

[Тимур Булатов](https://github.com/T1mBul)

[Анна Победоносцева](https://github.com/ZebraHr) тимлид
