from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from ..blog import views, views_upload
# from blog import views , views_upload

urlpatterns = [
    path('api/auth/', include('accounts.urls')),
    path('api/', include('blog.urls')),
]

# 在开发环境中提供媒体文件访问支持
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)