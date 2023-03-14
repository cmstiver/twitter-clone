from django.contrib import admin
from .models import Tweet, Retweet, Comment, UserProfile, Follow, Notification, Like

admin.site.register(Tweet)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Like)
admin.site.register(Notification)
admin.site.register(Retweet)
