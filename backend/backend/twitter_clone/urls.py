from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from . import views
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', ObtainAuthToken.as_view()),
    path('profile/edit/', views.UserUpdateView.as_view(), name='edit-profile'),
    path('change_password/', views.ChangePasswordView.as_view(),
         name='change_password'),
    path('tweets/', views.TweetListCreateView.as_view(), name='tweet-list'),
    path('tweets/<int:pk>/', views.TweetDetailView.as_view(), name='tweet-detail'),
    path('following_tweets/', views.FollowingTweetsListView.as_view(),
         name='following_tweets'),
    path('tweets/<int:tweet_id>/replies/',
         views.TweetReplyListView.as_view(), name='tweet-reply'),
    path('tweets/<int:tweet_id>/likes/',
         views.TweetLikesListView.as_view(), name='tweet-like'),
    path('tweets/<int:tweet_id>/retweets/',
         views.TweetRetweetListView.as_view(), name='tweet-retweet'),
    path('profile/', views.UserProfileDetailView.as_view(),
         name='my-profile'),
    path('profile/likes/', views.UserLikeListView.as_view(),
         name='my-profile-likes'),
    path('profile/replies/', views.UserRepliesListView.as_view(),
         name='my-profile-replies'),
    path('profile/follows/', views.FollowListView.as_view(),
         name='my-follow-list'),
    path('profile/<int:user_id>/', views.UserProfileDetailView.as_view(),
         name='profile-detail'),
    path('profile/<int:user_id>/follows/', views.FollowListView.as_view(),
         name='follow-list'),
    path('notifications/', views.NotificationListView.as_view(),
         name='notification-list'),
    path('notifications/seen/', views.NotificationMarkAsSeenView.as_view(),
         name='notifications-seen'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
