from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^weather$', views.weather),
    url(r'^login', views.login_page),
    url(r'^register$', views.register),
    url(r'^user-login', views.login),
    url(r'^favorite$', views.favorite),
    url(r'^delete$', views.delete),
]
