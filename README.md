# Api_Yamdb
![](https://github.com/clownvkkaschenko/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
### Описание проекта:
Проект Api\_Yamdb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий может быть расширен администратором. Сами произведения в Api\_Yamdb не хранятся, здесь нельзя посмотреть фильм или послушать музыку. Произведению может быть присвоен жанр из списка предустановленных. Новые жанры может создавать только администратор. Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти; из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. На одно произведение пользователь может оставить только один отзыв.
Для удобного запуска на любой локальной машине проект Api_Yamdb представлен в контейнере Docker.
### Запуск приложения на локальном компьютере:
Клонируйте репозиторий и перейти в корневую папку:
```
$ git clone git@github.com:clownvkkaschenko/yamdb_final.git
```
Cоздайте файл .env в папке infra:
```
$ touch infra/.env
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
### Теперь проект доступен по адресу:
http://localhost/
### Остановка и запуск docker-compose:
```
~$ docker-compose stop
```
```
~$ docker-compose start
```
### Загрузка данных из fixture.json в бд:
```
~$ docker-compose exec web python manage.py loaddata fixture.json
```
### Загрузка данных из csv файлов в бд:
```
~$ docker-compose exec web python manage.py load_csv
```
### Запуск проекта на сервере:
- Войдите на свой удаленный сервер в облаке
- Остановите службу nginx:
    ```
    sudo systemctl stop nginx
    ```
- Установите docker:
    ```
    sudo apt install docker.io
    ```
- Установите docker-compose, с этим вам поможет [официальная документация](https://docs.docker.com/compose/install/)
- Скопируйте файлы docker-compose.yaml и nginx/default.conf из вашего проекта на сервер в _home/<ваш_username>/docker-compose.yaml_ и _home/<ваш_username>/nginx/default.conf_ соответственно
- Добавьте в Secrets GitHub Actions переменные окружения для работы базы данных
- Выполните эти команды, после чего проект будет работать на вашем сервере
    ```
    ~$ sudo docker-compose up -d --build
    ~$ sudo docker-compose exec web python manage.py migrate
    ~$ sudo docker-compose exec web python manage.py createsuperuser
    ~$ sudo docker-compose exec web python manage.py collectstatic --no-input
    ```
### GitHub Actions:
Для запуска инструкций workflow добавьте в Secrets GitHub Actions переменные окружения. Имя переменных можно посмотреть в файле yamdb_workflow.yml. После этого, при пуше проекта, GitHub будет автоматически запускать тесты:
- проверки кода на соответствие стандарту PEP8 (с помощью пакета flake8) и запускать pytest из репозитория yamdb_final
- сборки и доставки докер-образа для контейнера web на Docker Hub
- автоматического деплоя проекта на боевой сервер

При успешном завершении тестирования произойдёт отправка уведомления в Telegram о том, что процесс деплоя успешно завершился.
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
### Проект доступен по адресу:
##### 84.201.177.80
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
