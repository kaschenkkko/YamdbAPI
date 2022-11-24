from django.core.validators import MaxValueValidator
from django.utils import timezone
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class SignUpSerializer(serializers.ModelSerializer):

    def validate(self, data):
        username = data['username']
        email = data['email']
        if username == 'me':
            raise serializers.ValidationError(
                'Использовать имя me в '
                'качестве username запрещено.')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'Такой username уже занят, надо придумать другой.'
            )
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже зарегистрирован.'
            )
        return data

    class Meta:
        model = User
        fields = ('username', 'email')


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username', read_only=True)

    def validate(self, attrs):
        if self.context['method'] != 'POST':
            return attrs
        title_id = self.context['title_id']
        author = self.context['author']
        if Review.objects.filter(author=author, title_id=title_id):
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на это произведение')
        return attrs

    def validate_score(self, score):
        if score < 0 or score > 10:
            return serializers.ValidationError('От 1 до 10')
        return score

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializerGet(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(default=0, read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializerPost(serializers.ModelSerializer):
    category = SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all())
    genre = SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True)
    year = serializers.IntegerField(
        validators=[MaxValueValidator(timezone.now().year)])

    class Meta:
        model = Title
        fields = '__all__'
