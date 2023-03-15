from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class Tweet(models.Model):
    content = models.TextField(max_length=280)
    parent_tweet = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    def save(self, *args, **kwargs):
        if self._state.adding and self.parent_tweet:
            Notification.objects.create(
                recipient=self.parent_tweet.user,
                sender=self.user,
                tweet=self,
                type='reply',
            )
        super().save(*args, **kwargs)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'tweet')

    def __str__(self):
        return f"{self.user.username} likes {self.tweet.content}"

    def save(self, *args, **kwargs):
        if self._state.adding:  # Check if this is a new Like being created
            Notification.objects.create(
                recipient=self.tweet.user,
                sender=self.user,
                tweet=self.tweet,
                type='like',
            )
        super().save(*args, **kwargs)


class Retweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'tweet')

    def __str__(self):
        return f"{self.user.username} retweeted {self.tweet.content}"

    def save(self, *args, **kwargs):
        if self._state.adding:  # Check if this is a new Retweet being created
            Notification.objects.create(
                recipient=self.tweet.user,
                sender=self.user,
                tweet=self.tweet,
                type='retweet',
            )
        super().save(*args, **kwargs)


class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"

    def save(self, *args, **kwargs):
        if self._state.adding:
            Notification.objects.create(
                recipient=self.followed,
                sender=self.follower,
                type='follow',
            )
        super().save(*args, **kwargs)


class Notification(models.Model):
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='+')
    tweet = models.ForeignKey(Tweet, on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=20, choices=[(
        'like', 'Like'), ('retweet', 'Retweet'), ('reply', 'Reply'), ('follow', 'Follow')])
    timestamp = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username} {self.type}ed {self.recipient.username}"
