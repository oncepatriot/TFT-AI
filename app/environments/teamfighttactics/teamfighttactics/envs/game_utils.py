import json
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import random
import sys
from joblib import dump, load
import os.path
from collections import Counter

def get_champion_data():
    champions_data = json.load(open('tft_static_data/set5patch1115/champions.json'))
    return champions_data

def get_items_data():
    items_data = json.load(open('tft_static_data/set5patch1115/items.json'))
    return items_data

def get_random_item_component():
    # Base components have ids from 1 to 9
    item = random.randint(1, 9)
    return item

def combine_items(item1, item2):
    # Take advantage of how riot provides item data.
    # BF Sword(1) + BF Sword(2) = "12" Deathblade
    items = get_items_data()

    items_to_combine = [item1, item2].sort()
    combined_item_id = ""
    for item in items_to_combine:
        combined_item_id += str(item)

    return int(combined_item_id)


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
    categories += [['None'] + champion_ids] * 5
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

class PlayerEncoder():
    def __init__(self):
        self.player_state_encoder = self.get_game_state_hot_encoder()

    def get_game_state_hot_encoder(self):
        encoder = load('./game_state_encoder.joblib') 
        return encoder

    # Take a Player instance and return their flattened_state to
    # be one hot encoded
    def get_player_state_flattened(self, player):
        board = [[c.champion_id, c.items[0], c.items[1], c.items[2], c.level] if c else ['None',0,0,0,0] for c in player.board]
        bench = [[c.champion_id, c.items[0], c.items[1], c.items[2], c.level] if c else ['None',0,0,0,0] for c in player.bench]
        shop = [c.champion_id if c else 'None' for c in player.shop]
        flattened_state = np.hstack(shop+board+bench)
        return flattened_state

    def get_player_observation(self, player):
        try:
            player_flattened = self.get_player_state_flattened(player)
            player_state = self.player_state_encoder.transform([player_flattened]).toarray()[0]
            observation = np.array([player.gold/100, player.health/100, player.streak/30, player.level/9, player.exp/100])
            observation = np.concatenate((observation, player_state))
        except Exception as e:
            print(player_flattened)
            print(player_state)
            print(observation)
            raise Exception(e)
        return observation
