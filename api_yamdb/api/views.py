from django_filters.rest_framework import DjangoFilterBackend
import random

from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets, pagination, status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .filter import TitleFilters
from .permissions import IsAuthorModeratorAdminOrReadOnly, IsAdmin, ReadOnly
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
)
from .mixins import CreateListDestroyMixin
from users.models import UserYamDb


class CategoryViewSet(CreateListDestroyMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = (IsAdmin | ReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = (IsAdmin | ReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    permission_classes = (IsAdmin | ReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilters

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = (
        IsAuthorModeratorAdminOrReadOnly,
        IsAuthenticatedOrReadOnly
    )

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'),
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'),
        )
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = (
        IsAuthorModeratorAdminOrReadOnly,
        IsAuthenticatedOrReadOnly
    )

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
        )
        serializer.save(author=self.request.user, review=review)


class SignUpView(APIView):
    def post(self, request):
        serializer = ConfirmationCodeSerializer(data=request.data)
        username = request.data.get('username')
        email = request.data.get('email')
        code = ''.join(random.choice('0123456789') for _ in range(6))
        UserYamDb.objects.create(username=username, email=email, confirmation_code=code)
        send_mail(
            subject='Ваш код для входа в систему',
            message=f'{code}',
            from_email='from@example.com',
            recipient_list=[f'{email}'],
            fail_silently=True,
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeView(APIView):
    def post(self, request):
        serializer = ConfirmationCodeSerializer
        user = request.user
        username = request.request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')

        confirmation_code = get_object_or_404(UserYamDb, username=username, confirmation_code=confirmation_code)
        confirmation_code.delete()

        refresh = RefreshToken.for_user(user)
        token = str(refresh.token)

        return Response(serializer.data)


class UserMeView(APIView):
    def get(self, request):
        users = UserYamDb.objects.all()
        serializer = UserYamDbSerializer(users, many=True)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserYamDbSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserYamDb.objects.all()
    serializer_class = UserYamDbSerializer
    pagination_class = pagination.LimitOffsetPagination
    search_fields = ('username',)

    @action(
        methods=['GET'],
        detail=False,
        url_path='me',
    )
    def get_current_user_info(self, request):
        serializer = UserYamDbSerializer(request.user)
        return Response(serializer.data)

    @action(
        methods=['PATCH'],
        detail=False,
        url_path='me',
    )
    def get_current_user_info(self, request):
        serializer = UserYamDbSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
