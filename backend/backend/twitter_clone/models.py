from django.db import models
from django.contrib.auth.models import User


class Tweet(models.Model):
    content = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tweets')
    likes = models.ManyToManyField(
        User, related_name='liked_tweets', blank=True)
    retweets = models.ManyToManyField(
        User, related_name='retweeted_tweets', blank=True, through='Retweet')

    def __str__(self):
        return f'{self.author.username} - {self.content}'


class Retweet(models.Model):
    tweet = models.ForeignKey(
        Tweet, on_delete=models.CASCADE, related_name='retweets')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='retweets')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('tweet', 'user')

    def __str__(self):
        return f'{self.user.username} retweeted {self.tweet}'


class Comment(models.Model):
    content = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    tweet = models.ForeignKey(
        Tweet, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'{self.author.username} - {self.content}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=160, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', blank=True)

    def __str__(self):
        return self.user.username


class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f'{self.follower.username} follows {self.followed.username}'


class Notification(models.Model):
    TYPE_CHOICES = [
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
        ('retweet', 'Retweet')
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notifications')
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE,
                              null=True, blank=True, related_name='notifications')
    retweet = models.ForeignKey(
        Retweet, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.type.capitalize()} notification for {self.user.username}'


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='likes')
    tweet = models.ForeignKey(
        Tweet, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'tweet')

    def __str__(self):
        return f'{self.user.username} likes {self.tweet}'
