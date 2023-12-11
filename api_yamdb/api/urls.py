from rest_framework.routers import SimpleRouter

from .views import ReviewViewSet


router = SimpleRouter()

router.register(
    'title/<int:title_id>/reviews',
    ReviewViewSet,
    basename='reviews'
)
