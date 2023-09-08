from django.core.exceptions import ValidationError
from djoser.views import UserViewSet as DjoserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import FollowSerializer, UserCreateSerializer, UserSerializer
from users.models import Follow, User


class UserViewSet(DjoserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    @action(
        methods=('GET',), detail=False, permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        queryset = Follow.objects.filter(user=self.request.user)
        page = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(methods=('POST', 'DELETE',), detail=True)
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            if request.user.id == author.id:
                raise ValidationError(
                    'Невозможно подписаться на себя.'
                )
            else:
                serializer = FollowSerializer(
                    Follow.objects.create(user=request.user, author=author),
                    context={'request': request},
                )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
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
