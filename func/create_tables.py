from cassandra.cluster import Cluster
import sys
sys.path.append('..')
from query.nosql_queries import *
 

def setup_keyspace():
    """
    The function to setup Cassandra environment.

    Returns:
        cluster : The connnection to the Cassandra instance.
        session : The connection towards current connecting database and for queries executing.
    """

    try: 
        # Make a connection to a Cassandra instance in the local machine (127.0.0.1)
        cluster = Cluster(['127.0.0.1']) 
        # To establish connection and begin executing queries, need a session
        session = cluster.connect()
    except Exception as e:
        print(e)

    # Create a Keyspace
    try:
        session.execute(keyspace_create)
    except Exception as e:
        print(e)

    # Set KEYSPACE to the keyspace specified above
    try:
        session.set_keyspace('darien_cassandra')
    except Exception as e:
        print(e)

    return cluster, session


def drop_tables(session):
    """
    The function to drop database if exists.

    Parameters:
        session : The connection towards current connecting database and for queries executing.
    """
    
    for query in drop_table_queries:
        try:
            rows = session.execute(query)
        except Exception as e:
            print(e)


def create_tables(session):
    """
    The function to create database.

    Parameters:
        session : The connection towards current connecting database and for queries executing.
    """
    
    for query in create_table_queries:
        try:
            session.execute(query)
        except Exception as e:
            print(e)


def main():
    
    cluster, session = setup_keyspace()
    drop_tables(session)
    create_tables(session)

    # Close the session and cluster connection
    session.shutdown()
    cluster.shutdown()

if __name__ == "__main__":
    main()