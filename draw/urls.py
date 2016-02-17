from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /draw/
    url(r'^$', views.test1, name='test1'),
    url(r'^[0-9]+/$', views.test2, name='test2'),
]
