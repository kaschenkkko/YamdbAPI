<div id="header" align="center">
  <h1>API Yamdb</h1>
  <img src="https://img.shields.io/badge/Python-3.7.9-brightgreen"/>
  <img src="https://img.shields.io/badge/Django-2.2.19-blueviolet"/>
  <img src="https://img.shields.io/badge/PostgreSQL-orange"/>
  <img src="https://img.shields.io/badge/Docker-red"/>
  <img src="https://img.shields.io/badge/Nginx-blue"/>
  <img src="https://img.shields.io/badge/Gunicorn-yellow"/>
</div>
<img src="https://github.com/clownvkkaschenko/YamdbAPI/actions/workflows/yamdb_workflow.yml/badge.svg"/>

Проект YaMDb собирает отзывы пользователей о фильмах, книгах и музыке. Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от 1 до 10, из пользовательских оценок формируется рейтинг.

Проект был разработан в команде из трёх разработчиков:
- **Иван Конышкин, Дамир Матюхин, Николай Гусев.**
### Запуск проекта:
Клонируйте репозиторий и перейти в корневую папку:
```
git clone git@github.com:clownvkkaschenko/YamdbAPI.git
```
Cоздайте файл .env в папке **infra** и заполните этот файл данными представленными ниже:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
DB_HOST=db
DB_PORT=5432
POSTGRES_PASSWORD=password
```
Из папки **infra** и запустите docker-compose:
```
~$ docker-compose up -d --build
```
В контейнере web выполните миграции, создайте суперпользователя и соберите статику:
```
~$ docker-compose exec web python manage.py migrate
~$ docker-compose exec web python manage.py createsuperuser
~$ docker-compose exec web python manage.py collectstatic --no-input
```
Загрузите подготовленые данные из fixture.json в БД:
```
~$ docker cp fixture.json <container_id>:app/
~$ docker-compose exec web python manage.py loaddata fixture.json
```
После этого проект будет доступен по url-адресу **localhost/api/v1/**

Документация к API доступна по url-адресу **localhost/redoc/**
