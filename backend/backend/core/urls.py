from django.contrib import admin
from django.urls import path, include
from frontend_app.views import front
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", front, name="front"),
    path('admin', admin.site.urls),
    path('api', include('twitter_clone.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
