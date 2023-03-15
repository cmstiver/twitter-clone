from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from . import views
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', ObtainAuthToken.as_view()),
    path('edit-profile/', views.UserUpdateView.as_view(), name='edit-profile'),
    path('change_password/', views.ChangePasswordView.as_view(),
         name='change_password'),
    #     path('tweets/', views.TweetList.as_view(), name='tweet-list'),
    #     path('tweets/<int:pk>/', views.TweetDetail.as_view(), name='tweet-detail'),
    #     path('tweets/<int:pk>/comments/',
    #          views.CommentList.as_view(), name='comment-list'),
    #     path('tweets/<int:pk>/likes/', views.LikeList.as_view(), name='comment-list'),
    #     path('tweets/<int:pk>/retweets/',
    #          views.RetweetList.as_view(), name='comment-list'),
    #     path('profile/<int:pk>/', views.UserProfileDetail.as_view(),
    #          name='profile-detail'),
    #     path('profile/<int:pk>/follows', views.FollowList.as_view(),
    #          name='follow-list'),
    #     path('notifications/', views.NotificationList.as_view(),
    #          name='notification-list'),
    #     path('notifications/<int:pk>/', views.NotificationDetail.as_view(),
    #          name='notification-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
