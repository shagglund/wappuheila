from django.conf.urls.defaults import patterns, url
from wappuheila.auth import views
from wappuheila import settings


urlpatterns = patterns('',
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',kwargs={'template_name':'registration/logout.html'}, name='logout'),
    url(r'^login/error/$', views.login_error, name='login_error'),
    url(r'^user_control_panel/$', views.user_control_panel, name='user_control_panel'),
)