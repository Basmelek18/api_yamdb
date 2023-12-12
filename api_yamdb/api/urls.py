from rest_framework.routers import SimpleRouter

from .views import ReviewViewSet


router = SimpleRouter()

router.register(
    r'titles/(?P<post_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
