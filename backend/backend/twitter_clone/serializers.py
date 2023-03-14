from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Tweet, Comment, Follow, Like, Notification, Retweet
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        user = authenticate(
            username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError("Invalid username or password.")
        attrs['user'] = user
        return attrs


class LogoutSerializer(serializers.Serializer):
    pass


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'author']


class TweetSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes = serializers.SerializerMethodField()
    retweets = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = ['id', 'content', 'created_at',
                  'author', 'comments', 'likes', 'retweets']

    def get_likes(self, obj):
        return obj.likes.count()

    def get_retweets(self, obj):
        return obj.retweets.count()


class FollowSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)
    followed = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'followed']


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tweet = TweetSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'tweet']


class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tweet = TweetSerializer(read_only=True)
    retweet = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'user', 'tweet', 'retweet',
                  'type', 'created_at', 'read']

    def get_retweet(self, obj):
        if obj.type == 'retweet':
            return RetweetSerializer(obj.retweet).data
        else:
            return None


class RetweetSerializer(serializers.ModelSerializer):
    tweet = TweetSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Retweet
        fields = ['id', 'tweet', 'user', 'created_at']
