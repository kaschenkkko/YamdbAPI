from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrOwnerPermission(BasePermission):
    """Уровни доступа:

    - Аноним: не может совершать действия с эндпоинтом.
    - Авторизованный пользователь: не может совершать действия со всеми
      материалами.
    - Автор: может редактировать и удалять свои материалы.
    - Модератор: не может совершать действия с эндпоинтом.
    - Админ: может редактировать и удалять все материалы.
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin
                or request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return (obj.username == request.user.username
                or request.user.is_admin
                or request.user.is_staff)


class IsModeratorOrAdminOrOwnerOrReadonlyPermission(BasePermission):
    """Уровни доступа:

    - Аноним: может просматривать материалы.
    - Авторизованный пользователь: может постить.
    - Автор: может редактировать и удалять свои материалы.
    - Админ, Модератор: может редактировать и удалять все материалы.
    """
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                and (obj.author == request.user
                     or request.user.is_admin
                     or request.user.is_staff
                     or request.user.is_moderator))


class IsAdminOrReadonlyPermission(BasePermission):
    """Уровни доступа:

    - Аноним: может просматривать материалы
    - Авторизованный пользователь: может просматривать материалы
    - Автор: может просматривать материалы
    - Модератор: может просматривать материалы
    - Админ: может просматривать материалы.
    """
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                and request.user.is_admin
                or request.user.is_staff)
