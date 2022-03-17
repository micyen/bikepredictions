# this statement is for Sriya because her shell was being weird
import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages')
#
import pandas as pd
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression

from sqlalchemy import create_engine
from info import USERNAME,PASSWORD,ADDRESS,DBNAME,PORT

def create_remote_connection():
    pymysql_str = ('mysql+pymysql://{username}:{password}@{host}:{port}/{dbname}'
        .format(username=USERNAME,
        password=PASSWORD,
        host=ADDRESS,
        dbname=DBNAME,
        port=PORT))

    cnx = create_engine(pymysql_str)
    return cnx

def create_dataframe(n, table_name):

    # Create remote database connection
    conn = create_remote_connection()

    # Get relevant data, later replace with proper training data query
    station_data = pd.read_sql_query("SELECT * FROM " + table_name, conn)

    # Convert time string to datetime
    station_data['time'] = pd.to_datetime(station_data['time'],
    format = '%Y-%m-%d %H:%M:%S',
    errors = 'coerce')
    station_data = station_data.sort_values(by="time", kind="mergesort")
    # print(station_data)

    # Separate datetime into numerical categories
    station_data['time_year'] = station_data['time'].dt.year
    station_data['time_month'] = station_data['time'].dt.month
    station_data['time_week'] = station_data['time'].dt.isocalendar().week
    station_data['time_day'] = station_data['time'].dt.day
    station_data['time_dayofweek'] = station_data['time'].dt.dayofweek
    station_data['time_hour'] = station_data['time'].dt.hour
    station_data['time_minute'] = station_data['time'].dt.minute

    # See which numerical columns are most important for predicting bike availability
    df = station_data.iloc[:,[0,1,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,29,30,31,32,33,34,35]]

    # Convert empty spaces and non-numeric entries to NaN except events colujmn
    cols = df.columns.drop('events')
    df[cols] = df[cols].apply(pd.to_numeric, errors='coerce', downcast='float')

    # Drop rows that contain non-numbers (some cells have 'T' or blank), except events column
    df.dropna(subset = [n for n in df if n != 'events'], inplace=True)

    X_ = df.iloc[:,[0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]]
    y = df.iloc[:,1]
    # numericize the categorical data (events) using one-hot encoding
    X = pd.get_dummies(X_, columns = ['events'], prefix='event')

    # Define feature selection w/ Pearson's Correlation Coefficient
    fs = SelectKBest(score_func=f_regression, k="all")

    # Apply feature selection
    X_selected = fs.fit(X, y)
    dfscores = pd.DataFrame(X_selected.scores_)
    dfcolumns = pd.DataFrame(X.columns)

    # Combine dataframes
    featureScores = pd.concat([dfcolumns,dfscores],axis=1)
    featureScores.columns = ['Variable', 'Score']

    # Print top 30 best scores
    print(featureScores.nlargest(30,'Score'))
    features = (featureScores.nlargest(n,'Score')['Variable']).sort_index()
    print(features)
    dataframe = X[features]
    #dataframe['time'] = station_data.time
    # print(station_data)
    return conn, dataframe, station_data.bikes_available
