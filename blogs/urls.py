from django.conf.urls import url
from blogs import views
app_name = 'blogs'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^(?P<passage_id>[0-9]+)/detail/$', views.passage_detail, name='passage_detail'),
    url(r'^(?P<pasage_id>[0-9]+)/edit/$', views.passage_edit, name='passage_edit'),
    url(r'^self/$', views.self_home, name='self_home'),
    url(r'^(?P<pasage_id>[0-9]+)/edit/statu$', views.edit_statu, name='edit_statu'),
    url(r'^add/$', views.add_passage, name='add_passage'),
    url(r'^add/statu/$', views.add_statu, name='add_statu')
]
