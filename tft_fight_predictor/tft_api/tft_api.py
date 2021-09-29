import requests

TEST_PUUID = "fXw8o7z7zlhYLI4j8FYYAMEdwRph6m85YvQX1o2FuElCz8SZHAuK9RrDHEZYl8mGh5k-Y9ufP1-dzQ"
TEST_MATCH_ID = "NA1_4055205965"
API_KEY = "RGAPI-5815debf-eed2-4d71-b14d-02e1a2cf3169"


def get_match_ids_by_puuid(puuid):
    r = requests.get(f"https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?count=20&api_key={API_KEY}")
    match_ids = r.json()
    return match_ids

# get_match_ids_by_puuid(TEST_PUUID)

def get_match_by_match_id(match_id):
    r = requests.get(f"https://americas.api.riotgames.com/tft/match/v1/matches/{match_id}?api_key={API_KEY}")
    return r.json()

get_match_by_match_id(TEST_MATCH_ID)