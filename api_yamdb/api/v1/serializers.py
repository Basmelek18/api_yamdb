from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.validators import validate_username
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import UserYamDb


class CategorySerializer(serializers.ModelSerializer):
    """A serializer for the Category model."""
    class Meta:
        exclude = ('id',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for the Genre model."""
    class Meta:
        exclude = ('id',)
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    """
    Serializer for the Title model.
    For read operations only.
    """
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )


class TitleWriteSerializer(serializers.ModelSerializer):
    """
    Serializer for the Title model.
    For write operations only.
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
        fields = (
            'name', 'year', 'description', 'genre', 'category'
        )

    def to_representation(self, title):
        serializer = TitleReadSerializer(title)
        return serializer.data


class ReviewSerializer(serializers.ModelSerializer):
    """A serializer for the Review model."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)

    def validate(self, data):
        """
        Checks to see if the author of the POST request has already written
        has written a review of this work before.
        """
        request = self.context['request']
        if request.method != 'POST':
            return data
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        if Review.objects.filter(
            author=request.user, title=title
        ).exists():
            raise serializers.ValidationError(
                'You can only leave one review!'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """A serializer for the Comment model."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)


class ConfirmationCodeSerializer(serializers.Serializer):
    """Serializer to register and send code to email."""
    username = serializers.CharField(
        max_length=settings.MAX_LENGTH_USERNAME,
        validators=[
            UnicodeUsernameValidator(),
            validate_username,
        ],
    )
    email = serializers.EmailField(max_length=settings.MAX_LENGTH_EMAIL,)

    class Meta:
        model = UserYamDb
        fields = ('email', 'username',)


class TokenSerializer(serializers.Serializer):
    """Serializer for working with JWT token."""
    username = serializers.CharField(
        max_length=settings.MAX_LENGTH_USERNAME,
        validators=[
            UnicodeUsernameValidator(),
            validate_username
        ],
    )
    confirmation_code = serializers.CharField()

    class Meta:
        model = UserYamDb
        fields = (
            'username',
            'confirmation_code',
        )


class UserYamDbSerializer(serializers.ModelSerializer):
    """Serializer for working with the user model."""
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
