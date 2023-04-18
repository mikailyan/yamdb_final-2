import csv

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Genre_Title, Review, Title
from users.models import User

FILESPATH = {
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Genre_Title: 'genre_title.csv',
    User: 'users.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}


class Command(BaseCommand):

    def handle(self, *args, **options):
        for key, value in FILESPATH.items():
            with open(f'static/data/{value}', 'r', encoding='utf-8-sig',
                      newline='') as f:
                reader = csv.DictReader(f)
                key.objects.bulk_create(key(**kwargs) for kwargs in reader)

            self.stdout.write(self.style.SUCCESS(f'Данные модели '
                                                 f'{key.__name__}'
                                                 f' импортированы успешно!'))
