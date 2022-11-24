from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role', 'bio', 'first_name',
                    'last_name',)
    search_fields = ('username', 'email', 'first_name', 'last_name',)
    empty_value_display = '-пусто-'
