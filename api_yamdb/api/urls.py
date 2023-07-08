from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (UserViewSet,
                       get_token, 
                       sign_up,
                       ReviewViewSet,
                       CommentViewSet)

v1_router = DefaultRouter()
v1_router.register(
    r'title/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews')
v1_router.register(
    r'title/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')
v1_router.register('users', UserViewSet)


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', sign_up, name='signup'),
    path('v1/auth/token/', get_token, name='token'),
]
