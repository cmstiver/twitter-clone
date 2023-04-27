from rest_framework import generics, permissions, status
from django.contrib.auth.models import User
from . import serializers, models
from django.shortcuts import get_object_or_404
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
import requests
from rest_framework.authtoken.models import Token
from django.db.models import Q


class UserCreate(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer


class UserCreateRandom(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer

    def post(self, request, *args, **kwargs):
        # Fetch JSON data from provided URL
        url = "https://api.mockaroo.com/api/0915f590?count=1&key=abc3baa0"
        response = requests.get(url)
        json_data = response.json()[0]
        print(json_data)

        # Validate and save new user
        serializer = self.get_serializer(data=json_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Generate auth token for new user
        user = serializer.instance
        token, created = Token.objects.get_or_create(user=user)

        # Create response data with auth token
        response_data = serializer.data
        response_data['auth_token'] = token.key

        # Return response
        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


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


class FollowingTweetList(generics.ListAPIView):
    serializer_class = serializers.TweetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        followed_users = models.Follow.objects.filter(
            follower=self.request.user).values_list('followed', flat=True)
        user_tweets = models.Tweet.objects.filter(user__in=followed_users)
        retweeted_tweet_ids = models.Retweet.objects.filter(
            user__in=followed_users).values_list('tweet_id', flat=True)
        retweeted_tweets = models.Tweet.objects.filter(
            id__in=retweeted_tweet_ids)
        return (user_tweets | retweeted_tweets).distinct().order_by('-created_at')


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

    def post(self, request, username):
        user_to_follow = get_object_or_404(User, username=username)

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


class FollowingList(generics.ListAPIView):
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        follows = models.Follow.objects.filter(follower=user)
        followed_users = [follow.followed for follow in follows]
        return followed_users


class FollowerList(generics.ListAPIView):
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        follows = models.Follow.objects.filter(followed=user)
        followers = [follow.follower for follow in follows]
        return followers


class UserTweetsList(generics.ListAPIView):
    serializer_class = serializers.TweetSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        user_tweets = models.Tweet.objects.filter(user__username=username)
        retweeted_tweet_ids = models.Retweet.objects.filter(
            user__username=username).values_list('tweet_id', flat=True)
        return (user_tweets | models.Tweet.objects.filter(id__in=retweeted_tweet_ids)).distinct().order_by('-created_at')


class UserLikesList(generics.ListAPIView):
    serializer_class = serializers.TweetSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        liked_tweet_ids = models.Like.objects.filter(
            user__username=username).values_list('tweet_id', flat=True)
        return models.Tweet.objects.filter(id__in=liked_tweet_ids)
