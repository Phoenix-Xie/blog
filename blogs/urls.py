from django.conf.urls import url
from blogs import views
app_name = 'blogs'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^search/$', views.search, name='search'),
    url(r'^(?P<passage_id>[0-9]+)/detail/$', views.passage_detail, name='passage_detail'),
    url(r'^(?P<passage_id>[0-9]+)/edit/$', views.passage_edit, name='passage_edit'),
    url(r'^self/$', views.self_home, name='self_home'),
    url(r'^change_password/', views.change_password, name='change_password'),
    url(r'^(?P<passage_id>[0-9]+)/edit/statu$', views.edit_statu, name='edit_statu'),
    url(r'^add/$', views.add_passage, name='add_passage'),
    url(r'^add/statu/$', views.add_statu, name='add_statu'),
    url(r'^(?P<passage_id>[0-9]+)/comment/$', views.add_comment, name='add_comment'),
    url(r'^(?P<passage_id>[0-9]+)/comment/statu$', views.add_comment_statu, name='add_comment_statu'),
]
