from django.db.models import Sum
from django.http import HttpResponse
from djoser.serializers import SetPasswordSerializer
from djoser.views import UserViewSet as DjoserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    SAFE_METHODS, IsAuthenticated,
)
from rest_framework.response import Response

from .filters import RecipeFilter
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import (
    FollowSerializer, IngredientSerializer, RecipeCreateSerializer,
    RecipeInfoSerializer, RecipeSerializer, TagSerializer,
    UserCreateSerializer, UserSerializer,
)
from recipes.models import (
    FavoriteRecipe, Ingredient, IngredientsInRecipe, Recipe, ShoppingList, Tag,
)
from users.models import Follow, User
from django_filters.rest_framework import DjangoFilterBackend


class UserViewSet(DjoserViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    @action(('GET',), detail=False, permission_classes=(IsAuthenticated,))
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == 'GET':
            return self.retrieve(request, *args, **kwargs)

    @action(('POST',), detail=False)
    def set_password(self, request, *args, **kwargs):
        serializer = SetPasswordSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            self.request.user.set_password(serializer.data['new_password'])
            self.request.user.save()
            return Response(
                {'message': 'Password changed successfully'},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(('GET',), detail=False, permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        queryset = Follow.objects.filter(user=self.request.user)
        page = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(('POST', 'DELETE'), detail=True,)
    def subscribe(self, request, id=None):
        author = get_object_or_404(User, id=id)
        follow = Follow.objects.filter(user=request.user, author=author,)
        if request.method == 'POST':
            if request.user.id == author.id:
                return Response(
                    {'message': 'Unable to subscribe to yourself'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if follow.exists():
                return Response(
                    {'message': 'Already subscribed'},
                    status=status.HTTP_204_NO_CONTENT
                )
            serializer = FollowSerializer(
                Follow.objects.create(user=request.user, author=author),
                context={'request': request},
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        elif request.method == 'DELETE':
            if follow.exists():
                follow.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'errors': 'No such author in your subscriptions'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {'errors': 'Invalid operation'},
            status=status.HTTP_400_BAD_REQUEST,
        )


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def destroy(self, request, pk=None):
        instance = get_object_or_404(Recipe, id=pk)
        if not instance.author == request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        ('POST', 'DELETE'), detail=True, permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        favorite_recipe = FavoriteRecipe.objects.filter(
            user=request.user, recipe=recipe
        ).first()

        if request.method == 'POST':
            if favorite_recipe:
                return Response(
                    {'message': 'Recipe is already in favorites'},
                    status.HTTP_400_BAD_REQUEST
                )
            favorite_recipe = FavoriteRecipe(user=request.user, recipe=recipe)
            serializer = RecipeInfoSerializer(favorite_recipe)
            favorite_recipe.save()

            return Response(
                serializer.data,
                status.HTTP_201_CREATED,
            )
        if request.method == 'DELETE':
            if favorite_recipe:
                favorite_recipe.delete()
            return Response(
                {'message': ('Recipe has been successfully '
                             'removed from favorites')},
                status.HTTP_204_NO_CONTENT
            )

    @action(
        ('POST', 'DELETE'), detail=True, permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        shopping_list = ShoppingList.objects.filter(
            user=request.user, recipe=recipe
        ).first()

        if request.method == 'POST':
            if shopping_list:
                return Response(
                    {'message': 'Recipe is already in your shopping list'},
                    status.HTTP_400_BAD_REQUEST
                )
            shopping_list = ShoppingList(user=request.user, recipe=recipe)
            serializer = RecipeInfoSerializer(shopping_list)
            shopping_list.save()

            return Response(
                serializer.data,
                status.HTTP_201_CREATED,
            )
        if request.method == 'DELETE':
            if not shopping_list:
                return Response(
                    {'message': 'No such recipe in your shopping list'},
                    status.HTTP_400_BAD_REQUEST)
            shopping_list.delete()
            return Response(
                {'message': ('Recipe has been successfully '
                             'removed from shopping list')},
                status.HTTP_204_NO_CONTENT
            )

    @action(('GET',), detail=False, permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        ingredients = IngredientsInRecipe.objects.all()
        ingredients = ingredients.values(
            'ingredient__name',
            'ingredient__measurement_unit'
        )
        shopping_list = ingredients.filter(
            recipe__in_shopping_list__user=request.user
        ).annotate(ingredient_total=Sum('amount'))
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_list.txt"'
        )
        response.write(f"{request.user.username}'s shopping list\n\n")
        for ingredient in shopping_list:
            ingredients = ''.join(
                f'{ingredient.get("ingredient__name")} - '
                f'{ingredient.get("ingredient_total")}'
                f'{ingredient.get("ingredient__measurement_unit")}\n'
            )
            response.write(f'{ingredients}')

        return response
