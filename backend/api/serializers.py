from django.contrib.auth import get_user_model
from django.db import transaction
from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.fields import Base64ImageField
from recipes.constant import COOK_TIME_MIN
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from users.models import Follow, FoodUser

User = get_user_model()


class FoodUserSerializer(UserSerializer):
    """Сериализатор пользователей приложения Foodgramm"""
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    def get_is_subscribed(self, obj):
        """Проверка информации о подписке текущего пользователя"""
        request = self.context.get('request')
        return (
            request and request.user.is_authenticated
            and obj.following.filter(
                user=request.user).exists()
        )

    class Meta:
        model = FoodUser
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_subscribed',
        )


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели теги."""

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ингредиенты."""

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit')


class ShortIngredientSerializer(serializers.ModelSerializer):
    """Краткий сериализатор для ингредиентов.
    Включает информацию о количестве ингрдиентов.
    """

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all())

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'amount'
        )


class RecipePostSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления рецептов.
    Сериализатор используется для создания и обновления рецептов.
    Включает информацию о списке ингредиентов, тегах и изображении.
    """

    ingredients = ShortIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField()
    cooking_time = serializers.IntegerField(
        write_only=True,
        min_value=COOK_TIME_MIN)

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        )

    def validate(self, data):
        ingredients = data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError(
                'В рецепте необходимо указать ингредиенты')
        inrgedients_list = [ingredient['id'] for ingredient in ingredients]
        ingredients_set = set(inrgedients_list)
        if len(ingredients) != len(ingredients_set):
            raise serializers.ValidationError(
                'Ингредиенты не должны повторяться!')
        tags = data.get('tags')
        if not tags:
            raise serializers.ValidationError(
                'Необходимо указать минимум один тег'
            )
        tag_set = set(tags)
        if len(tags) != len(tag_set):
            raise serializers.ValidationError(
                'Теги не должны повторяться!'
            )
        return data

    def create_ingredients(self, recipe, ingredients):
        recipe_ingredients = []
        for ingredient_data in ingredients:
            ingredient_id = ingredient_data.get('id')
            amount = ingredient_data.get('amount')
            recipe_ingredient = RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient_id,
                amount=amount
            )
            recipe_ingredients.append(recipe_ingredient)
        RecipeIngredient.objects.bulk_create(recipe_ingredients)

    @transaction.atomic
    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=self.context['request'].user,
                                       **validated_data)
        recipe.tags.set(tags_data)
        self.create_ingredients(recipe, ingredients_data)
        recipe.save()
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        instance.tags.set(tags_data)
        RecipeIngredient.objects.filter(recipe=instance).delete()
        self.create_ingredients(instance, ingredients_data)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeGetSerializer(
            instance, context={'request': self.context.get('request')}
        ).data


class RecipeGetSerializer(serializers.ModelSerializer):
    """Сериализатор для получения информации о рецептах."""

    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_image(self, obj):
        """Получает URL изображения рецепта."""
        if obj.image:
            return obj.image.url
        return None

    def get_ingredients(self, obj):
        """Получает информацию об ингредиентах рецепта."""
        ingredients_data = []
        for ingredient in obj.ingredients.all():
            recipe_ingredient = ingredient.recipe_ingredient.first()
            amount = recipe_ingredient.amount if recipe_ingredient else None
            ingredient_data = {
                'id': ingredient.id,
                'name': ingredient.name,
                'measurement_unit': ingredient.measurement_unit,
                'amount': amount
            }
            ingredients_data.append(ingredient_data)
        return ingredients_data

    def get_is_favorited(self, obj):
        """Проверяет, добавлен ли рецепт в избранное."""
        request = self.context.get('request')
        return (
            request and request.user.is_authenticated
            and obj.recipefavorite.filter(user=request.user).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        """Проверяет, добавлен ли рецепт в список покупок."""
        request = self.context.get('request')
        return (
            request
            and request.user.is_authenticated
            and obj.shoppingcart.filter(user=request.user).exists()
        )


class FollowSerializer(FoodUserSerializer):
    """Сериализатор подписок на авторов и получения их рецептов."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(FoodUserSerializer.Meta):
        fields = FoodUserSerializer.Meta.fields + ('recipes_count', 'recipes',)
        model = FoodUser

    def get_recipes(self, obj):
        """Получает список рецептов автора."""
        recipes = obj.recipes.all()
        pararms = self.context['request'].query_params
        if 'recipes_limit' in pararms:
            try:
                recipes = recipes[:int(pararms['recipes_limit'])]
            except ValueError:
                pass
        return ShortRecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        """Получает количество рецептов автора."""
        return obj.recipes.count()


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Краткий сериализатор для рецептов."""

    image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None


class FavoritetSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления рецептов в избранное."""

    class Meta:
        model = Favorite
        fields = ('user',
                  'recipe')

        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже добавлен в избранное'
            )
        ]

    def to_representation(self, instance):
        recipe = instance.recipe
        return ShortRecipeSerializer(recipe).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления рецептов список покупок."""

    class Meta:
        model = ShoppingCart
        fields = ('user',
                  'recipe')

        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже добавлен в избранное'
            )
        ]

    def to_representation(self, instance):
        recipe = instance.recipe
        return ShortRecipeSerializer(recipe).data


class SubscriberFollowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = (
            'user',
            'following'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Подписка уже оформлена'
            )
        ]

    def validate(self, data):
        user = data.get('user')
        following_user = data.get('following')
        if user == following_user:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!')
        return data
