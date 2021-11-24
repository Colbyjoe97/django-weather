from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^weather$', views.weather),
    url(r'^login', views.login_page),
    url(r'^user-login', views.login),
    url(r'^register$', views.register),
]
