from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=15)
    image = models.ImageField(upload_to='profile_images/',
                              default='default.webp')
    bio = models.CharField(max_length=160, default="")
    location = models.CharField(max_length=40, default="")
    website_url = models.URLField(max_length=75, default="")
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

    @property
    def replies_ordered_by_likes(self):
        return self.replies.annotate(like_count=Count('likes')).order_by('-like_count')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username}: {self.content}'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(
        Tweet, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'tweet')

    def __str__(self):
        return f"{self.user.username} likes {self.tweet.content}"


class Retweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(
        Tweet, on_delete=models.CASCADE, related_name='retweets')

    class Meta:
        unique_together = ('user', 'tweet')

    def __str__(self):
        return f"{self.user.username} retweeted {self.tweet.content}"


class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"
