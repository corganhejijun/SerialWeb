from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^chart/', views.chart, name='chart'),
    url(r'onePage/', views.onePage, name='onePage'),
    url(r'fourPage/', views.fourPage, name='fourPage'),
    url(r'data/', views.datadown, name='datadown')
]