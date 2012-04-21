from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Wappuheila.views.home', name='home'),
    # url(r'^Wappuheila/', include('Wappuheila.foo.urls')),
    url(r'^',include('wappuheila.wappuheila.urls')),
    url(r'^auth/',include('wappuheila.auth.urls')),
    url(r'social_auth/', include('social_auth.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
