import sqlite3 as sq

#### STATUS TABLE #####
def cut_status(conn):

    # cut down the status table
    conn.execute("DELETE FROM status WHERE DATE(REPLACE(time,'/','-')) < " + start)
    conn.commit()

    conn.execute("DELETE FROM status WHERE DATE(REPLACE(time,'/','-')) >= " + end)
    conn.commit()

    # check the first five entries
    cursor = conn.execute("SELECT * FROM status LIMIT 5")

    for row in cursor:
        print(row)

#### WEATHER TABLE #####

# update the dates to be YYYY-MM-DD
def update_dates(conn):

    # for the form M/DD/YYYY
    conn.execute("UPDATE weather \
                    SET date = substr(date, 6, 4) || '-' || '0' ||\
                                substr(date, 1, 1) || '-' || \
                                substr(date, 3, 2) \
                                WHERE date LIKE '_/__/____'")
    conn.commit()
    # for the form M/D/YYYY
    conn.execute("UPDATE weather \
                    SET date = substr(date, 5, 4) || '-' || '0' ||\
                                substr(date, 1, 1) || '-' || '0' ||\
                                substr(date, 3, 1) \
                                WHERE date LIKE '_/_/____'")
    conn.commit()
    # for the form MM/D/YYYY
    conn.execute("UPDATE weather \
                    SET date = substr(date, 6, 4) || '-' || \
                                substr(date, 1, 2) || '-' || '0' || \
                                substr(date, 4, 1) \
                                WHERE date LIKE '__/_/____'")
    conn.commit()
    # for the form MM/DD/YYYY
    conn.execute("UPDATE weather \
                    SET date = substr(date, 7, 4) || '-' || \
                                substr(date, 1, 2) || '-' || \
                                substr(date, 4, 2) \
                                WHERE date LIKE '__/__/____'")
    conn.commit()
    print("weather dates are updated.")
    cursor = conn.execute("SELECT date FROM weather LIMIT 5")
    for row in cursor:
        print(row)

#### GENERAL TABLE ####

# cut down the table to only have dates >= start and < end
def cut_table( conn, start, end, table ):

    total_delete = 0
    # cut down the weather table
    conn.execute("DELETE FROM " + table + " WHERE date < " + start)
    conn.commit()
    total_delete += conn.total_changes

    conn.execute("DELETE FROM " + table + " WHERE date >= " + end)
    conn.commit()
    total_delete += conn.total_changes

    # check the first five entries
    cursor = conn.execute("SELECT date, zip_code FROM " + table + " LIMIT 5")

    for row in cursor:
        print(row)
    print('Total number of rows delete: ' + str(total_delete) )

#### MAIN ####

# set the start and end dates to extract
start = "'2015-07-01'"
end = "'2015-08-01'"

# change the name of the db to connect to HERE
conn = sq.connect('../statweather.db')
print("Connection established.")

# can comment out/in these functions one at a time

### this cuts down the status table
#cut_status(conn, start, end)

### this updates the dates in weather to have the format YYYY-MM-DD
#update_dates(conn)

### this cuts down the given table to the given date range
## NOTE: make sure the date in the given table is properly structured as YYYY-MM-DD
## otherwise it might delete everything which would be painful
## this will cut the table to have dates >= start and < end
table = "StatusWeatherJoin"
cut_table(conn, start, end, table)

conn.close()
print("Connection closed.")
