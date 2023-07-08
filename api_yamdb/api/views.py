import uuid
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.filters import SearchFilter
from rest_framework import viewsets, filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers import (ReviewSerializer,
                          CommentSerializer,
                          UserSerializer,
                          GetTokenSerializer,
                          ProfileSerializer,
                          SignUpSerializer,
                          ProfileSerializer)
from api_yamdb.settings import DEFAULT_FROM_EMAIL, DEFAULT_EMAIL_SUBJECT
from reviews.models import User, Title
from api.permission import IsAdmin
from api.paginations import ReviewPagination, CommentPagination
 

class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки отзывов к произведениям"""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    pagination_class = CommentPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter)
    filters_field = ('author', )
    search_fields = ('author', )
    ordering_fields = ('pub_date', )

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = title.reviews.get(id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = title.reviews.get(id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки комментариев к отзывам"""
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    pagination_class = ReviewPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter)
    filters_field = ('score',)
    search_fields = ('score', 'author', 'title')
    ordering_fields = ('pub_date', 'score')

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all().order_by('id')

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

 
class UserViewSet(ModelViewSet):
    """Вьюсет для модели пользователя."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin, )
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username', 'email')

    @action(
        methods=('get', 'patch'),
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,),
        serializer_class=ProfileSerializer
    )
    def set_profile(self, request, id=None):
        """Изменяет данные в профайле пользователя."""
        user = get_object_or_404(User, id=request.user.id)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def sign_up(request):
    """Регистрирует пользователя и отправляет код подтверждения."""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    confirmation_code = str(uuid.uuid4())
    user, created = User.objects.get_or_create(
        **serializer.validated_data,
        confirmation_code=confirmation_code
    )
    send_mail(
        subject=DEFAULT_EMAIL_SUBJECT,
        message=user.confirmation_code,
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=(user.email,)
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def get_token(request):
    """"Выдает токен для авторизации."""
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']
    user = get_object_or_404(User, username=username)
    if confirmation_code != user.confirmation_code:
        return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
    return Response({'token': str(AccessToken.for_user(user))},
                    status=status.HTTP_200_OK)
