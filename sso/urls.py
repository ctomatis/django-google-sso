from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^auth/google/callback', views.google_callback),

    url(r'^logout/$', auth_views.logout, {'next_page': '/'}),
    url(r'^admin/login/$', views.index),
    url(r'^admin/logout/$', auth_views.logout, {'next_page': '/'})
]
