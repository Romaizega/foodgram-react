from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from users.models import Follow, FoodUser

User = get_user_model

admin.site.site_header = 'Администратор сайта "Foodgram"'
admin.site.empty_value_display = 'Не выбрано'
admin.site.unregister(Group)


@admin.register(FoodUser)
class FoodUserAdmin(UserAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
    )
    list_editable = (
        'username',
        'email',
        'first_name',
        'last_name',)
    search_fields = (
        'username',
        'email',)
    list_filter = (
        'username',
        'email',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'following')
    list_filter = (
        'following',
        'user'
    )
    list_display_links = (
        'following',
        'user'
    )


admin.site.empty_value_display = 'Не задано'
