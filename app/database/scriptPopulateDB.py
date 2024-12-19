# import the MongoClient class
from pymongo import MongoClient, errors

# global variables for MongoDB host (default port is 27017)
#DOMAIN = 'localhost'
DOMAIN = '34.77.106.168'
PORT = 27017

print("Connecting to database.....")

    # try to instantiate a client instance
client = MongoClient(
        host = [ str(DOMAIN) + ":" + str(PORT) ],
        serverSelectionTimeoutMS = 5000, # 5 second timeout
        username = "root",
        password = "root",
    )

db = client["database"]

# drop everything in there
db.drop_collection("music")

db = db["music"]

import csv

file = open("charts_0.csv")

csvreader = csv.reader(file,delimiter=',')

# store the headers in a separate variable,
# move the reader object to point on the next row
headings = next(csvreader)

listOfSongs = []

for row in csvreader:

    song = {
        'title' : row[0].strip(),
        'rank': row[1].strip(),
        'date' : row[2].strip(),
        'artist': row[3].strip(),
        'url': row[4].strip(),
        'region': row[5].strip(),
        'chart': row[6].strip(),
        'trend': row[7].strip(),
        'streams': row[8].strip(),
    }

    # append
    listOfSongs.append(song)

db.insert_many(listOfSongs)
    
file.close()

print('Done')