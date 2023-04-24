from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from . import views
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('register', views.UserCreate.as_view(), name='register-user'),
    path('register_random', views.UserCreateRandom.as_view(),
         name='register-random-user'),
    path('my-profile', views.UserUpdate.as_view(), name='edit-user'),
    path('obtain-auth', ObtainAuthToken.as_view(), name='obtain-auth'),
    path('profiles/<str:username>',
         views.UserRetrieve.as_view(), name='retrieve-user'),
    path('tweets', views.TweetListCreate.as_view(), name='tweet-list-create'),
    path('following_tweets', views.FollowingTweetList.as_view(),
         name='following-tweet-list'),
    path('tweets/<int:tweet_id>', views.TweetDetail.as_view(),
         name='tweet-detail'),
    path('tweets/<int:parent_tweet_id>/reply',
         views.TweetListCreate.as_view(), name='tweet-create-reply'),
    path('tweets/<int:tweet_id>/like',
         views.LikeToggle.as_view(), name='like-toggle'),
    path('tweets/<int:tweet_id>/retweet',
         views.RetweetToggle.as_view(), name='retweet-toggle'),
    path('profiles/<int:user_id>/follow',
         views.FollowToggle.as_view(), name='follow-toggle'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
