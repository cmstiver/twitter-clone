from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=15)
    image = models.ImageField(upload_to='profile_images/',
                              default='https://twirpz.files.wordpress.com/2015/06/twitter-avi-gender-balanced-figure.png?w=640')
    bio = models.TextField(max_length=160)
    location = models.CharField(max_length=40)
    website_url = models.URLField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}'s profile"
