# this statement is for Sriya because her shell was being weird
import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages')
#
import pandas as pd
import sqlite3 as sq
import pymysql
import time
from sklearn.model_selection import train_test_split
from models import decision_tree, random_forest, xgboost, time_to_float
from selection import create_dataframe

########## Main Program for Running Tests ##########

# TODO add elements for user to choose which columns to include so we can easily do sensitivity analysis

## creates the connection to the db and returns X with the most important features and y with bikes_available
## pass in how many features to choose, and name of the status weather table
conn, X, y = create_dataframe(17, 'StatusWeatherJoin')

## features (columns) are extracted into X
# print(X)

## target column
# print(y)

## split training and testing data
train_X, val_X, train_y, val_y = train_test_split(X, y, test_size=0.2, shuffle=False)
print("------- TRAINING DATA -------")
cpy = train_X.copy()
cpy['bikes_available'] = train_y
print(cpy)
print("------- VALIDATION DATA -------")
cpy = val_X.copy()
cpy['bikes_available'] = val_y
print(cpy)
print()

## test on different models
## also printing out how much time each takes for comparison

start = time.perf_counter()
decision_tree(train_X, train_y, val_X, val_y)
end = time.perf_counter()
print(f"Elapsed Time: {end - start:0.2f} seconds")

start = time.perf_counter()
random_forest(train_X, train_y, val_X, val_y)
end = time.perf_counter()
print(f"Elapsed Time: {end - start:0.2f} seconds")

start = time.perf_counter()
xgboost(train_X, train_y, val_X, val_y)
end = time.perf_counter()
print(f"Elapsed Time: {end - start:0.2f} seconds")

# conn.close()
