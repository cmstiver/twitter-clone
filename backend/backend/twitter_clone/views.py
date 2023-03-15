from django.contrib.auth.models import User
from rest_framework import generics

from . import serializers


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserRegistrationSerializer
