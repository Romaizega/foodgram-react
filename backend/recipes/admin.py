from django.contrib import admin
from django.contrib.admin import display
from django.utils.html import format_html

from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)


class TagAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'color',
        'slug'
    )
    search_fields = (
        'name',
        'slug'
    )
    list_filter = (
        'name',
        'slug'
    )
    prepopulated_fields = {'slug': ('name',)}
    list_display_links = ('name',)
    ordering = ('name',)


class IngredientAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'measurement_unit'
    )
    list_display_links = ('name',)
    search_fields = ('name',)


class IngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 2


class RecipeAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'author',
        'name',
        'image_display',
        'text',
        'cooking_time',
        'total_in_favorites',
        'pub_date',
    )
    filter_horizontal = ('tags',)
    inlines = (IngredientInline,)
    list_display_links = (
        'name',
        'author')
    list_filter = (
        'name',
        'author',
        'tags')

    @display(description='Изображение')
    def image_display(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" height="50px" />')
        return 'Нет фото'

    @display(description='В избранном')
    def total_in_favorites(self, obj):
        return Favorite.objects.filter(recipe=obj).count()


class RecipeIngredientAdmin(admin.ModelAdmin):

    list_display = (
        'recipe',
        'ingredient',
        'amount'
    )


class FavoriteAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'recipe'
    )
    list_display_links = ('user',)


class ShoppingCartAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'recipe'
    )

    list_display_links = ('user',)


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Favorite, FavoriteAdmin)
