from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.v1.views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    SignUpView,
    TitleViewSet,
    UserViewSet,
    VerifyCodeView,
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
    'titles',
    TitleViewSet,
    basename='titles'
)
router_v1.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
router_v1.register(
    'users',
    UserViewSet,
    basename='users'
)

auth_urls = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('token/', VerifyCodeView.as_view(), name='token'),
]


urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include(auth_urls)),
]
