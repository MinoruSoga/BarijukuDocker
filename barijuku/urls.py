from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('app.urls')),
    path('admin/', admin.site.urls),
    # path('accounts/', include('accounts.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('student/', include('student.urls')),
    path('trainer/', include('trainer.urls')),
    # path('accounts/', include('allauth.urls')),
    path('user/', include('user.urls')),
    path('shop/', include('shop.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
