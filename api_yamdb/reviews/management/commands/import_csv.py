import csv
from django.core.management.base import BaseCommand

from reviews.models import Category, Title, Review, Genre, Comment, GenreTitle
from users.models import UserYamDb


class Command(BaseCommand):
    def import_category(self):
        with open('static/data/category.csv', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Category.objects.create(
                    id=row['id'], name=row['name'], slug=row['slug']
                )

    def import_comments(self):
        with open('static/data/comments.csv', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Comment.objects.create(
                    id=row['id'],
                    review_id=row['review_id'],
                    text=row['text'],
                    author_id=row['author'],
                    pub_date=row['pub_date']
                )

    def import_genre(self):
        with open('static/data/genre.csv', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Genre.objects.create(
                    id=row['id'], name=row['name'], slug=row['slug']
                )

    def import_genre_title(self):
        with open('static/data/genre_title.csv', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                GenreTitle.objects.create(
                    id=row['id'], title_id=row['title_id'],
                    genre_id=row['genre_id']
                )

    def import_review(self):
        with open('static/data/review.csv', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Review.objects.create(
                    id=row['id'],
                    title_id=row['title_id'],
                    text=row['text'],
                    author_id=row['author'],
                    score=row['score'],
                    pub_date=row['pub_date']
                )

    def import_titles(self):
        with open('static/data/titles.csv', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Title.objects.create(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category_id=row['category']
                )

    def import_users(self):
        with open('static/data/users.csv', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                UserYamDb.objects.create(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name']
                )

    def handle(self, *args, **options):
        self.import_category()
        self.import_genre()
        self.import_titles()
        self.import_genre_title()
        self.import_users()
        self.import_review()
        self.import_comments()
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
