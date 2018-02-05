from django.conf.urls import url
from .import views
app_name = 'login_and_sign'
urlpatterns = [
    url(r'^sign$', views.sign, name='sign'),
]