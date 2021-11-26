from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_pandas.io import read_frame

import re
import numpy as np
import pandas as pd

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


def scatters(request):
    return render(request, "players/scatters.html")


def homepage(request):
    return render(request, "players/homepage.html")


def athletes(request, index):

    if request.method == 'GET':
        player_list_2022 = []
        player_tuple_2022 = PlayerInfo22.objects.values_list('id_id__name',
                                                             'club',
                                                             'club_logo',
                                                             'id_id__age',
                                                             'id_id__nationality',
                                                             'id_id__flag',
                                                             'best_position',
                                                             'id_id__preferred_foot',
                                                             'overall',
                                                             'id_id').exclude(contract_valid_until__lte = 2022).exclude(release_clause="")
        for each in player_tuple_2022:
            temp_dict = {'name': each[0],
                         'club': each[1],
                         'logo': each[2],
                         'age': each[3],
                         'nationality': each[4],
                         'flag': each[5],
                         'position': each[6],
                         'foot': each[7],
                         'overall': each[8],
                         'id': each[9]}
            player_list_2022.append(temp_dict)

        if index == '':
            index = 1
        pag = Paginator(player_list_2022, 20)
        page = pag.page(index)

        res_dict = {
            "players_2022": page
        }

        return render(request, "players/athletes.html", {"players_2022": page})

    if request.method == 'POST':
        target_name = request.POST['target_name']
        target_club = request.POST['target_club']
        target_nation = request.POST['target_nation']
        player_list_2022 = []
        player_tuple_2022 = PlayerInfo22.objects.values_list('id_id__name',
                                                             'club',
                                                             'club_logo',
                                                             'id_id__age',
                                                             'id_id__nationality',
                                                             'id_id__flag',
                                                             'best_position',
                                                             'id_id__preferred_foot',
                                                             'overall',
                                                             'id_id')\
                                                                .exclude(contract_valid_until__lte=2022)\
                                                                .exclude(release_clause="")\
                                                                .filter(id_id__name__icontains = str(target_name),
                                                                        club__icontains = str(target_club),
                                                                        id_id__nationality__icontains = str(target_nation))

        for each in player_tuple_2022:
            temp_dict = {'name': each[0],
                         'club': each[1],
                         'logo': each[2],
                         'age': each[3],
                         'nationality': each[4],
                         'flag': each[5],
                         'position': each[6],
                         'foot': each[7],
                         'overall': each[8],
                         'id': each[9]}
            player_list_2022.append(temp_dict)

        if index == '':
            index = 1
        pag = Paginator(player_list_2022, 20)
        page = pag.page(index)

        res_dict = {
            "players_2022": page
        }

        return render(request, "players/athletes.html", {"players_2022": page})


def prediction(request):
    return render(request, "players/prediction.html")


def similarity(request, target_id):

    # Getting target player's information
    target_player_basic = PlayerBasics.objects.get(pk = target_id)
    target_player_info = PlayerInfo22.objects.get(pk = target_id)
    target_player_status = PlayerStatus22.objects.get(pk = target_id)

    # Getting other players' information
    other_player_status = PlayerStatus22.objects.all().\
                                                    exclude(id_id__contract_valid_until__lte=2022).\
                                                    exclude(id_id__release_clause="")
    other_player_info = PlayerInfo22.objects.values_list('id_id__name',
                                                           'club',
                                                           'club_logo',
                                                           'id_id__age',
                                                           'id_id__nationality',
                                                           'id_id__flag',
                                                           'best_position',
                                                           'id_id__preferred_foot',
                                                           'overall',
                                                           'id_id').\
                                                            exclude(contract_valid_until__lte=2022).\
                                                            exclude(release_clause="")
    exclude_list = ['_state', 'week_foot', 'skill_moves', 'marking']

    target_status_dict = dict([(kk, target_player_status.__dict__[kk])
                               for kk in target_player_status.__dict__.keys()
                               if kk not in exclude_list])

    target_basic_dict = dict([(kk, target_player_basic.__dict__[kk])
                               for kk in target_player_basic.__dict__.keys()
                               if kk not in exclude_list])

    target_info_dict = dict([(kk, target_player_info.__dict__[kk])
                               for kk in target_player_info.__dict__.keys()
                               if kk not in exclude_list])

    other_info_df = read_frame(other_player_info)
    other_status_df = read_frame(other_player_status)
    other_status_df = other_status_df.drop(columns = [(col) for col in exclude_list if col in other_status_df.columns])
    other_status_df.rename(columns={'id': 'id_id'})

    target_status_np = other_status_df.loc[other_status_df['id'] == str(target_id)].drop(columns = ['id']).to_numpy()
    dis = np.linalg.norm(other_status_df.drop(columns = ['id']).to_numpy() - target_status_np, ord=2, axis = 1)
    other_info_df.loc[:, 'similarity'] = dis
    other_info_df['similarity'] = (1000-other_info_df['similarity'])/10

    res_list = []
    for each in other_player_info:
        temp_dict = {'name': each[0],
                     'club': each[1],
                     'logo': each[2],
                     'age': each[3],
                     'nationality': each[4],
                     'flag': each[5],
                     'position': each[6],
                     'foot': each[7],
                     'overall': each[8],
                     'id': each[9],
                     'similarity': float(other_info_df.loc[other_info_df['id'] == str(each[9])]['similarity'].values)}
        res_list.append(temp_dict)

    new_res_list = sorted(res_list, key=lambda e: e.__getitem__('similarity'), reverse = True)

    print(other_info_df)
    print(other_info_df.loc[other_info_df['id'] == '41']['similarity'])
    # for each in other_status_df.drop(columns = ['id']).to_numpy():
    #     compare_status_np = each
    #     print(np.linalg.norm(each-target_status_np, ord=2))

    pag = Paginator(new_res_list, 30)
    page = pag.page(1)

    return render(request, "players/similarity.html",
                  {'similar': page,
                   'target_player_basic': target_player_basic})


def player_detail(request, player_id):
    player_status = PlayerStatus22.objects.get(pk = player_id)
    player_basic = PlayerBasics.objects.get(pk = player_id)
    player_info = PlayerInfo22.objects.get(pk = player_id)

    exclude_list = ['_state', 'id_id', 'week_foot', 'skill_moves', 'marking']
    status_dict = dict([(kk, player_status.__dict__[kk]) for kk in player_status.__dict__.keys() if kk not in exclude_list])
    print(status_dict)

    return render(request, "players/player_detail.html",
                  {'player_status': status_dict,
                   'player_id': player_id,
                   'player_name': player_basic.name,
                   'player_photo': player_basic.photo,
                   'player_age': player_basic.age,
                   'player_pos': player_info.best_position,
                   'player_overall': player_info.overall,
                   'player_foot': player_basic.preferred_foot})