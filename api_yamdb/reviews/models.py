from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

from reviews.validators import validate_year
from users.models import UserYamDb


class BaseModel(models.Model):
    """
    Abstract model.
    Adds a name and slug to the model.
    """
    name = models.CharField(
        verbose_name='Title',
        max_length=settings.LEN_TEXT,
    )
    slug = models.SlugField(
        verbose_name='Slug',
        unique=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Genre(BaseModel):
    """Genres Module."""
    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'
        ordering = ('name',)


class Category(BaseModel):
    """Category model."""
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ('name',)


class Title(models.Model):
    """A model of the works"""
    name = models.CharField(
        verbose_name='Title',
        max_length=settings.LEN_TEXT,
    )
    year = models.SmallIntegerField(
        verbose_name='Year of release',
        validators=[validate_year],
    )
    description = models.TextField(
        verbose_name='Description',
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Genre',
        related_name='title_genre'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Categories',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='title_category'
    )

    class Meta:
        verbose_name = 'Work'
        verbose_name_plural = 'Works'
        ordering = ('year', 'name')

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """A model of the relationship between works and genres"""
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
    """Model Reviews."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Work',
    )
    text = models.TextField(
        verbose_name='Text of feedback',
    )
    author = models.ForeignKey(
        UserYamDb,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Author',
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                settings.SCORE_MIN,
                message=f'The grade cannot be lower than {settings.SCORE_MIN}'
            ),
            MaxValueValidator(
                settings.SCORE_MAX,
                message=f'The grade cant be higher {settings.SCORE_MAX}'
            )
        ],
        verbose_name='Grade',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Publication date',
    )

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Comment Model."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Review',
    )
    text = models.TextField(
        verbose_name='Comment text',
    )
    author = models.ForeignKey(
        UserYamDb,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Author',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Publication date',
    )

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.text
