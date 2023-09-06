# from rest_framework import generics
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny
# from .serializers import UserCreateSerializer


# class UserCreateView(generics.CreateAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = UserCreateSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         return Response({
#             'user': UserCreateSerializer(
#                 user, context=self.get_serializer_context()
#             ).data,
#             'message': 'User created successfully.',
#         })
