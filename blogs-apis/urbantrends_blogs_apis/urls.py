from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from accounts.views import GoogleLogin, AppleLogin, SubscribeView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/auth/social/google/', GoogleLogin.as_view(), name='google_login'),
    path('api/auth/social/apple/', AppleLogin.as_view(), name='apple_login'),

    # Accounts
    path('api/accounts/', include('accounts.urls')),
    path('api/subscribe/', SubscribeView.as_view(), name='subscribe'),

    # Blogs
    path('api/', include('blogs.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
