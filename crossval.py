import time
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from models import time_to_float
from selection import create_dataframe
from sklearn.pipeline import make_pipeline

########## Runs Cross Validation on Baseline Models & XGBoost for SWJoin3 ##########

## creates the connection to the db and returns X with the most important features and y with bikes_available
## pass in how many features to choose, and name of the status weather table
conn, X, y = create_dataframe(17, 'SWJoin_3')

# cross validate on different models
# prints out how much time each takes for comparison
start = time.perf_counter()
dt_scores = cross_val_score(DecisionTreeRegressor(), X, y, scoring='neg_mean_absolute_error')
end = time.perf_counter()
print('Decision Tree MAE: %2f' %(-1 * dt_scores.mean()))
print(f"Elapsed Time: {end - start:0.2f} seconds")

start = time.perf_counter()
rf_scores = cross_val_score(RandomForestRegressor(), X, y, scoring='neg_mean_absolute_error')
end = time.perf_counter()
print('Random Forest MAE: %2f' %(-1 * rf_scores.mean()))
print(f"Elapsed Time: {end - start:0.2f} seconds")

start = time.perf_counter()
xgb_scores = cross_val_score(XGBRegressor(n_estimators=200, learning_rate=0.05), X, y, scoring='neg_mean_absolute_error')
end = time.perf_counter()
print('XGBoost MAE: %2f' %(-1 * xgb_scores.mean()))
print(f"Elapsed Time: {end - start:0.2f} seconds")

# conn.close()
