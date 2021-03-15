from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('user.urls')),
    path('', include('blood_request.urls')),
    path('event/', include('event.urls')),
    path('notifications', include('notification_control.urls')),

    # path('oauth/', include('social_django.urls', namespace='social')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
