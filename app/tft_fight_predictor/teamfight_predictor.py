from joblib import dump, load
import os.path


class TftFightPredictor():
	def __init__(self):
		self.model = load(os.path.dirname(__file__) + '/data/best_model.joblib') 
		self.encoder = load(os.path.dirname(__file__) + '/data/one_hot_encoder.joblib')

	def predict_tft_fight(self, player_one, player_two):
		"""
		Predict a given tft fight
		Arguments: PlayerOne instance, PlayertwoInstance

		fight_data to pass into predictor should look like:
		[
			"TFT5_Nautilus",89,0,0,2,
			"TFT5_Thresh",0,0,0,1,
			"TFT5_Nidalee",0,0,0,2,
			"TFT5_Jax",16,29,15,1,
			"TFT5_Rell",55,77,0,2,
			"TFT5_Galio",2099,2046,2011,2,
			"TFT5_Viego",45,0,0,2,
			"TFT5_Garen",34,33,1158,2,
			"None",0,0,0,0,

			"TFT5_Vayne",49,23,26,3,
			"TFT5_Hecarim",2055,25,0,3,
			"TFT5_Sejuani",0,0,0,3,
			"TFT5_Nautilus",0,0,0,2,
			"TFT5_Thresh",0,0,0,2,
			"TFT5_Ashe",17,79,17,2,
			"TFT5_Rell",34,44,4,1,
			"TFT5_Draven",0,0,0,1,
			"None",0,0,0,0
		]
		each "row" is  unit_id,item_id,item_id2,item_id3,level
		"""
		p1board = self.encode_player_state_for_prediction(player_one)
		p2board = self.encode_player_state_for_prediction(player_two)
		try:
			predict_this = self.encoder.transform([p1board + p2board])
		except Exception as e:
			print(p1board, p2board)
			raise Exception("Problem encoding players boards for prediction")

		prediction = self.model.predict_proba(predict_this)

		# Returns probabilities player_one wins, player_two_wins. Example: .7, .3
		return prediction[0][0], prediction[0][1]

	def encode_player_state_for_prediction(self, player):
		"""
		transform:
			class Player():
		        self.id = id
		        self.gold = 0
		        self.level = 1
		        self.exp = 0
		        self.shop = [None]*5
		        self.board = [None]*9
		        self.bench = [None]*9
		        self.health = 100
		        self.ready = False
		        self.items = [0]*6
		        self.streak = 0

			to CSV:
			[
				"TFT5_Vayne",49,23,26,3,
				"TFT5_Hecarim",2055,25,0,3,
				"TFT5_Sejuani",0,0,0,3,
				"TFT5_Nautilus",0,0,0,2,
				"TFT5_Thresh",0,0,0,2,
				"TFT5_Ashe",17,79,17,2,
				"TFT5_Rell",34,44,4,1,
				"TFT5_Draven",0,0,0,1,
				"None",0,0,0,0
			]
		"""
		encoded = []
		sorted(player.board, key=lambda c: 0 if c != None else 1)
		for champ in player.board:
			if champ == None:
				encoded += ["None",0,0,0,0]
			else:
				encoded += [
					champ.champion_id, 
					int(champ.items[0]) if champ.items[0] else 0,
					int(champ.items[1]) if champ.items[1] else 0,
					int(champ.items[2]) if champ.items[2] else 0,
					champ.level
				]

		return encoded