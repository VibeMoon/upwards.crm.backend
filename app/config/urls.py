from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from .yasg import urlpatterns as docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    # path('api/', include('crm.urls')),
]

urlpatterns += docs_urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
