# Api_Yamdb
![](https://github.com/clownvkkaschenko/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
### Описание проекта:
Проект Api\_Yamdb собирает отзывы пользователей на произведения . Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий может быть расширен администратором. Сами произведения в Api\_Yamdb не хранятся, здесь нельзя посмотреть фильм или послушать музыку. В категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха. Произведению может быть присвоен жанр из списка предустановленных. Новые жанры может создавать только администратор. Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти; из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. На одно произведение пользователь может оставить только один отзыв.
Для удобного запуска на любой локальной машине проект Api_Yamdb представлен в контейнере Docker.
### Запуск приложения:
Клонируйте репозиторий и перейти в корневую папку:
```
$ git clone git@github.com:clownvkkaschenko/infra_sp2.git
```
Cоздайте файл .env в папке infra:
```
$ touch infra_sp2/infra/.env
```
Заполните этот файл, придумайте и введите пароль в последней строке:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
DB_HOST=db
DB_PORT=5432
POSTGRES_PASSWORD=password
```
Перейдите в папку infra и запустите docker-compose:
```
~$ docker-compose up -d --build
```
Теперь в контейнере web нужно выполнить миграции, создать суперпользователя и собрать статику:
```
~$ docker-compose exec web python manage.py migrate
~$ docker-compose exec web python manage.py createsuperuser
~$ docker-compose exec web python manage.py collectstatic --no-input
```
Теперь проект доступен по адресу http://localhost/
### Загрузка данных из csv файлов в бд:
```
~$ docker-compose exec web python manage.py load_csv
```
### Остановка и запуск docker-compose:
```
~$ docker-compose stop
```
```
~$ docker-compose start
```
### Примеры выполнения запросов для API:
#### - Получаем JWT-токена(POST запрос)
```
api/v1/jwt/create/
```
Payload:
```
{
    "username": "string",
    "password": "string"
}
```
Response sample (status code = 200):
```
{
    "token": "string"
}
```
#### - Получение списка всех категорий(GET запрос)
(*Аутентификация не требуется*)
```
api/v1/categories/
```
```
[
 {
   "count": 0,
   "next": "string",
   "previous": "string",
   "results": [
     {
        "name": "string",
        "slug": "string"
     }
   ]
 }
]
```
#### - Добавление нового отзыва(POST запрос)
(*требуется Аутентификация*)
```
api/v1/titles/{title_id}/reviews/
```
Payload:
```
{
    "text": "string",
    "score": 1
}
```
Response sample (status code = 201):
```
{
    "id": 0,
    "text": "string",
    "author": "string",
    "score": 1,
    "pub_date": "2019-08-24T14:15:22Z"
}
```
#### - Добавление новой категории(POST запрос)
(*требуются права Администратора*)
```
api/v1/categories/
```
Payload:
```
{
    "name": "string",
    "slug": "string"
}
```
Response sample (status code = 201):
```
{
    "name": "string",
    "slug": "string"
}
```
### Документация:
Доступна по адресу http://localhost/redoc/
### Используемые технологии:
- [Python 3.7.9](https://www.python.org/)
- [Django 2.2.19](https://www.djangoproject.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
- [Nginx](https://nginx.org/ru/)
- [Gunicorn](https://gunicorn.org/)
### Авторы:
- Иван Конышкин
- Дамир Матюхин
- Николай Гусев
