from rest_framework import generics, permissions, status
from django.contrib.auth.models import User
from . import serializers, models
from django.shortcuts import get_object_or_404
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response


class UserCreate(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer


class UserUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user


class UserRetrieve(generics.RetrieveAPIView):
    serializer_class = serializers.UserSerializer
    lookup_field = 'username'

    def get_queryset(self):
        username = self.kwargs['username']
        return User.objects.filter(username=username)


class TweetListCreate(generics.ListCreateAPIView):
    queryset = models.Tweet.objects.filter(parent_tweet__isnull=True)
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
    serializer_class = serializers.TweetDetailSerializer
    lookup_url_kwarg = 'tweet_id'

    def get_queryset(self):
        tweet_id = self.kwargs['tweet_id']
        return models.Tweet.objects.filter(id=tweet_id)


class LikeToggle(generics.GenericAPIView):
    queryset = models.Like.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, tweet_id):
        tweet = models.Tweet.objects.get(id=tweet_id)
        user = request.user
        try:
            like = models.Like.objects.get(user=user, tweet=tweet)
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Like.DoesNotExist:
            models.Like.objects.create(user=user, tweet=tweet)
            return Response(status=status.HTTP_201_CREATED)


class RetweetToggle(generics.GenericAPIView):
    queryset = models.Retweet.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, tweet_id):
        tweet = models.Tweet.objects.get(id=tweet_id)
        user = request.user
        try:
            retweet = models.Retweet.objects.get(user=user, tweet=tweet)
            retweet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Retweet.DoesNotExist:
            models.Retweet.objects.create(user=user, tweet=tweet)
            return Response(status=status.HTTP_201_CREATED)


class FollowToggle(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(User, id=user_id)

        if user_to_follow == request.user:
            return Response({'error': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            follow = models.Follow.objects.get(
                follower=request.user, followed=user_to_follow)
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Follow.DoesNotExist:
            models.Follow.objects.create(
                follower=request.user, followed=user_to_follow)
            return Response(status=status.HTTP_201_CREATED)
