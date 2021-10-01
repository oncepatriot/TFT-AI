import requests
import random
import pandas as pd
import json
import itertools
import copy
import csv
import os.path
import time

TEST_PUUID = "8o6dOaqtLQEni0LoLCCEr_VV8Q_vpKiWyjdB1hqvFbQctqTWLhI8v6F2afau2xyRiGAXx6EWKzetTg" #RamKev
TEST_MATCH_ID = "NA1_4055205965"
API_KEY = "RGAPI-9c210b84-88ac-4f60-95cb-ec8e97e4bf5f"


def get_match_ids_by_puuid(puuid):
    r = requests.get(f"https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?count=50&api_key={API_KEY}")
    match_ids = r.json()
    return match_ids

def get_match_by_match_id(match_id):
    r = requests.get(f"https://americas.api.riotgames.com/tft/match/v1/matches/{match_id}?api_key={API_KEY}")
    return r.json()

def run_match_data_scraper():
    player_puuids = [TEST_PUUID]
    match_ids_processed = {}
    while True:   
        time.sleep(15)
        print("Getting match ids by puuid:")
        puuid = player_puuids.pop(0)

        match_ids = get_match_ids_by_puuid(puuid)
        match_ids = random.sample(match_ids, 10)

        for match_id in match_ids:
            if not match_ids_processed.get(match_id):
                match_data = get_match_by_match_id(match_id)
                match_puuids = match_data['metadata']['participants']
                match_puuids.remove(puuid)
                player_puuids.append(match_puuids)

                print("Processing Match Data: ", match_id)
                process_match_data_and_add_to_training_data_set(match_data)
                match_ids_processed[match_id] = True
                time.sleep(15)
            else:
                continue

def process_match_data_and_add_to_training_data_set(match_data):
	"""
	Periodically query Riot TFT API for match data to process and
	add to training data. TODO: Separate the processing into smaller functions
	
	"""

    # TODO: DOES NOT HANDLE 10/11/12 UNITS FROM FONS?
    players = match_data["info"]["participants"]
    players = sorted(players, key=lambda i: i['placement'])
    players = [{
        "placement": player['placement'],
        "units": player['units'],
    } for player in players]

    for player in players:
        player['units'] = [[unit['character_id'], unit['items'], unit['rarity'], unit['tier']] for unit in player['units']]
 
    match_pairs = []
    for i, j in itertools.product(players, players):
        if i['placement'] < j['placement']:
            if random.randint(0, 1) == 1:
                match_pairs.append([0, i, j])
            else:
                match_pairs.append([1, j, i])

    # Generate more match pair data by pairing players against
    # strictly worse versions of themselves. (one less unit)
    for player in players:
        player_copy = copy.deepcopy(player)
        while len(player_copy['units']) > 0:
            stronger = copy.deepcopy(player_copy)
            player_copy['units'].pop()
            weaker = copy.deepcopy(player_copy)
            
            # Randomize whether to add to data set to not influence
            # model too much that more unit = win
            if random.randint(0,100) < 15:
	            if random.randint(0, 1) == 1:
	                match_pairs.append([0, stronger, weaker])
	            else:
	                match_pairs.append([1, weaker, stronger])

    rows = []
    for match_pair in match_pairs:
        winner = match_pair[0]
        player1_units = match_pair[1]["units"]
        player2_units = match_pair[2]["units"]
        
        row = [winner]

        for player_num, player_units in enumerate([player1_units, player2_units]):
            for i in range(9):
                if i < len(player_units):
                    unit = player_units[i]
                    unit_id = unit[0]
                    unit_items = unit[1]
                    unit_level = unit[3]
                else:
                    unit_id = "None"
                    unit_items = [0,0,0]
                    unit_level = 0
                
                row.append(unit_id)
                items = unit_items + [0]*(3-len(unit_items))
                row = row + items
                
                row.append(unit_level)

        rows.append(row)

    print("About to write to csv")
    with open(os.path.dirname(__file__) + '/../data/preprocessed_training_data.csv', mode='a') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in rows:
            writer.writerow(row)

    csv_file.close()
    print("done, waiting 15 seconds before next request")