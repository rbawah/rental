from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view( 
    openapi.Info(
        title="DJANGOREALTOR  API",
        default_version="0.0.1",
        description="A consummable API for DJANGOREALTOR",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="arbawah1@gmail.com"),
        license=openapi.License(name="BSD License"),
        ),
            public=True,
            permission_classes=(permissions.AllowAny,),
            )

urlpatterns = [
    
    path('dradmin1372/', admin.site.urls), # Django Admin
    #path('accounts/', include('django.contrib.auth.urls')), # Django User Management
    path('accounts/', include('allauth.urls')), # django-allauth User Management
    path('', include('mainpages.urls')),
    path('accounts/', include('accounts.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/dj-rest-auth/', include('dj_rest_auth.urls')),
    path('api/', include('api.urls')),
    path('api/dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

