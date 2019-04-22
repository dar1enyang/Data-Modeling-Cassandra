# Introduction

NoSQL databases are not a direct replacement for an relational database management system (RDBMS).  

If you like to learn more about data modeling in SQL([My data modeling project using PostgreSQL](https://github.com/dar1enyang/Data-Modeling-PostgreSQL))

For the following needs, NoSQL is a better match than an RDBMS.

+ **Need high Availability in the data**: Indicates the system is always up and there is no downtime
+ **Have Large Amounts of Data**
+ **Need Linear Scalability**: The need to add more nodes to the system so performance will increase linearly
+ **Low Latency**: Shorter delay before the data is transferred once the instruction for the transfer has been received.
+ **Need fast reads and write**

---

Knowing how customers interact with the platform via app or website is very important to the music streaming business. 

The analytics people are particularly interested in understanding the following questions:

+ Give the artist, song title and song's length in the music app history that was heard during  a specific session
+ Give the artist, song title(sorted by itemInSession) and user info based on the specific userid and session
+ Give every user info in the music app history who listened to a specific song

Currently, there is no easy way to query the data to generate the results, since the data reside in a directory of CSV files on user activity on the app.

# Project Objective

Design and structure data to make it available to the others in the team. So they can make use of it easily.

Throughout this project, I have completed the following tasks:

1. Created an Apache Cassandra database which can create queries on song play data to answer the questions mentioned above
2. Minimized partition reads by modeling the data to fit target queries
3. Built an ETL pipeline that transfers data from a set of CSV files within a directory to create a streamlined CSV file to model and insert data into Apache Cassandra tables.

# Technology 

<p align="middle">
  <img img height="270" width="400" src="https://ws3.sinaimg.cn/large/006tNc79ly1g2btcxl58xj318r0u0tgv.jpg" />
  <img img height="270" width="500" src="https://ws2.sinaimg.cn/large/006tNc79ly1g2bsv06jf3j30gp05njtd.jpg" />




# Explore the datasets

##### 1. Song Dataset

The first dataset is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. For example, here are filepaths to two files in this dataset.

```txt
song_data/A/B/C/TRABCEI128F424C983.json
song_data/A/A/B/TRAABJL12903CDCF1A.json
```

And below is an example of what a single song file, TRAABJL12903CDCF1A.json, looks like.

```json
{"num_songs": 1, 
 "artist_id": "ARJIE2Y1187B994AB7", 
 "artist_latitude": null, 
 "artist_longitude": null, 
 "artist_location": "", 
 "artist_name": "Line Renaud", 
 "song_id": "SOUPIRU12A6D4FA1E1", 
 "title": "Der Kleine Dompfaff", 
 "duration": 152.92036, 
 "year": 0}
```

##### 2. Log Dataset

The second dataset consists of log files in JSON format. These describe app activity logs from a music streaming app based on specified configurations.

The log files in the dataset are partitioned by year and month. 

For example, here are filepaths to two files in this dataset.

```txt
log_data/2018/11/2018-11-12-events.json
log_data/2018/11/2018-11-13-events.json
```

And below is an example of what the data in a log file, 2018-11-12-events.json, looks like.

![](https://ws3.sinaimg.cn/large/006tNc79ly1g2bsvkkb18j316d0cstbp.jpg)

# Methodology 

### Star Schema Design - Optimized for queries on song play analysis

![](https://ws2.sinaimg.cn/large/006tNc79ly1g2bsvrjxy1j30hg0c2aax.jpg)



# How to use this project

How to install and set up Postgres locally in case you want to follow along with the project on your local machine. This [link](https://www.codementor.io/engineerapart/getting-started-with-postgresql-on-mac-osx-are8jcopb) provides it for MacOs. It goes through configuring Postgres, creating users, creating databases using the psql utility.

Perform ETL development in `etl.ipynb` and `test.ipynb`

1. Run `create_tables.py` to create database and tables 

   (Alter queries if you want in `sql_queries.py`)

2. Run `etl.py` to perform the complete ETL pipeline
