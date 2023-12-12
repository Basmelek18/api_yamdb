from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import (
    ReviewViewSet,
    CommentViewSet,
    SignUpView
)


router_v1 = SimpleRouter()

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
    path('v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
