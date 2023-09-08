from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'username',
        'first_name',
        'last_name'
    )
    search_fields = ('id', r'^username', r'^email')
    empty_value_display = '-пусто-'
