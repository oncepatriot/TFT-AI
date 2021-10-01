import json

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