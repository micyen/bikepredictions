import pandas as pd
import sqlite3

# Create a SQL connection to our SQLite database
con = sqlite3.connect("archive/database.sqlite")
# df = pd.read_sql_query("SELECT * FROM weather where date like '9/%/2013'", con)
# df = pd.read_sql_query("SELECT DISTINCT zip_code FROM weather ", con)
# df2 = pd.read_sql_query("SELECT DISTINCT city FROM station ", con)


def executeQuery(query):
    cur = con.cursor()
    cur.executescript(query)
    con.commit()
    return cur.fetchall()


def readQuery(query):
    #cursor = con.cursor()
    result = pd.read_sql_query(query, con)
    return result


def createZipCityTable():
    cur = con.cursor()
    cmd_citytable = "CREATE TABLE  city_info(zip_code int, city varchar(255));"
    

    con.execute(cmd_citytable)

    cmd_insert0 = "INSERT INTO city_info(zip_code, city) VALUES (94107, 'San Francisco')"
    cmd_insert1 = "INSERT INTO city_info(zip_code, city) VALUES (94063, 'Redwood City')"
    cmd_insert2 = "INSERT INTO city_info(zip_code, city) VALUES (94301, 'Palo Alto')"
    cmd_insert3 = "INSERT INTO city_info(zip_code, city) VALUES (94041, 'Mountain View')"
    cmd_insert4 = "INSERT INTO city_info(zip_code, city) VALUES (95113, 'San Jose')"

    cur.execute(cmd_insert0)
    cur.execute(cmd_insert1)
    cur.execute(cmd_insert2)
    cur.execute(cmd_insert3)
    cur.execute(cmd_insert4)

    # Be sure to close the connection
    con.commit()

#### WEATHER TABLE #####

# update the dates to be YYYY-MM-DD
def update_dates():

    cur = con.cursor()

    # for the form M/DD/YYYY
    cur.execute("UPDATE WeatherCity \
                    SET date = substr(date, 6, 4) || '-' || '0' ||\
                                substr(date, 1, 1) || '-' || \
                                substr(date, 3, 2) \
                                WHERE date LIKE '_/__/____'")
    con.commit()
    # for the form M/D/YYYY
    cur.execute("UPDATE WeatherCity \
                    SET date = substr(date, 5, 4) || '-' || '0' ||\
                                substr(date, 1, 1) || '-' || '0' ||\
                                substr(date, 3, 1) \
                                WHERE date LIKE '_/_/____'")
    con.commit()
    # for the form MM/D/YYYY
    cur.execute("UPDATE WeatherCity \
                    SET date = substr(date, 6, 4) || '-' || \
                                substr(date, 1, 2) || '-' || '0' || \
                                substr(date, 4, 1) \
                                WHERE date LIKE '__/_/____'")
    con.commit()
    # for the form MM/DD/YYYY
    cur.execute("UPDATE WeatherCity \
                    SET date = substr(date, 7, 4) || '-' || \
                                substr(date, 1, 2) || '-' || \
                                substr(date, 4, 2) \
                                WHERE date LIKE '__/__/____'")
    con.commit()
    print("weather dates are updated.")
    cursor = con.execute("SELECT date FROM WeatherCity LIMIT 5")
    for row in cursor:
        print(row)


def dropJoinedTables():
    executeQuery("DROP TABLE city_info")
    executeQuery("DROP TABLE station_zip")
    executeQuery("DROP TABLE StationZipCity")
    executeQuery("DROP TABLE status_zip_join")
    executeQuery("DROP TABLE WeatherCity")
    executeQuery("DROP TABLE StatusWeatherJoin")

def createNecessaryTables():
    createZipCityTable()
    cmd_join = "SELECT * FROM weather LEFT JOIN city_info ON weather.zip_code = city_info.zip_code"
    cmd_table = "CREATE TABLE weather_city AS " + cmd_join + ";" 
    executeQuery(cmd_table)

    cmd_join2 = "SELECT id, name, lat, long, dock_count, installation_date, city_info.* FROM station LEFT JOIN city_info ON station.city = city_info.city;"
    cmd_table2 = "CREATE TABLE StationZipCity AS " +cmd_join2+ ";"
    executeQuery(cmd_table2)


    cmd_status_zip_join = ("CREATE TABLE status_zip_join AS SELECT status.*, StationZipCity.zip_code FROM status LEFT JOIN StationZipCity on StationZipCity.id = status.station_id")
    executeQuery(cmd_status_zip_join)

    # clean weather_city
    cmd_table3 = "CREATE TABLE WeatherCity AS SELECT date, max_temperature_f, mean_temperature_f, min_temperature_f,max_dew_point_f, mean_dew_point_f, min_dew_point_f, max_humidity,mean_humidity, min_humidity, max_sea_level_pressure_inches, mean_sea_level_pressure_inches, min_sea_level_pressure_inches, max_visibility_miles, mean_visibility_miles, min_visibility_miles, max_wind_Speed_mph, mean_wind_speed_mph, max_gust_speed_mph, precipitation_inches, cloud_cover, events, wind_dir_degrees, zip_code FROM weather_city  "
    executeQuery(cmd_table3)

    #update weather dates
    update_dates()

    cmd_weather_status_join = "SELECT status_zip_join.station_id, status_zip_join.bikes_available, status_zip_join.docks_available, status_zip_join.time , WeatherCity.* FROM status_zip_join LEFT JOIN WeatherCity ON status_zip_join.zip_code = WeatherCity.zip_code WHERE WeatherCity.date=DATE( REPLACE(status_zip_join.time, '/', '-')  )"
    cmd_table4 = "CREATE TABLE StatusWeatherJoin AS " + cmd_weather_status_join
    executeQuery(cmd_table4)