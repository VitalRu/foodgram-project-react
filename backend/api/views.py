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
)
from recipes.models import Ingredient, Recipe, Tag
from users.models import Follow, User


class UserViewSet(DjoserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    @action(('GET',), detail=False, permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        queryset = Follow.objects.filter(user=self.request.user)
        page = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(('POST', 'DELETE'), detail=True,)
    def subscribe(self, request, id):
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


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
