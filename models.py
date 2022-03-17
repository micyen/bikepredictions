import pandas as pd
from sklearn.metrics import mean_absolute_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

############################ Baseline Models ############################

# uses a decision tree regressor
def decision_tree(train_X, train_y, val_X, val_y):

    print("--------------------- DecisionTreeRegressor ---------------------")
    # fit the model
    d_tree = DecisionTreeRegressor(random_state=0)
    d_tree.fit(train_X, train_y)

    # make validation predictions
    val_pred = d_tree.predict(val_X)

    # calculate mean square error
    mae(val_X, val_y, val_pred)

# uses random forests
def random_forest(train_X, train_y, val_X, val_y):

    print("--------------------- RandomForestRegressor ---------------------")
    # fit the momdel
    rf_model = RandomForestRegressor(random_state=0)
    rf_model.fit(train_X, train_y)

    # make validation predictions
    val_pred = rf_model.predict(val_X)

    # calculate mean square error
    mae(val_X, val_y, val_pred)

############################ Main Models ############################

# uses xgboost
def xgboost(train_X, train_y, val_X, val_y):

    print("--------------------- XGBoostRegressor ---------------------")
    # fit the model 200
    xgb_model = XGBRegressor( n_estimators=200, learning_rate=0.05 )
    xgb_model.fit(train_X, train_y)

    # make validation predictions
    val_pred = xgb_model.predict(val_X)

    # calculate mean square error
    mae(val_X, val_y, val_pred)

############################ Misc Functions ############################

# converts the timestamps to floating points
def time_to_float(data):
    new_data = data.copy()
    new_data['time'] = data['time'].values.astype(float)
    return new_data


# computes the mean square error
def mae(val_X, val_y, val_pred):

    val_mae = mean_absolute_error(val_pred, val_y)
    val_cpy = val_X.copy()
    #val_cpy['time'] = pd.to_datetime(val_cpy['time'])
    val_cpy['bikes_available'] = val_pred
    print(val_cpy)
    print( "Validation MAE = {}".format(val_mae) )
