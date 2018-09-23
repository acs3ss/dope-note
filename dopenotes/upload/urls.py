from django.urls import path
from django.conf.urls import url
#from django.contrib.auth.views import login, logout
from . import views

app_name = 'upload'
urlpatterns = [
    path('', views.index),
    path('class/add', views.add_class, name='add-class'),
    url(r'^(?P<pk>\d+)/$', views.video_detail_view, name='detail')
]
