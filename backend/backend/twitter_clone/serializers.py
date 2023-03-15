from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from . import models


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = models.UserProfile
        fields = ['username', 'bio', 'location',
                  'birth_date', 'profile_picture']


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'username': {'max_length': 15},
            'email': {'required': False, 'allow_blank': True},
            'password': {'write_only': True},
        }

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        models.UserProfile.objects.create(user=user)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False, partial=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'profile']
        extra_kwargs = {
            'username': {'max_length': 15},
            'email': {'required': False, 'allow_blank': True}
        }

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        instance = super().update(instance, validated_data)

        if profile_data:
            profile_serializer = UserProfileSerializer(
                instance.profile, data=profile_data, partial=True)

            if profile_serializer.is_valid(raise_exception=True):
                profile_serializer.save()

        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value


class TweetSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(
        read_only=True, source='user.username')

    class Meta:
        model = models.Tweet
        fields = ['id', 'content', 'user', 'timestamp']
        read_only_fields = ['id', 'timestamp']


class TweetLikeSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        read_only=True)
    user = serializers.StringRelatedField(
        read_only=True, source='user.username')
    tweet = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.Like
        fields = ['id', 'user_id', 'user', 'tweet']


class TweetRetweetSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        read_only=True)
    user = serializers.StringRelatedField(
        read_only=True, source='user.username')
    tweet = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.Like
        fields = ['id', 'user_id', 'user', 'tweet']


class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.StringRelatedField(
        read_only=True, source='follower.username')
    followed = serializers.StringRelatedField(
        read_only=True, source='followed.username')

    class Meta:
        model = models.Follow
        fields = ['follower', 'followed']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        fields = ['id', 'recipient', 'sender',
                  'tweet', 'type', 'timestamp', 'seen']
        read_only_fields = ['id', 'timestamp']
