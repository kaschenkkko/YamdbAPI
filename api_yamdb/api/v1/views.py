from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title
from users.models import User

from .filters import FilterTitle
from .mixins import CreateListDestroytViewSet
from .permissions import (IsAdminOrOwnerPermission,
                          IsAdminOrReadonlyPermission,
                          IsModeratorOrAdminOrOwnerOrReadonlyPermission)
from .serializers import (CategorySerializer, CommentSerializer,
                          ConfirmationCodeSerializer, GenreSerializer,
                          ReviewSerializer, SignUpSerializer,
                          TitleSerializerGet, TitleSerializerPost,
                          UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrOwnerPermission]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    lookup_field = 'username'

    @action(methods=['GET', 'PATCH'], detail=False,
            permission_classes=[IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        else:
            serializer = UserSerializer(request.user, data=request.data,
                                        partial=True)
            serializer.is_valid(raise_exception=True)
            if request.user.is_admin:
                serializer.save()
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)


class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers)

    def perform_create(self, serializer):
        try:
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            user, _ = User.objects.get_or_create(
                username=username,
                email=email,
            )
            user.confirmation_code = default_token_generator.make_token(user)
        except IntegrityError:
            return Response('Что-то пошло не так, проверьте введенные данные.',
                            status=status.HTTP_400_BAD_REQUEST)
        return send_mail(subject='Ваш код подтверждения для авторизации',
                         message=(
                             'Отправьте этот код подтверждения для '
                             f'получения токена: {user.confirmation_code}.'),
                         from_email='from@example.com',
                         recipient_list=[email])


@api_view(["POST"])
@permission_classes([AllowAny])
def get_token(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    if default_token_generator.check_token(
        user, serializer.validated_data.get("confirmation_code")
    ):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsModeratorOrAdminOrOwnerOrReadonlyPermission]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def get_serializer_context(self):
        context = super(ReviewViewSet, self).get_serializer_context()
        context.update(
            {'author': self.request.user,
             'title_id': self.kwargs.get('title_id'),
             'method': self.request.method})
        return context


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsModeratorOrAdminOrOwnerOrReadonlyPermission]
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs['review_id'],
            title__id=self.kwargs['title_id']
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs['review_id'],
            title__id=self.kwargs['title_id']
        )
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(CreateListDestroytViewSet):
    permission_classes = [IsAdminOrReadonlyPermission]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroytViewSet):
    permission_classes = [IsAdminOrReadonlyPermission]
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadonlyPermission]
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('category', 'genre', 'name', 'year')
    filterset_class = FilterTitle

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return TitleSerializerGet
        return TitleSerializerPost
