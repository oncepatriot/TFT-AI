from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import os.path
import sys
from joblib import dump, load
sys.path.insert(1, os.path.join(sys.path[0], '...'))

import environments.teamfighttactics.teamfighttactics.envs.game_utils as game_utils

# Fit model to linear regression
def logistic(training_data,target_data):
    X_train, X_test, y_train, y_test = train_test_split(training_data,target_data,random_state=42,test_size=0.2)
    model = LogisticRegression(max_iter=20000)
    model.fit(X_train,y_train)
    y_pre = model.predict(X_test)
    print('Accuracy : ', accuracy_score(y_test,y_pre))
    return model

def get_categories_for_one():

    champions_data = game_utils.get_champion_data()
    champion_ids = [c['championId'] for c in champions_data]
    champion_ids.insert(0, 'None')
    champion_ids.sort()

    items_data = game_utils.get_items_data()
    item_ids = [i['id'] for i in items_data]
    item_ids.insert(0, 0)
    item_ids.sort()

    levels = [0,1,2,3]
    levels.sort()

    categories = [
        champion_ids,item_ids,item_ids,item_ids,levels,
        champion_ids,item_ids,item_ids,item_ids,levels,
        champion_ids,item_ids,item_ids,item_ids,levels,
        champion_ids,item_ids,item_ids,item_ids,levels,
        champion_ids,item_ids,item_ids,item_ids,levels,
        champion_ids,item_ids,item_ids,item_ids,levels,
        champion_ids,item_ids,item_ids,item_ids,levels,
        champion_ids,item_ids,item_ids,item_ids,levels,
        champion_ids,item_ids,item_ids,item_ids,levels,

        champion_ids,item_ids,item_ids,item_ids,levels,
        champion_ids,item_ids,item_ids,item_ids,levels,
        champion_ids,item_ids,item_ids,item_ids,levels,
        champion_ids,item_ids,item_ids,item_ids,levels,
        champion_ids,item_ids,item_ids,item_ids,levels,
        champion_ids,item_ids,item_ids,item_ids,levels,
        champion_ids,item_ids,item_ids,item_ids,levels,
        champion_ids,item_ids,item_ids,item_ids,levels,
        champion_ids,item_ids,item_ids,item_ids,levels
    ]
    return categories
       

# Now prep file to be interpreted by model
def read_training_data_and_build_model():
    # Pull all training data

    df_train = pd.read_csv(os.path.dirname(__file__) + '/../data/preprocessed_training_data.csv')
    df_train.head()

    # Split target-label from rest of data
    train_data = df_train.drop(['winner'],axis=1) # data without the winner
    target = df_train['winner'] # winner column in data

    # One hot encode data
    one = OneHotEncoder(categories=get_categories_for_one())
    one.fit(train_data)
    train = one.transform(train_data)
    print("Saving one hot encoder")
    dump(one, os.path.dirname(__file__) + '/../data/one_hot_encoder.joblib') 

    # Build model fitting to a Linear Regression
    model = logistic(train, target)

    # Save model
    print("Saving new best model")
    dump(model, os.path.dirname(__file__) + '/../data/best_model.joblib') 
