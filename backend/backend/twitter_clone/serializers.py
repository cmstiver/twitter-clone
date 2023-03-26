from rest_framework import serializers
from django.contrib.auth.models import User
from . import models
from django.contrib.auth.password_validation import validate_password
import re


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = ['name', 'image', 'bio',
                  'location', 'website_url', 'created_at']
        extra_kwargs = {
            'image': {'required': False},
            'bio': {'required': False},
            'location': {'required': False},
            'website_url': {'required': False},
            'created_at': {'read_only': True},
        }


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'profile']
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True},
            'email': {'required': False},
        }

    def validate_username(self, value):
        if not re.match(r'^[\w-]+$', value):
            raise serializers.ValidationError(
                'Username can only contain alphanumeric characters, underscores, and dashes.')
        if len(value) < 5:
            raise serializers.ValidationError(
                'Username must be at least 5 characters long.')
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        models.Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.name = profile_data.get('name', profile.name)
        profile.bio = profile_data.get('bio', profile.bio)
        profile.location = profile_data.get('location', profile.location)
        profile.website_url = profile_data.get(
            'website_url', profile.website_url)
        profile.image = profile_data.get('image', profile.image)
        profile.save()

        return instance


class TweetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = models.Tweet
        fields = ['id', 'user', 'content', 'image', 'created_at']
        read_only_fields = ['id', 'created_at']


class TweetDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = models.Tweet
        fields = ['id', 'user', 'parent_tweet',
                  'content', 'image', 'created_at', 'replies']
        read_only_fields = ['id', 'created_at']
