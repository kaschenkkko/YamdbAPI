import csv
import logging
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

models = {
    'category.csv': Category,
    'genre.csv': Genre,
    'titles.csv': Title,
    'users.csv': User,
    'review.csv': Review,
    'comments.csv': Comment
}


class Command(BaseCommand):
    help = 'Загружаем данные в бд из csv'

    def handle(self, *args, **options):
        for csv_key, model in models.items():
            file = os.path.join(settings.BASE_DIR, f"static/data/{csv_key}")
            with open(file, encoding='utf-8') as f:
                reader = csv.DictReader(f)
                try:
                    for row in reader:
                        model.objects.create(**row)
                except IntegrityError:
                    logging.warning('Данные уже загружены')
                    break
            logging.info(f'Данные из файла {csv_key} успешно загружены')
