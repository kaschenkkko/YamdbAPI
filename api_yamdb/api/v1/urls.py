from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, SignUpViewSet, TitlesViewSet, UserViewSet,
                    get_token)

v1_router = DefaultRouter()

v1_router.register('users', UserViewSet, basename='users')
v1_router.register('titles', TitlesViewSet, basename='titles')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('categories', CategoryViewSet, basename='categories')

v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')

v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')

auth_patterns = [
    path('signup/', SignUpViewSet.as_view({'post': 'create'}), name='signup'),
    path('token/', get_token, name='token')
]

urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/', include(auth_patterns))
]
