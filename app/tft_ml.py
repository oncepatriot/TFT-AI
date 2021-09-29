import tft_fight_predictor.tft_api.tft_api as tft_api



match_data = tft_api.get_match_by_match_id(tft_api.TEST_MATCH_ID)


players = match_data["info"]["participants"]

players = [{
	"placement": player['placement'],
	"traits": player['traits'],
	"level": player['level'],
	"units": player['units'],
} for player in players]

players = sorted(players, key=lambda i: i['placement'])

# Create dataset. 
# Each player beats all players underneath them.
# Each player beats their own board with less units.

#Format data as such:
# ["WINNER. 0 = player1, 1=player2 ", [player1data], [playerdata2]]

