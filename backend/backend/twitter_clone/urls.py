from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('tweets/', views.TweetList.as_view()),
    path('tweets/<int:pk>/', views.TweetDetail.as_view()),
    path('tweets/<int:pk>/comments/', views.CommentList.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('follows/', views.FollowList.as_view()),
    path('follows/<int:pk>/', views.FollowDetail.as_view()),
    path('likes/', views.LikeList.as_view()),
    path('likes/<int:pk>/', views.LikeDetail.as_view()),
    path('retweets/', views.RetweetList.as_view()),
    path('retweets/<int:pk>/', views.RetweetDetail.as_view()),
    path('notifications/', views.NotificationList.as_view()),
    path('notifications/<int:pk>/', views.NotificationDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
