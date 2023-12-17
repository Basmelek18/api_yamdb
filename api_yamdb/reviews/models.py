from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

from reviews.validators import validate_year
from users.models import UserYamDb


class BaseModel(models.Model):
    """
    Абстрактная модель.
    Добавляет к модели название и slug.
    """
    name = models.CharField(
        verbose_name='Название',
        max_length=settings.LEN_TEXT,
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Genre(BaseModel):
    """Модуль жанры."""
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)


class Category(BaseModel):
    """Модель категорий."""
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)


class Title(models.Model):
    """Модель произведений"""
    name = models.CharField(
        verbose_name='Название',
        max_length=settings.LEN_TEXT,
    )
    year = models.SmallIntegerField(
        verbose_name='Год выпуска',
        validators=[validate_year],
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр',
        related_name='title_genre'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категории',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='title_category'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('year', 'name')

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Модель связи произведений и жанров"""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='title_genre'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genre_title'
    )

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    """Модель отзывов."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    text = models.CharField(
        max_length=200,
        verbose_name='Текст отзыва',
    )
    author = models.ForeignKey(
        UserYamDb,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
        verbose_name='Оценка',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментариев."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.CharField(
        max_length=200,
        verbose_name='Текст комментария',
    )
    author = models.ForeignKey(
        UserYamDb,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
