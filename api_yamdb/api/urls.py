from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    ReviewViewSet,
    CommentViewSet,
    SignUpView,
    VerifyCodeView,
    TitleViewSet,
    GenreViewSet,
    UserViewSet,
)


router_v1 = DefaultRouter()


router_v1.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)
router_v1.register(
    r'titles',
    TitleViewSet,
    basename='titles'
)
router_v1.register(
    r'genres',
    GenreViewSet,
    basename='genres'
)
router_v1.register(
    'users',
    UserViewSet,
    basename='users'
)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', VerifyCodeView.as_view(), name='verify'),
]
