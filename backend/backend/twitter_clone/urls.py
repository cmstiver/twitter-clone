from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from . import views
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('register/', views.UserCreate.as_view(), name="register_user"),
    path('my-profile/', views.UserUpdate.as_view(), name='edit_user'),
    path('obtain-auth/', ObtainAuthToken.as_view(), name='obtain_auth'),
    path('profiles/<int:id>/', views.UserRetrieve.as_view(), name='retrieve_user'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
