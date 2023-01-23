from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    ROLES = [
        (USER, 'user'),
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator')
    ]
    username_validator = AbstractUser.username_validator
    username = models.CharField(
        verbose_name='username', max_length=150,
        unique=True, validators=[username_validator],
        help_text=('Обязательное поле. Может быть '
                   'не длиннее 150 знаков.')
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=254, blank=False, unique=True
    )
    role = models.CharField(
        verbose_name='Уровень доступа',
        choices=ROLES, max_length=50, default=USER
    )
    bio = models.TextField(verbose_name='О себе', blank=True)
    first_name = models.CharField(
        verbose_name='Имя', max_length=150, blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия', max_length=150, blank=True
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=150, blank=True, null=True
    )

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_user(self):
        return self.role == 'user'

    def __str__(self):
        return self.username

    class Meta:
        verbose_name: str = 'Пользователь'
        verbose_name_plural: str = 'Пользователи'
