from django.core.validators import RegexValidator, EmailValidator
from rest_framework import serializers, validators
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import UserYamDb


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date',)
        # validators = [
        #     validators.UniqueTogetherValidator(
        #         queryset=Review.objects.all(),
        #         fields=('title', 'author'),
        #         message=(
        #             'Валидация на уникальность данных не пройдена: '
        #             f'запись с полями {fields} уже существует. Пользователь '
        #             'может оставить только один отзыв на произведение!'
        #         )
        #     )
        # ]


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'review', 'text', 'author', 'pub_date',)


class ConfirmationCodeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Field should contain only letters, digits, and @/./+/-/_ characters.',
                code='invalid_characters',
            ),
        ],
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[
            EmailValidator(
                message='Enter a valid email address.'
            )
        ]
    )

    class Meta:
        model = UserYamDb
        fields = ('email', 'username',)
        validators = [
            UniqueTogetherValidator(
                queryset=UserYamDb.objects.all(),
                fields=('email', 'username',),
            )
        ]


class UserYamDbSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Field should contain only letters, digits, and @/./+/-/_ characters.',
                code='invalid_characters',
            ),
        ],
    )
    email = serializers.EmailField(max_length=254,)
    first_name = serializers.CharField(max_length=150, )
    last_name = serializers.CharField(max_length=150, )

    class Meta:
        model = UserYamDb
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=UserYamDb.objects.all(),
                fields=('username', 'email'),
            )
        ]
