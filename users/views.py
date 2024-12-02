from time import sleep
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from users.models import User
from users import serializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.UserCreateSerializer
        elif self.action == 'auth':
            return serializers.UserAuthSerializer
        elif self.action == 'partial_update':
            return serializers.UserUpdateSerializer
        return serializers.UserSerializer

    @swagger_auto_schema(
        responses={201: serializers.UserSerializer,}
    )
    def create(self, request):
        create_serializer = self.get_serializer(data=request.data)
        if create_serializer.is_valid():
            user, _ = User.objects.get_or_create(phone_number=create_serializer.validated_data["phone_number"])
            serializer = serializers.UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, id=pk)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(
        responses={200: serializers.UserSerializer,}
    )
    def partial_update(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        update_serializer = self.get_serializer(instance=user, data=request.data, partial=False)
        if update_serializer.is_valid():
            update_serializer.save()
            serializer = serializers.UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='auth')
    @swagger_auto_schema(
        responses={200: serializers.OTPResponseSerializer,}
    )
    def auth(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            sleep(2)
            return Response({"message": "OTP sent"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)