from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (Registration, LoginView, LogoutView,
                    TweetList, TweetDetail, CommentList,
                    FollowList, FollowDetail, LikeList,
                    LikeDetail, RetweetList, RetweetDetail,
                    NotificationList, NotificationDetail,
                    UserProfileDetail, UserProfileList, FollowUser)

urlpatterns = [
    path('register/', Registration.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('tweets/', TweetList.as_view(), name='tweet-list'),
    path('tweets/<int:pk>/', TweetDetail.as_view(), name='tweet-detail'),
    path('tweets/<int:pk>/comments/', CommentList.as_view(), name='comment-list'),
    path('follows/', FollowList.as_view(), name='follow-list'),
    path('follows/<int:pk>/', FollowDetail.as_view(), name='follow-detail'),
    path('follow/<int:user_id>/', FollowUser.as_view(), name='follow_user'),
    path('likes/', LikeList.as_view(), name='like-list'),
    path('likes/<int:pk>/', LikeDetail.as_view(), name='like-detail'),
    path('retweets/', RetweetList.as_view(), name='retweet-list'),
    path('retweets/<int:pk>/', RetweetDetail.as_view(), name='retweet-detail'),
    path('notifications/', NotificationList.as_view(), name='notification-list'),
    path('notifications/<int:pk>/', NotificationDetail.as_view(),
         name='notification-detail'),
    path('profiles/', UserProfileList.as_view(), name='profile-list'),
    path('profiles/<int:pk>/', UserProfileDetail.as_view(),
         name='profile-detail'),
    path('get-token/', obtain_auth_token, name='api_token_auth'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
