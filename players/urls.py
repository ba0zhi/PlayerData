from django.contrib import admin
from django.urls import path
from players import views

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('clubs', views.clubs, name='clubs'),
    path('players', views.players, name='players'),
    path('predict_player', views.predict_player, name='predict_player'),
    path('similar_player', views.similar_player, name='similar_player'),
]