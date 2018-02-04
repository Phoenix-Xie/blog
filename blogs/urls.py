from django.conf.urls import url
from blogs import views
app_name = 'blogs'
urlpatterns = [
    url(r'^$', views, name='home'),
]
