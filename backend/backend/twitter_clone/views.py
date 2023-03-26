from rest_framework import generics, permissions
from django.contrib.auth.models import User
from . import serializers, models
from django.shortcuts import get_object_or_404
from .permissions import IsOwnerOrReadOnly


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


class TweetListCreate(generics.ListCreateAPIView):
    queryset = models.Tweet.objects.all()
    serializer_class = serializers.TweetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        parent_tweet_id = self.kwargs.get('parent_tweet_id')
        if parent_tweet_id:
            parent_tweet = get_object_or_404(models.Tweet, pk=parent_tweet_id)
            serializer.save(user=self.request.user, parent_tweet=parent_tweet)
        else:
            serializer.save(user=self.request.user)


class TweetDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = models.Tweet.objects.all()
    serializer_class = serializers.TweetDetailSerializer
    lookup_url_kwarg = 'tweet_id'
