from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import os.path
from joblib import dump, load

# Fit model to linear regression
def logistic(training_data,target_data):
    X_train, X_test, y_train, y_test = train_test_split(training_data,target_data,random_state=42,test_size=0.2)
    model = LogisticRegression(max_iter=20000)
    model.fit(X_train,y_train)
    y_pre = model.predict(X_test)
    print('Accuracy : ', accuracy_score(y_test,y_pre))
    return model

# Now prep file to be interpreted by model
def read_training_data_and_build_model():
	# Pull all training data
	df_train = pd.read_csv(os.path.dirname(__file__) + '/../data/preprocessed_training_data.csv')
	df_train.head()

	# Split target-label from rest of data
	train_data = df_train.drop(['winner'],axis=1) # data without the winner
	target = df_train['winner'] # winner column in data

	# One hot encode data
	one = OneHotEncoder()
	one.fit(train_data)
	train = one.transform(train_data)
	print("Saving one hot encoder")
	dump(one, os.path.dirname(__file__) + '/../data/one_hot_encoder.joblib') 

	# Build model fitting to a Linear Regression
	model = logistic(train, target)

	# Save model
	print("Saving new best model")
	dump(model, os.path.dirname(__file__) + '/../data/best_model.joblib') 


class TftFightPredictor():
	def __init__(self):
		self.model = load(os.path.dirname(__file__) + '/../data/best_model.joblib') 
		self.encoder = load(os.path.dirname(__file__) + '/../data/one_hot_encoder.joblib')

	def predict_tft_fight(self, fight_data):
		"""
		Predict a given tft fight
		Arguments:
		fight_data - A list that looks like: 
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

		predict_this = self.encoder.transform([fight_data])
		prediction = self.model.predict(predict_this)
		return prediction[0]