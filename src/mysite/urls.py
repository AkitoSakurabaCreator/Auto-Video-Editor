from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings

from django.conf.urls.static import static #EC

from django.views.static import serve  #追加

# import xadmin #xadmin


urlpatterns = [
    path('', include('app.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('u22_admin/', admin.site.urls),
    re_path(r'^celery-progress/', include('celery_progress.urls', namespace="celery_progress")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)