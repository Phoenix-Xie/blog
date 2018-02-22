from django.conf.urls import url
from .import views
app_name = 'login_and_sign'
urlpatterns = [
    url(r'^create_code_img/', views.create_code_img, name='create_code_img'),
    url(r'^sign$', views.sign, name='sign'),
    url(r'^message$', views.sign_message, name='message'),
    url(r'^home$', views.home, name='home'),
]