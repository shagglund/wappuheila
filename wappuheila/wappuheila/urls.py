from django.conf.urls.defaults import patterns, url
from wappuheila.wappuheila import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^wappuheilas/$', views.wappuheila, name='wappuheilas'),
    url(r'^wappuheila/(?P<wph_id>\d+)/$', views.wappuheila, name='wappuheila_details'),
    url(r'^questions/$', views.questions, name='questions'),
    url(r'^questions/results/$', views.results, name='questions_results'),
    url(r'^leave_message/(?P<wph_id>\d+)$', views.leave_message, name='leave_message'),
    url(r'^register_as_wappuheila/$', views.register_as_wappuheila, name='register_as_wappuheila'),
)