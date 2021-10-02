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
