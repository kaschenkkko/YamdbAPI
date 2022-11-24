from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrOwnerPermission(BasePermission):
    """Уровень доступа:
    Аноним: Не может совершать действия с эндпоинтом
    Авторизованный пользователь: Не может совершать действия со всеми
    материалами
    Автор: Может редактировать и удалять свои материалы
    Модератор: Не может совершать действия с эндпоинтом
    Админ: Может редактировать и удалять все материалы."""
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin
                or request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return (obj.username == request.user.username
                or request.user.is_admin
                or request.user.is_staff)


class IsModeratorOrAdminOrOwnerOrReadonlyPermission(BasePermission):
    """Уровень доступа:
    Аноним: Может просматривать материалы
    Авторизованный пользователь: Может постить
    Автор: Может редактировать и удалять свои материалы
    Модератор: Может редактировать и удалять все материалы
    Админ: Может редактировать и удалять все материалы."""
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
    """Уровень доступа:
    Аноним: Может просматривать материалы
    Авторизованный пользователь: Может просматривать материалы
    Автор: Может просматривать материалы
    Модератор: Может просматривать материалы
    Админ: Может просматривать материалы."""
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                and request.user.is_admin
                or request.user.is_staff)
