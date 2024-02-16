from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from recipes.constant import (COOK_TIME_MAX, COOK_TIME_MIN,
                              MAX_AMOUNT_OF_INGREDIENT, MAX_CHAR_FIELD_LENGTH,
                              MIN_AMOUNT_OF_INGREDIENT)

User = get_user_model()


class Tag(models.Model):
    """Модель тегов."""

    name = models.CharField(
        max_length=MAX_CHAR_FIELD_LENGTH,
        unique=True,
        verbose_name='Название тега'
    )
    color = ColorField(
        max_length=7,
        unique=True,
        default='#000000',
        format='hex',
        verbose_name='Цвет тега HEX'
    )
    slug = models.SlugField(
        max_length=MAX_CHAR_FIELD_LENGTH,
        unique=True,
        verbose_name='Идентификатор'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиентов."""

    name = models.CharField(
        max_length=MAX_CHAR_FIELD_LENGTH,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=MAX_CHAR_FIELD_LENGTH,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)
        constraints = (
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_name_measurement_unit'
            ),
        )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    name = models.CharField(
        max_length=MAX_CHAR_FIELD_LENGTH,
        verbose_name='Название рецепта',
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Фото готового блюда',
        blank=True,
        null=True
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        through='RecipeIngredient'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (мин.)',
        validators=[
            MinValueValidator(COOK_TIME_MIN),
            MaxValueValidator(COOK_TIME_MAX)],
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    @receiver(pre_delete, sender='recipes.Recipe')
    def delete_recipe_images(sender, instance, **kwargs):
        """Удаляет изображение рецепта вместе с рецептом."""
        if instance.image:
            instance.image.delete(False)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Промежуточная модель ингредиентов."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(MIN_AMOUNT_OF_INGREDIENT),
            MaxValueValidator(MAX_AMOUNT_OF_INGREDIENT)]
    )

    class Meta:
        verbose_name = 'Ингредиент для рецепта'
        verbose_name_plural = 'Ингредиенты в рецептах'
        default_related_name = 'recipe_ingredient'
        constraints = (
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            ),
        )

    def __str__(self):
        return f'{self.ingredient}, {self.amount}'


class FavoriteShoppingCartBaseModel(models.Model):
    """Базовая модель избранного и списка покупок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        abstract = True
        ordering = ('user',)


class Favorite(FavoriteShoppingCartBaseModel):
    """Модель избранного."""

    class Meta(FavoriteShoppingCartBaseModel.Meta):
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        default_related_name = 'recipefavorite'
        constraints = (
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe_in_favorite'
            ),
        )

    def __str__(self):
        return self.user


class ShoppingCart(FavoriteShoppingCartBaseModel):
    """Модель списка покупок."""

    class Meta(FavoriteShoppingCartBaseModel.Meta):
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        default_related_name = 'shoppingcart'
        constraints = (
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe_in_shopping_cart'
            ),
        )

    def __str__(self):
        return self.user
