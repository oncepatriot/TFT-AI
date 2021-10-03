import json
from sklearn.preprocessing import OneHotEncoder
import numpy as np

def get_cost_x_champions(cost):
    champions_data = json.load(open('tft_static_data/set5patch1115/champions.json'))
    # [
    #  {
    #    "name": "Aatrox",
    #    "championId": "TFT5_Aatrox",
    #    "cost": 1,
    #    "traits": [
    #      "Set5_Redeemed",
    #      "Set5_Legionnaire"
    #    ]
    # }, ...]
    champs = [c for c in champions_data if c['cost'] == cost]
    return champs

def get_champion_id_and_item_name_to_unique_id_map():
    champions_data = json.load(open('tft_static_data/set5patch1115/champions.json'))
    items_data = json.load(open('tft_static_data/set5patch1115/items.json'))

    champs_and_items = []
    for c in champions_data:
        champs_and_items.append(c['championId'])
    for i in items_data:
        champs_and_items.append(i['id'])

    champs_and_items.insert(0, None)

    num_ids = len(champs_and_items)
    id_map = {}
    for i, champ_or_item in enumerate(champs_and_items):
        id_map[champ_or_item] = (i / num_ids)

    return id_map
