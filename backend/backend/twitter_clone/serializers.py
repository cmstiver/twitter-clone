from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'image', 'bio', 'location', 'website_url',]
        extra_kwargs = {
            'image': {'required': False},
            'bio': {'required': False},
            'location': {'required': False},
            'website_url': {'required': False},
        }


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'profile']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': False},
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user, **profile_data)
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
