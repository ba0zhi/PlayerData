from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path(r'clubs', views.clubs, name='clubs'),
    path(r'prediction', views.prediction, name='prediction'),
    path(r'similarity', views.similarity, name='similarity'),
    path(r'players', views.players, name='players'),
]