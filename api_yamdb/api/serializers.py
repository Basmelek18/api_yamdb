from django.core.validators import RegexValidator, EmailValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.shortcuts import get_object_or_404

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import UserYamDb


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
    """Сериализатор для регистрации и отправки кода на email."""
    username = serializers.CharField(
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message=('Field should contain only letters, '
                         'digits, and @/./+/-/_ characters.'),
                code='invalid_characters',
            ),
        ],
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[
            EmailValidator(
                message='Enter a valid email address.'
            ),
        ]
    )

    def validate_username(self, value):
        if 'me' == value:
            raise serializers.ValidationError(
                "Вы не можете создать пользователя с именем me"
            )
        return value

    class Meta:
        model = UserYamDb
        fields = ('email', 'username',)


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с токеном JWT."""
    username = serializers.CharField(
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message=('Field should contain only letters, '
                         'digits, and @/./+/-/_ characters.'),
                code='invalid_characters',
            ),
        ],
    )
    confirmation_code = serializers.IntegerField()

    class Meta:
        model = UserYamDb
        fields = (
            'username',
            'confirmation_code',
        )


class AdminUserYamDbSerializer(serializers.ModelSerializer):
  """Сериализатор для работы с моделью user."""
    username = serializers.CharField(
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message=('Field should contain only letters, '
                         'digits, and @/./+/-/_ characters.'),
                code='invalid_characters',
            ),
            UniqueValidator(
                queryset=UserYamDb.objects.all(),
                message='Пользователь с таким username уже существует',
            )
        ],
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[
            UniqueValidator(
                queryset=UserYamDb.objects.all(),
                message='Пользователь с таким email уже существует',
            )
        ]
    )

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


class UserYamDbSerializer(AdminUserYamDbSerializer):
    role = serializers.StringRelatedField()
