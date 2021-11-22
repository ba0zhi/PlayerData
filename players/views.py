from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django_pandas.io import read_frame
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import numpy as np
import pandas as pd

from sklearn.cluster import KMeans

from .models import PlayerBasics
from .models import PlayerInfo17
from .models import PlayerInfo18
from .models import PlayerInfo19
from .models import PlayerInfo20
from .models import PlayerInfo21
from .models import PlayerInfo22
from .models import PlayerStatus17
from .models import PlayerStatus18
from .models import PlayerStatus19
from .models import PlayerStatus20
from .models import PlayerStatus21
from .models import PlayerStatus22
# Create your views here.


def index(request):
    player_basic = PlayerBasics.objects.all()
    return render(request, "players/index.html",
                  {"PlayerBasics": player_basic})


def clubs(request):
    return render(request, "players/clubs.html")


def homepage(request):
    return render(request, "players/homepage.html")


def athletes(request):
    player_list_2022 = []
    player_tuple_2022 = PlayerInfo22.objects.values_list('id_id__name',
                                                         'club',
                                                         'club_logo',
                                                         'id_id__age',
                                                         'id_id__nationality',
                                                         'id_id__flag',
                                                         'best_position',
                                                         'id_id__preferred_foot',
                                                         'overall').exclude(contract_valid_until__lte = 2022).exclude(release_clause="")
    for each in player_tuple_2022:
        temp_dict = {'name': each[0],
                     'club': each[1],
                     'logo': each[2],
                     'age': each[3],
                     'nationality': each[4],
                     'flag': each[5],
                     'position': each[6],
                     'foot': each[7],
                     'overall': each[8]}
        player_list_2022.append(temp_dict)

    pag = Paginator(player_list_2022, 30)
    page = pag.page(12)

    res_dict = {
        "players_2022": page
    }

    return render(request, "players/athletes.html", {"players_2022": page})


def prediction(request):
    return render(request, "players/prediction.html")


def similarity(request):
    return render(request, "players/similarity.html")


def player_detail(request):
    return render(request, "players/player_detail.html")