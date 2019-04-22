# CREATE KEYSPACE
keyspace_create = "CREATE KEYSPACE IF NOT EXISTS darien_cassandra \
                WITH REPLICATION = \
                { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }"
# DROP TABLES
session_info_drop = "DROP TABLE IF EXISTS session_info"
user_activity_drop = "DROP TABLE IF EXISTS user_activity"
user_history_drop = "DROP TABLE IF EXISTS user_history"

# CREATE TABLES

session_info_create = "CREATE TABLE IF NOT EXISTS session_info \
                    (artist text, \
                    song text, \
                    length float, \
                    sessionId int, \
                    itemInSession int, \
                    PRIMARY KEY (sessionId, itemInSession));"

user_activity_create = "CREATE TABLE IF NOT EXISTS user_activity \
                    (artist text, \
                    song text, \
                    firstName text, \
                    lastName text, \
                    userId int, \
                    sessionId int, \
                    itemInSession int, \
                    PRIMARY KEY (userId, sessionId, itemInSession)) \
                    WITH CLUSTERING ORDER BY (sessionId ASC, itemInSession DESC);"

user_history_create = "CREATE TABLE IF NOT EXISTS user_history \
                    (firstName text, \
                    lastName text, \
                    song text, \
                    userId int, \
                    PRIMARY KEY (song, userId));"


# INSERT RECORDS

session_info_insert = "INSERT INTO session_info \
                    (artist, song, length, sessionId, itemInSession) \
                    VALUES (%s, %s, %s, %s, %s);"

user_activity_insert = "INSERT INTO user_activity \
                    (artist, song, firstName, lastName, userId, sessionId, itemInSession) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s);"

user_history_insert = "INSERT INTO user_history \
                    (firstName, lastName, song, userId) \
                    VALUES (%s, %s, %s, %s);"


# VERIFY QUERIES

session_info_find = "SELECT artist, song, length \
                    from session_info \
                    WHERE sessionId = %s AND itemInSession =%s"

user_activity_find = "SELECT firstName, lastName, itemInSession, artist, song \
                    from user_activity \
                    WHERE userId = %s AND sessionId = %s"

user_history_find = "SELECT userId, firstName, lastName \
                    from user_history \
                    WHERE song = %s"


create_table_queries = [session_info_create, user_activity_create, user_history_create]
drop_table_queries = [session_info_drop, user_activity_drop, user_history_drop]


