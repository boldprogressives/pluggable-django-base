from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',

    url('^$', 'standalone_django_project.views.home', name='home'),

# @@TODO

    url(r'^admin/', include(admin.site.urls)),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )

urlpatterns += patterns(
    'django.contrib.auth.views',
    (r'^accounts/login/$', 'login'),
    (r'^accounts/logout/$', 'logout'),
    )

for pattern in settings.PLUGIN_URLCONFS:
    if len(pattern) == 2:
        regex, module = pattern
        urlpatterns += patterns(
            '',
            url(regex, include(module)),
            )
    elif len(pattern) == 3:
        regex, module, namespace = pattern
        urlpatterns += patterns(
            '',
            url(regex, include(module, namespace=namespace)),
            )
    
