from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from . import views
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('register/', views.UserCreate.as_view(), name='register-user'),
    path('my-profile/', views.UserUpdate.as_view(), name='edit-user'),
    path('obtain-auth/', ObtainAuthToken.as_view(), name='obtain-auth'),
    path('profiles/<int:id>/', views.UserRetrieve.as_view(), name='retrieve-user'),
    path('tweets/', views.TweetListCreate.as_view(), name='tweet-list-create'),
    path('tweets/<int:parent_tweet_id>/reply',
         views.TweetListCreate.as_view(), name='tweet-create-child'),
    path('tweets/<int:tweet_id>/', views.TweetDetail.as_view(),
         name='tweet-detail'),



]

urlpatterns = format_suffix_patterns(urlpatterns)
