from django.contrib import admin
from django.urls import path, include
from frontend_app.views import front

urlpatterns = [
    path("", front, name="front"),
    path('admin/', admin.site.urls),
    path('api/', include('twitter_clone.urls'))
]
