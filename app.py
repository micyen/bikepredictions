import database as database
import pandas as pd
import sqlite3

cmd_query = "SELECT * FROM city_info"

## execute each set of commands one at a time. make sure the ones before current execution instructions set are commented as well as the ones after.
## basically only uncomment one at a time and run the code. 

#######################################################
## CREATE CITY&ZIP TABLE
# database.createZipCityTable()

## merge city and weather data
# cmd_join = "SELECT * FROM weather LEFT JOIN city_info ON weather.zip_code = city_info.zip_code"
# cmd_table = "CREATE TABLE weather_city AS " + cmd_join + ";" 
# database.executeQuery(cmd_table)

## clean weather_city and drop it
# cmd_table3 = "CREATE TABLE WeatherCity AS SELECT date, max_temperature_f, mean_temperature_f, min_temperature_f,max_dew_point_f, mean_dew_point_f, min_dew_point_f, max_humidity,mean_humidity, min_humidity, max_sea_level_pressure_inches, mean_sea_level_pressure_inches, min_sea_level_pressure_inches, max_visibility_miles, mean_visibility_miles, min_visibility_miles, max_wind_Speed_mph, mean_wind_speed_mph, max_gust_speed_mph, precipitation_inches, cloud_cover, events, wind_dir_degrees, zip_code FROM weather_city  "
# database.executeQuery(cmd_table3)
# database.executeQuery("DROP TABLE weather_city")

## update weather dates
#database.update_dates()

## merge station and city_info data
# cmd_join2 = "SELECT id, name, lat, long, dock_count, installation_date, city_info.* FROM station LEFT JOIN city_info ON station.city = city_info.city;"
# cmd_table2 = "CREATE TABLE StationZipCity AS " +cmd_join2+ ";"
# database.executeQuery(cmd_table2)
# print(database.readQuery("select * from StationZipCity limit 10"))

## merge status and StationZipCity data --  will take a bit so watch your cpu/memory/disk usage
# cmd_status_zip_join = ("CREATE TABLE status_zip_join AS SELECT status.*, StationZipCity.zip_code FROM status LEFT JOIN StationZipCity on StationZipCity.id = status.station_id")
# database.executeQuery(cmd_status_zip_join)


## FINAL MERGE - weather, status, and city data -- will take a bit so watch your cpu/memory/disk usage
# cmd_weather_status_join = "SELECT status_zip_join.station_id, status_zip_join.bikes_available, status_zip_join.docks_available, status_zip_join.time , WeatherCity.* FROM status_zip_join LEFT JOIN WeatherCity ON status_zip_join.zip_code = WeatherCity.zip_code WHERE WeatherCity.date=DATE( REPLACE(status_zip_join.time, '/', '-')  )"
# cmd_table4 = "CREATE TABLE StatusWeatherJoin AS " + cmd_weather_status_join
# database.executeQuery(cmd_table4)

cmd_view_tables = "select name from sqlite_master where type= 'table' and name not like 'sqlite_%'"
print(database.readQuery(cmd_view_tables))
print(database.readQuery("select * from StatusWeatherJoin limit 10"))