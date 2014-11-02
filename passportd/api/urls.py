from django.conf.urls import patterns, url

from api import views

urlpatterns = patterns('',
    url(r'^$', views.PingView.as_view(), name='ping'),
    url(r'^timeslots$', views.TimeslotsView.as_view(), name='timeslots'),
    url(r'^boats$', views.BoatsView.as_view(), name='boats'),
)
