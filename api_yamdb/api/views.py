import random

from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

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
    UserYamDbSerializer,
    ConfirmationCodeSerializer,
    TokenSerializer,
    AdminUserYamDbSerializer,
    AdminUserYamDbPatchSerializer
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
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
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


class SignUpView(APIView):
    """
    Получить код подтверждения на переданный email. Права доступа: Доступно без
    токена.
    """
    def post(self, request):
        serializer = ConfirmationCodeSerializer(data=request.data)
        username = request.data.get('username')
        email = request.data.get('email')
        code = ''.join(random.choice('0123456789') for _ in range(6))
        user = UserYamDb.objects.all()

        if serializer.is_valid():
            if user.filter(username=username):
                if user.get(username=username).email != email:
                    return Response(
                        {'username': ['Поле email не совпадает с пользователем']},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                user.filter(username=username).update(confirmation_code=code)
            else:
                if UserYamDb.objects.filter(email=email):
                    return Response(
                        {'email': ['данный пользователь не существует']},
                        status=status.HTTP_400_BAD_REQUEST)
                UserYamDb.objects.create(username=username,
                                         email=email, confirmation_code=code)
            send_mail(
                subject='Ваш код для входа в систему',
                message=f'{code}',
                from_email='from@example.com',
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
        try:
            user = UserYamDb.objects.get(username=data['username'])
        except UserYamDb.DoesNotExist:
            return Response(
                {'username': 'Пользователь не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        if str(data.get('confirmation_code')) == user.confirmation_code:
            token = AccessToken.for_user(user)
            return Response(
                {'token': str(token)},
                status=status.HTTP_200_OK
            )
        return Response(
            {'confirmation_code': 'Неверный код подтверждения'},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(viewsets.ModelViewSet):
    """
    Получение списка всех пользователей.
    Права доступа: Администратор.
    """
    queryset = UserYamDb.objects.all()
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
            serializer = UserYamDbSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserYamDbSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save(role=self.request.user.role, partial=True)

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return AdminUserYamDbPatchSerializer
        return AdminUserYamDbSerializer
