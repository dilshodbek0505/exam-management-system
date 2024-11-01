from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect

from .schema import swagger_urlpatterns

urlpatterns = [
    path("", lambda _request: redirect('swagger/')),
    path("admin/", admin.site.urls),
    path("api/v1/common/", include("apps.common.urls", namespace="common")),
    path("api/v1/notifications/", include("apps.notification.urls", namespace="notifications")),
    path("api/v1/user/", include("apps.user.urls", namespace='user')),
    path("i18n/", include("django.conf.urls.i18n"))
]

urlpatterns += swagger_urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
