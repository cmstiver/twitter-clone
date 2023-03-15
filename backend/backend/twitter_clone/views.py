from django.contrib.auth.models import User
from rest_framework import generics, permissions, views, status
from rest_framework.response import Response
from . import serializers, models
from django.contrib.auth import update_session_auth_hash
from .permissions import IsOwnerOrReadOnly


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserRegistrationSerializer


class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = serializers.ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.data.get("old_password")
            new_password = serializer.data.get("new_password")
            if not user.check_password(old_password):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return Response({"detail": "Password updated successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TweetListCreateView(generics.ListCreateAPIView):
    queryset = models.Tweet.objects.all()
    serializer_class = serializers.TweetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TweetDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Tweet.objects.all()
    serializer_class = serializers.TweetSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class TweetReplyListView(generics.ListCreateAPIView):
    serializer_class = serializers.TweetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        tweet_id = self.kwargs['tweet_id']
        return models.Tweet.objects.filter(parent_tweet_id=tweet_id)

    def perform_create(self, serializer):
        tweet_id = self.kwargs['tweet_id']
        parent_tweet = models.Tweet.objects.get(id=tweet_id)
        serializer.save(author=self.request.user, parent_tweet=parent_tweet)


class TweetLikesListView(generics.ListCreateAPIView):
    serializer_class = serializers.TweetLikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        tweet_id = self.kwargs['tweet_id']
        return models.Like.objects.filter(tweet=tweet_id)

    def perform_create(self, serializer):
        tweet_id = self.kwargs['tweet_id']
        tweet = models.Tweet.objects.get(id=tweet_id)
        serializer.save(user=self.request.user, tweet=tweet)
