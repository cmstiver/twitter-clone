from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=15)
    image = models.ImageField(upload_to='profile_images/',
                              default='default.webp')
    bio = models.TextField(max_length=160, default="")
    location = models.CharField(max_length=40, default="")
    website_url = models.URLField(default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}'s profile"


class Tweet(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tweets')
    parent_tweet = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    content = models.CharField(max_length=280)
    image = models.ImageField(upload_to='tweet_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username}: {self.content}'
