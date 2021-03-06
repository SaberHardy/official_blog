from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    # path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    # path('secret/', include(admin.site.urls)),  # this is the new admin path
    path('admin/', admin.site.urls),
    path('', include('blogapp.urls', namespace='blog')),
    path('account/', include('accounts.urls', namespace='accounts')),
    path('account/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL,
#                           document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)
