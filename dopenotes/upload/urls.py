from django.urls import path
from django.contrib.auth.views import login, logout
from .views import *

app_name = 'upload'
urlpatterns = [
    # Homepage
    path('', views.home),
]