from django.conf.urls import patterns, url

from Apps.news import views

urlpatterns = patterns('',
    url(r'^$', views.Index, name = 'index'),
    url(r'^addnews/$', views.AddNews, name = 'addnews')
)
