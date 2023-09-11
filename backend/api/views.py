from django.core.exceptions import ValidationError
from djoser.serializers import SetPasswordSerializer
from djoser.views import UserViewSet as DjoserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import (
    FollowSerializer, IngredientSerializer, RecipeCreateSerializer,
    RecipeSerializer, TagSerializer, UserCreateSerializer, UserSerializer,
    FavoritedSerializer
)
from recipes.models import FavoriteRecipe, Ingredient, Recipe, Tag
from users.models import Follow, User


class UserViewSet(DjoserViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    @action(('POST',), detail=False, permission_classes=(IsAuthenticated,))
    def set_password(self, request, *args, **kwargs):
        serializer = SetPasswordSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            self.request.user.set_password(serializer.data['new_password'])
            self.request.user.save()
            return Response(
                'Password changed successfully',
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
        if request.method == 'POST':
            if request.user.id == author.id:
                raise ValidationError(
                    'Unable to subscribe to yourself'
                )
            else:
                serializer = FollowSerializer(
                    Follow.objects.create(user=request.user, author=author),
                    context={'request': request},
                )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        elif request.method == 'DELETE':
            follow = Follow.objects.filter(
                user=request.user,
                author=author,
            )
            if follow.exists():
                follow.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {'errors': 'Unrecognized author'},
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


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        queryset = Recipe.objects.select_related('author').prefetch_related(
            'tags', 'ingredients', 'recipe'
        )
        return queryset

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
            serializer = FavoritedSerializer(favorite_recipe)
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
        else:
            return Response(
                {'message': 'Recipe is not found in favorites'},
                status.HTTP_404_NOT_FOUND
            )
