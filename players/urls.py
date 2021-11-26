from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path(r'scatters', views.scatters, name='scatters'),
    path(r'prediction', views.prediction, name='prediction'),
    path(r'similarity/<int:target_id>/', views.similarity, name='similarity'),
    path(r'player_detail/<int:player_id>', views.player_detail, name='player_detail'),
    url(r'^athletes/(\d*)$', views.athletes, name='athletes'),
]