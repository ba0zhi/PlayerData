from django.contrib import admin
from django.urls import path
from players import views

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
]