import json
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import random
import sys
from joblib import dump, load
import os.path

def get_champion_data():
    champions_data = json.load(open('tft_static_data/set5patch1115/champions.json'))
    return champions_data

def get_items_data():
    items_data = json.load(open('tft_static_data/set5patch1115/items.json'))
    return items_data

def get_cost_x_champions(cost):
    champions_data = get_champion_data()
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


def create_and_save_game_state_one_hot_encoder():
    champions_data = get_champion_data()
    items_data = get_items_data()

    champion_ids = [c['championId'] for c in champions_data]
    item_ids = [str(i['id']) for i in items_data]

    flattened_game_state = _generate_flattened_player_state_for_one_hot_encoding()

    categories = []
    # First five categories is the shop, which can hold CHAMPION_IDs
    categories += [champion_ids] * 5
    for i in range(18):
        categories += [['None'] + champion_ids] # the champion name
        categories += [['0'] + item_ids] * 3 # 3 items champ can hold
        categories.append(["0", "1","2","3"]) # champ levels

    game_state_encoder = OneHotEncoder(
        categories=categories,
        # drop=True <- We may want to drop first column due to collinearity.
    )
    game_state_encoder.fit([flattened_game_state])

    one_hot_encoded_state = game_state_encoder.transform([flattened_game_state]).toarray()[0]

    dump(game_state_encoder, './game_state_encoder.joblib') 
    encoder = load('./game_state_encoder.joblib') 


def get_game_state_hot_encoder():
    encoder = load('./game_state_encoder.joblib') 
    return encoder


def _generate_flattened_player_state_for_one_hot_encoding():
    champions_data = get_champion_data()
    items_data = get_items_data()

    champion_ids = [c['championId'] for c in champions_data]
    item_ids = [str(i['id']) for i in items_data]

    # Mock out what the game state we want to encode will look like

    # A board will consists of up to 9 champions, each with 3 item slots and their level.
    # A champion is represented by a array of size 4 with [CHAMPION_ID, ITEM1, ITEM2, ITEM3, CHAMPION_LEVEL]
    board = [
        [
            random.choice(champion_ids), 
            random.choice(item_ids), 
            random.choice(item_ids), 
            random.choice(item_ids), 
            random.randint(1,3)
        ] for i in range(8)
    ]
    board.append(['None',0,0,0,0]) # add an unoccupied board slot

    bench = [
        [
            random.choice(champion_ids), 
            random.choice(item_ids), 
            random.choice(item_ids), 
            random.choice(item_ids), 
            random.randint(1,3)
        ] for i in range(8)
    ]
    bench.append(['None',0,0,0,0])

    # SHOP just has the champion names
    shop = [random.choice(champion_ids) for i in range(5)] 

    # Now we need to represent this game state as a 1-d vector. 
    # Note that since we work with np arrays, everything is converted to 
    # a string
    flattened_game_state = np.hstack(shop+board+bench)
    return flattened_game_state
