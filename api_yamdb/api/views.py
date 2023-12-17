from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .filter import TitleFilters
from .permissions import (
    IsAuthorModeratorAdminOrReadOnly,
    IsAdmin,
    ReadOnly,
)
from reviews.models import Category, Title, Review, Genre
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    CategorySerializer,
    GenreSerializer,
    UpdateUserYamDbSerializer,
    ConfirmationCodeSerializer,
    TokenSerializer,
    UserYamDbSerializer,
)
from .mixins import CreateListDestroyMixin
from users.models import UserYamDb


class CategoryViewSet(CreateListDestroyMixin):
    """
    Представление модели Category.
    Обрабатывает запросы GET, POST и DELETE с учетом прав доступа.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdmin | ReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyMixin):
    """
    Представление модели Genre.
    Обрабатывает запросы GET, POST и DELETE с учетом прав доступа.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdmin | ReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """
    Представление модели Title.
    Обрабатывает все запросы с учетом прав доступа.
    """
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdmin | ReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilters
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление модели Review."""
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthorModeratorAdminOrReadOnly,
    )
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            pk=self.kwargs['title_id'],
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            pk=self.kwargs['title_id'],
        )
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Представление модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthorModeratorAdminOrReadOnly,
        IsAuthenticatedOrReadOnly
    )
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs['review_id'],
            title=self.kwargs['title_id']
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs['review_id'],
            title=self.kwargs['title_id']
        )
        serializer.save(author=self.request.user, review=review)

    def perform_update(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs['review_id'],
            title=self.kwargs['title_id']
        )
        serializer.save(
            author=self.request.user,
            review=review,
            role=self.request.user.role,
            partial=True
        )


class SignUpView(APIView):
    """
    Получить код подтверждения на переданный email. Права доступа: Доступно без
    токена.
    """
    def post(self, request):
        serializer = ConfirmationCodeSerializer(data=request.data)
        username = request.data.get('username')
        email = request.data.get('email')
        user = get_object_or_404(UserYamDb, username=username)
        code = default_token_generator.make_token(user)

        if serializer.is_valid(raise_exception=True):
            UserYamDb.objects.get_or_create(username=username, email=email)
            send_mail(
                subject='Ваш код для входа в систему',
                message=code,
                from_email=settings.FROM_EMAIL,
                recipient_list=[f'{email}'],
                fail_silently=True,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeView(APIView):
    """
    Получение JWT-токена в обмен на username и confirmation code.
    """
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(UserYamDb, username=data['username'])
        if not default_token_generator.check_token(user, data.get('confirmation_code')):
            return Response(
                {'confirmation_code': 'Неверный код подтверждения'},
                status=status.HTTP_400_BAD_REQUEST
            )
        token = AccessToken.for_user(user)
        return Response(
            {'token': str(token)},
            status=status.HTTP_200_OK
        )


class UserViewSet(viewsets.ModelViewSet):
    """
    Получение списка всех пользователей.
    Права доступа: Администратор.
    """
    queryset = UserYamDb.objects.all()
    serializer = UserYamDbSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete')

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,)
    )
    def get_current_user_info(self, request):
        if request.method == 'GET':
            serializer = UpdateUserYamDbSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UpdateUserYamDbSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
