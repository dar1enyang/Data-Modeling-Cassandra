import pandas as pd
import cassandra
import re
import os
import glob
import numpy as np
import json
import csv
import sys
import os.path
sys.path.append('..')
from query.nosql_queries import *
from create_tables import *

def process_raw_data(filepath, filename):
    """
    Use this filepath to get the data to run event data processing. 

    Parameters:
        filepath : The csv file path resides event data.
        filename : The new file name to store the concatenated data.
    """

    # Get current folder and subfolder event data
    filepath = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + filepath

    # Create a for loop to create a list of files and collect each filepath
    for root, dirs, files in os.walk(filepath):
        
    # join the file path and roots with the subdirectories using glob
        file_path_list = glob.glob(os.path.join(root,'*'))
    
    # get total number of files found
    num_files = len(file_path_list)
    print('{} files found in {}'.format(num_files, filepath))

    # initiating an empty list of rows that will be generated from each file
    full_data_rows_list = [] 
    
    # for every filepath in the file path list 
    for i, datafile in enumerate(file_path_list, 1):

    # reading csv file 
        with open(datafile, 'r', encoding = 'utf8', newline='') as csvfile: 
            # creating a csv reader object 
            csvreader = csv.reader(csvfile) 
            next(csvreader)
            
     # extracting each data row one by one and append it        
            for line in csvreader:
                #print(line)
                full_data_rows_list.append(line) 
            print('{}/{} files processed.'.format(i, num_files))

    # creating a smaller event data csv file called event_datafile_full csv 
    # that will be used to insert data into the Apache Cassandra tables
    csv.register_dialect('myDialect', quoting=csv.QUOTE_ALL, skipinitialspace=True)

    with open(filename, 'w', encoding = 'utf8', newline='') as f:
        writer = csv.writer(f, dialect='myDialect')
        writer.writerow(['artist','firstName','gender','itemInSession','lastName','length',\
                    'level','location','sessionId','song','userId'])
        for row in full_data_rows_list:
            if (row[0] == ''):
                continue
            writer.writerow((row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[12], row[13], row[16]))


def process_session_info(session, filename):
    """
    Use this filepath to get the data to insert data into session_info table. 

    Parameters:
        session : The connection towards current connecting database and for queries executing.
        filename : The csv file resides all event data.
    """

    with open(filename, encoding = 'utf8') as f:
        csvreader = csv.reader(f)
        next(csvreader) # skip header
        for line in csvreader:
            # Execute query: session_info_insert
            try:
                session.execute(session_info_insert, (line[0], line[9], float(line[5]), int(line[8]), int(line[3])))
            except Exception as e:
                print(e)


def process_user_activity(session, filename):
    """
    Use this filepath to get the data to insert data into user_activity table. 

    Parameters:
        session : The connection towards current connecting database and for queries executing.
        filename : The csv file resides all event data.
    """

    with open(filename, encoding = 'utf8') as f:
        csvreader = csv.reader(f)
        next(csvreader) # skip header
        for line in csvreader:
            # Execute query: user_activity_insert
            try:
                session.execute(user_activity_insert, (line[0], line[9], line[1], line[4], int(line[10]), int(line[8]), int(line[3])))
            except Exception as e:
                print(e)


def process_user_history(session, filename):
    """
    Use this filepath to get the data to insert data into user_history table. 

    Parameters:
        session : The connection towards current connecting database and for queries executing.
        filename : The csv file resides all event data.
    """

    with open(filename, encoding = 'utf8') as f:
        csvreader = csv.reader(f)
        next(csvreader) # skip header
        for line in csvreader:
            # Execute query: user_history_find
            try:
                session.execute(user_history_insert, (line[1], line[4], line[9], int(line[10])))
            except Exception as e:
                print(e)
  

def main():
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect('darien_cassandra')

    fileName = 'event_datafile_new.csv'
    process_raw_data(filepath = '/data/event_data', filename = fileName)

    process_session_info(session, fileName)
    process_user_activity(session, fileName)
    process_user_history(session, fileName)
    
    # Close the session and cluster connection
    session.shutdown()
    cluster.shutdown()

if __name__ == "__main__":
    main()