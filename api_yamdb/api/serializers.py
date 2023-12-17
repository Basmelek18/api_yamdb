from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from django.shortcuts import get_object_or_404

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import UserYamDb
from api.validators import validate_username


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""
    class Meta:
        exclude = ('id',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""
    class Meta:
        exclude = ('id',)
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Title.
    Только для операций чтения.
    """
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = '__all__'


class TitleWriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Title.
    Только для операций записи.
    """
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
    """Сериализатор для модели Review."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)

    def validate(self, data):
        """
        Проверяет не писал ли уже автор POST запроса
        отзыв на это произведение раньше.
        """
        title_id = self.context['view'].kwargs.get('title_id')
        request = self.context['request']
        title = get_object_or_404(Title, id=title_id)
        if request.method == 'POST':
            if Review.objects.filter(
                author=request.user, title=title
            ).exists():
                raise serializers.ValidationError(
                    'Можно оставить только один отзыв!'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)


class ConfirmationCodeSerializer(serializers.Serializer):
    """Сериализатор для регистрации и отправки кода на email."""
    username = serializers.CharField(
        max_length=settings.MAX_LENGTH_USERNAME,
        validators=[
            UnicodeUsernameValidator(),
            validate_username,
        ],
    )
    email = serializers.EmailField(
        max_length=settings.MAX_LENGTH_EMAIL,

    )

    class Meta:
        model = UserYamDb
        fields = ('email', 'username',)


class TokenSerializer(serializers.Serializer):
    """Сериализатор для работы с токеном JWT."""
    username = serializers.CharField(
        max_length=settings.MAX_LENGTH_USERNAME,
        validators=[
            UnicodeUsernameValidator(),
            validate_username
        ],
    )
    confirmation_code = serializers.IntegerField()

    class Meta:
        model = UserYamDb
        fields = (
            'username',
            'confirmation_code',
        )


class UserYamDbSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с моделью user."""
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


class UpdateUserYamDbSerializer(UserYamDbSerializer):
    role = serializers.CharField(read_only=True)
