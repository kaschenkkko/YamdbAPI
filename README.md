<div id="header" align="center">
  <h1>API Yamdb</h1>
  <img src="https://img.shields.io/badge/Python-3.7.9-F8F8FF?style=for-the-badge&logo=python&logoColor=20B2AA">
  <img src="https://img.shields.io/badge/Django-2.2.19-F8F8FF?style=for-the-badge&logo=django&logoColor=00FF00">
  <img src="https://img.shields.io/badge/PostgreSQL-555555?style=for-the-badge&logo=postgresql&logoColor=F5F5DC">
  <img src="https://img.shields.io/badge/Docker-555555?style=for-the-badge&logo=docker&logoColor=2496ED">
  <img src="https://img.shields.io/badge/nginx-555555?style=for-the-badge&logo=nginx&logoColor=009639">
  <img src="https://img.shields.io/badge/gunicorn-555555?style=for-the-badge&logo=gunicorn&logoColor=499848">
  <a href="https://github.com/clownvkkaschenko/YamdbAPI/actions/workflows/yamdb_workflow.yml">
  <img src="https://img.shields.io/github/actions/workflow/status/clownvkkaschenko/YamdbAPI/yamdb_workflow.yml?branch=master&label=API Yamdb workflows&style=for-the-badge&color=F8F8FF&logo=githubactions&logoColor=2088FF"><a>
</div>


Проект YaMDb собирает отзывы пользователей о фильмах, книгах и музыке. Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от 1 до 10, из пользовательских оценок формируется рейтинг.

Проект был разработан в команде из трёх разработчиков:
- **Иван Конышкин, Дамир Матюхин, Николай Гусев.**
### Запуск проекта:
- Клонируйте репозиторий и перейдите в него 
  ```
  git clone git@github.com:clownvkkaschenko/YamdbAPI.git
  ```
- Cоздайте файл .env в папке **infra** и заполните этот файл данными представленными ниже
  ```
  DB_ENGINE=django.db.backends.postgresql
  DB_NAME=postgres
  POSTGRES_USER=postgres
  DB_HOST=db
  DB_PORT=5432
  POSTGRES_PASSWORD=password
  ```
- Из папки **infra** и запустите docker-compose
  ```
  ~$ docker-compose up -d --build
  ```
- В контейнере web выполните миграции, создайте суперпользователя и соберите статику
  ```
  ~$ docker-compose exec web python manage.py migrate
  ~$ docker-compose exec web python manage.py createsuperuser
  ~$ docker-compose exec web python manage.py collectstatic --no-input
  ```
- Загрузите подготовленые данные из fixture.json в БД
  ```
  ~$ docker cp fixture.json <container_id>:app/
  ~$ docker-compose exec web python manage.py loaddata fixture.json
  ```

После этого проект будет доступен по url-адресу **localhost/api/v1/**

Документация к API доступна по url-адресу **localhost/redoc/**
