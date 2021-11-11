from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.


def index(request):
    return render(request, "players/index.html")
def clubs(request):
    return render(request, "players/clubs.html")
def homepage(request):
    return render(request, "players/homepage.html")
def players(request):
    return render(request, "players/players.html")
def predict_player(request):
    return render(request, "players/predict_player.html")
def similar_player(request):
    return render(request, "players/similar_player.html")
