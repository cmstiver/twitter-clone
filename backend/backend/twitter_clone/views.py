from django.contrib.auth.models import User
from rest_framework import generics, permissions, views, status
from rest_framework.response import Response
from . import serializers, models
from django.contrib.auth import update_session_auth_hash
from .permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404
from django.db.models import Q


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserRegistrationSerializer


class UserUpdateView(generics.RetrieveUpdateAPIView):
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
        serializer.save(user=self.request.user)


class TweetDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Tweet.objects.all()
    serializer_class = serializers.TweetSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class FollowingTweetsListView(generics.ListAPIView):
    serializer_class = serializers.TweetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.values_list('followed', flat=True)
        queryset = models.Tweet.objects.filter(
            Q(user__in=following_users) | Q(retweet__user__in=following_users))
        return queryset


class TweetReplyListView(generics.ListCreateAPIView):
    serializer_class = serializers.TweetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        tweet_id = self.kwargs['tweet_id']
        return models.Tweet.objects.filter(parent_tweet_id=tweet_id)

    def perform_create(self, serializer):
        tweet_id = self.kwargs['tweet_id']
        parent_tweet = models.Tweet.objects.get(id=tweet_id)
        serializer.save(user=self.request.user, parent_tweet=parent_tweet)


class TweetLikesListView(generics.ListCreateAPIView):
    serializer_class = serializers.TweetLikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        tweet_id = self.kwargs['tweet_id']
        return models.Like.objects.filter(tweet=tweet_id)

    def perform_create(self, serializer):
        tweet_id = self.kwargs['tweet_id']
        tweet = get_object_or_404(models.Tweet, id=tweet_id)
        user = self.request.user
        like = models.Like.objects.filter(tweet=tweet, user=user).first()

        if like:
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            serializer.save(user=user, tweet=tweet)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class TweetRetweetListView(generics.ListCreateAPIView):
    serializer_class = serializers.TweetLikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        tweet_id = self.kwargs['tweet_id']
        return models.Retweet.objects.filter(tweet=tweet_id)

    def perform_create(self, serializer):
        tweet_id = self.kwargs['tweet_id']
        tweet = get_object_or_404(models.Tweet, id=tweet_id)
        user = self.request.user
        retweet = models.Retweet.objects.filter(tweet=tweet, user=user).first()

        if retweet:
            retweet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            serializer.save(user=user, tweet=tweet)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class FollowListView(generics.ListCreateAPIView):
    serializer_class = serializers.FollowSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id', None)
        if user_id:
            user = get_object_or_404(User, pk=user_id)
        else:
            user = self.request.user

        return models.Follow.objects.filter(followed=user)

    def perform_create(self, serializer):
        user_id = self.kwargs.get('user_id', None)
        if user_id:
            user = get_object_or_404(User, id=user_id)
        else:
            user = self.request.user

        follower = self.request.user

        if follower == user:
            return Response({'error': 'You cannot follow yourself!'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            follow = models.Follow.objects.get(
                follower=follower, followed=user)
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Follow.DoesNotExist:
            serializer.save(follower=follower, followed=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserProfileDetailView(generics.RetrieveAPIView):
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()

    def get_object(self):
        user_id = self.kwargs.get('user_id', None)
        if user_id:
            user = get_object_or_404(User, pk=user_id)
        else:
            user = self.request.user

        return get_object_or_404(models.UserProfile, user=user)


class UserLikeListView(generics.ListAPIView):
    serializer_class = serializers.TweetLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id', None)
        if user_id:
            user = get_object_or_404(User, pk=user_id)
        else:
            user = self.request.user

        return models.Like.objects.filter(user=user)


class UserRepliesListView(generics.ListAPIView):
    serializer_class = serializers.TweetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id', None)
        if user_id:
            user = get_object_or_404(User, pk=user_id)
        else:
            user = self.request.user

        return models.Tweet.objects.filter(user=user, parent_tweet__isnull=False)


class NotificationListView(generics.ListAPIView):
    serializer_class = serializers.NotificationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return models.Notification.objects.filter(recipient=user, seen=False)


class NotificationMarkAsSeenView(views.APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request):
        unseen_notifications = models.Notification.objects.filter(
            recipient=request.user, seen=False)

        for notification in unseen_notifications:
            notification.seen = True
            notification.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
