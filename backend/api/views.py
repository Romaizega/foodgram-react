from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.filters import IngredientFilter, RecipeFilter
from api.format_to_pdf import generate_pdf
from api.pagination import LimitPagination
from api.permissions import IsAuthorOrAdminOrReadOnly
from api.serializers import (FavoritetSerializer, FollowSerializer,
                             FoodUserSerializer, IngredientSerializer,
                             RecipePostSerializer, ShoppingCartSerializer,
                             SubscriberFollowingSerializer, TagSerializer)
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from users.models import Follow, FoodUser


class FoodUserViewSet(UserViewSet):
    """ViewSet для работы с пользователями приложения Foodgramm."""

    queryset = FoodUser.objects.all()
    serializer_class = FoodUserSerializer
    pagination_class = LimitPagination

    def get_permissions(self):
        if self.action == 'me':
            return (IsAuthenticated(),)
        return super().get_permissions()

    @action(detail=True, methods=('post',),
            serializer_class=FollowSerializer,
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        user_to_follow = get_object_or_404(FoodUser, id=id)
        data = {
            'user': request.user.id,
            'following': id
        }
        serializer = SubscriberFollowingSerializer(
            data=data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        user_serializer = FoodUserSerializer(user_to_follow)
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def unsubscribe(self, request, id):
        user = request.user
        deleted_count, _ = Follow.objects.filter(
            user=user, following=id).delete()
        if deleted_count:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=('get',),
            serializer_class=FollowSerializer,
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        """Получает подписки текущего пользователя."""
        user = self.request.user
        subscriptions = FoodUser.objects.filter(following__user=user)
        page = self.paginate_queryset(subscriptions)
        serializer = FollowSerializer(
            page,
            context={'request': request},
            many=True,
        )
        return self.get_paginated_response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для работы с тегами."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для работы с ингредиентами."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с рецептами."""

    queryset = Recipe.objects.order_by('-pub_date').all()
    serializer_class = RecipePostSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def create_new_object(self, request, pk, serializer_class):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializer_class(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_object(self, request, pk, model):
        recipe = get_object_or_404(Recipe, id=pk)
        deleted_count, _ = model.objects.filter(
            user=request.user, recipe=recipe).delete()
        if deleted_count:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=('post',),
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk):
        return self.create_new_object(request, pk, FavoritetSerializer)

    @favorite.mapping.delete
    def unfavorite(self, request, pk):
        return self.delete_object(request, pk, Favorite)

    @action(detail=True, methods=('post',),
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk):
        return self.create_new_object(request, pk, ShoppingCartSerializer)

    @shopping_cart.mapping.delete
    def remove_from_shopping_cart(self, request, pk):
        return self.delete_object(request, pk, ShoppingCart)

    @action(
        ['get'],
        detail=False)
    def download_shopping_cart(self, request):
        """Загрузка списка покупок в формате PDF."""
        ingredient_list = ShoppingCart.objects.filter(
            user=request.user
        ).values(
            'recipe__ingredients__name',
            'recipe__ingredients__measurement_unit',
        ).annotate(
            total_amount=Sum('recipe__recipe_ingredient__amount')
        ).order_by('recipe__ingredients__name')

        pdf_response = generate_pdf(ingredient_list)
        return pdf_response
