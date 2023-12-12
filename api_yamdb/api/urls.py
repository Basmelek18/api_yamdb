from django.urls import path, include
from rest_framework.routers import SimpleRouter


from .views import ReviewViewSet, SignupView, TokenTakenView


router_v1 = SimpleRouter()

router_v1.register(
    r'titles/(?P<post_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', SignupView.as_view(), name='token_obtain_pair'),
    path('v1/auth/token/', TokenTakenView.as_view(), name='token_refresh'),
]