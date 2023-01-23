from django.db import models
from users.models import User


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название категории',
        unique=True, max_length=256
    )
    slug = models.SlugField(
        verbose_name='Адрес в URL - category/',
        unique=True, max_length=50
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Адрес в URL - genres/',
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=256
    )
    year = models.PositiveIntegerField(
        verbose_name='Дата выхода произведения',
        db_index=True
    )
    description = models.CharField(
        verbose_name='Описание произведения',
        max_length=1000, null=True
    )
    genre = models.ManyToManyField(
        Genre, related_name='titles',
        verbose_name='Жанры произведения'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', blank=True, null=True,
        verbose_name='Категория произведения'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField(verbose_name='Текст отзыва')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews', verbose_name='Название фильма')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews', verbose_name='Автор отзыва')
    score = models.PositiveIntegerField(verbose_name='Рейтинг')
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name='Дата публикации')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'), name='unique_object')]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments', verbose_name='Автор комментария')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments', verbose_name='id отзыва')
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
