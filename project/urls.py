# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^', include('luggage.urls')),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^currencies/', include('currencies.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r"^payments/", include("pinax.stripe.urls")),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

    urlpatterns += static(
            settings.STATIC_URL,
            document_root=settings.STATIC_ROOT
    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
