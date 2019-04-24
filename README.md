# Introduction

NoSQL databases are not a direct replacement for a relational database management system (RDBMS).  

If you like to learn more about data modeling in SQL([My data modeling project using PostgreSQL](https://github.com/dar1enyang/Data-Modeling-PostgreSQL))

For the following needs, NoSQL is a better match than an RDBMS.

+ **Need High Availability in the data**: Indicates the system is always up and there is no downtime
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
  <img img  src="https://ws2.sinaimg.cn/large/006tNc79ly1g2bsv06jf3j30gp05njtd.jpg" />


# Explore the dataset

For this project, you'll be working with one dataset: `event_data`. The directory of CSV files partitioned by date. Here are examples of file paths to two files in the dataset:

```txt
event_data/2018-11-08-events.csv
event_data/2018-11-09-events.csv
```

Below is the screenshot of `2018-11-01-events.csv`:

![](https://ws3.sinaimg.cn/large/006tNc79ly1g2bv8lpy9dj32260iehas.jpg)

I extracted the following features(11 total): 

- artist 
- firstName of user
- gender of user
- item number in the session
- last name of the user
- length of the song
- level (paid or free song)
- location of the user
- sessionId
- song title
- userId

The image below is a screenshot of what the denormalized data  appear like: 

![](https://ws3.sinaimg.cn/large/006tNc79ly1g2bv4vvcl7j319i0enajs.jpg)



# Methodology 

### Schema Design - Minimized partition reads by modeling the data to fit target queries

## Schema Design
The special thing in schema designing in Apache Cassandra is to 'think queries first'.

In order to answer the proposed questions, following three tables were created: 

1. session_info

   + Give the artist, song title and song's length in the music app history that was heard during  a specific session

<p align="center">
  <br>Partition Keys: (sessionId, itemInSession) <br>
    <img src="https://ws2.sinaimg.cn/large/006tNc79ly1g2bvj1de8dj304r03ea9y.jpg" />
</p>   


2. user_acitivity

   + Give the artist, song title(sorted by itemInSession) and user info based on the specific userid and session

<p align="center">
  <br>Partition Keys: (userId, sessionId) / Clustering Column: itemInSession <br>
    <img src="https://ws3.sinaimg.cn/large/006tNc79ly1g2bvjbg53fj304x044aa0.jpg" />
</p>



3. user_history

   + Give every user info in the music app history who listened to a specific song

<p align="center">
  <br>Partition Keys: (song, userId) <br>
    <img src="https://ws4.sinaimg.cn/large/006tNc79ly1g2bvjgmv7sj304p02tjr9.jpg" />
</p>





# How to use this project

In order to run this project locally, please follow the documentation.

**Installing Apache Cassandra to run locally on your machine:**
[Cassandra Documentation](http://cassandra.apache.org/doc/latest/getting_started/installing.html)

## Go Directories

### `/func`

Main applications for this project

Performed ETL development in `etl.ipynb` and `validate_tables.ipynb`

### `/query`

All queries for this project

### `/data`

All data for this project

1. Run `func/create_tables.py` to create database and tables 

   (Alter queries if you want in `query/nosql_queries.py`)

2. Run `func/etl.py` to perform the complete ETL pipeline
