from rest_framework import generics, permissions
from django.contrib.auth.models import User
from . import serializers


class UserCreate(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer


class UserUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user


class UserRetrieve(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'id'
