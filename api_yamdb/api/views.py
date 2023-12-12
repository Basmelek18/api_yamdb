import random

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, pagination
from rest_framework.views import APIView

from reviews.models import Title, Review
from .serializers import ReviewSerializer, CommentSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = ()

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
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = ()

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
        user = request.user
        code = ''.join(random.choice('0123456789') for _ in range(6))
        ConfirmationCode.objects.create(user=user, code=code)

        # Здесь также отправьте код на почту, используя, например, Django EmailBackend

        return Response({'message': 'Code generated successfully'}, status=status.HTTP_201_CREATED)

class VerifyCodeView(APIView):
    def post(self, request):
        user = request.user
        code = request.data.get('code')

        confirmation_code = get_object_or_404(ConfirmationCode, user=user, code=code)
        confirmation_code.delete()  # Удалите код после его использования

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({'access_token': access_token})