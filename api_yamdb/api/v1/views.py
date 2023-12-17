from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework import status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api.v1.filter import TitleFilters
from api.v1.mixins import CreateListDestroyMixin
from api.v1.permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsAuthorModeratorAdminOrReadOnly,
)
from api.v1.serializers import (
    CategorySerializer,
    CommentSerializer,
    ConfirmationCodeSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    TokenSerializer,
    UpdateUserYamDbSerializer,
    UserYamDbSerializer,
)
from reviews.models import Category, Genre, Review, Title
from users.models import UserYamDb


class CategoryViewSet(CreateListDestroyMixin):
    """
    Представление модели Category.
    Обрабатывает запросы GET, POST и DELETE с учетом прав доступа.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyMixin):
    """
    Представление модели Genre.
    Обрабатывает запросы GET, POST и DELETE с учетом прав доступа.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """
    Представление модели Title.
    Обрабатывает все запросы с учетом прав доступа.
    """
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly,)
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

    def get_title(self):
        return get_object_or_404(
            Title,
            pk=self.kwargs['title_id'],
        )

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Представление модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthorModeratorAdminOrReadOnly,
        IsAuthenticatedOrReadOnly
    )
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_review(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs['review_id'],
            title=self.kwargs['title_id']
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class SignUpView(APIView):
    """
    Получить код подтверждения на переданный email. Права доступа: Доступно без
    токена.
    """
    def post(self, request):
        serializer = ConfirmationCodeSerializer(data=request.data)
        username = request.data.get('username')
        email = request.data.get('email')
        user = UserYamDb.objects.all()
        if serializer.is_valid(raise_exception=True):
            username_from_data = UserYamDb.objects.filter(username=username).first()
            email_from_data = UserYamDb.objects.filter(email=email).first()
            if email_from_data != username_from_data:
                if username_from_data is None:
                    return Response(
                        {'email': ['Поле email не совпадает с username']},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                elif email_from_data is None:
                    return Response(
                        {'username': ['Поле username не совпадает с email']},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    return Response(
                        {
                            'username': ['Поле username не совпадает с email'],
                            'email': ['Поле email не совпадает с username']
                         },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            user, created = user.get_or_create(username=username, email=email)
            code = default_token_generator.make_token(user)
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
        if not default_token_generator.check_token(
                user,
                data.get('confirmation_code')
        ):
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
    serializer_class = UserYamDbSerializer
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
