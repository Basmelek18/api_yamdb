from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (
    CategoryViewSet,
    ReviewViewSet,
    CommentViewSet,
    SignUpView,
    VerifyCodeView
)


router_v1 = SimpleRouter()


router_v1.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)

router_v1.register(
    r'titles/(?P<post_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)

router_v1.register(
    r'titles/(?P<post_id>\d+)/reviews/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', VerifyCodeView.as_view(), name='verify'),
]
