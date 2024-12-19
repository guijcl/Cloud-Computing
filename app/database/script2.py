# Just to verify if the database was really populated

# import the MongoClient class
from pymongo import MongoClient, errors

# global variables for MongoDB host (default port is 27017)
DOMAIN = '34.77.106.168'
PORT = 27017

myclient = MongoClient(
        host = [ str(DOMAIN) + ":" + str(PORT) ],
        serverSelectionTimeoutMS = 5000, # 5 second timeout
        username = "root",
        password = "root",
    )

db = myclient['database']

cool = db['music']

#para ver a db dos users
#cool = db['account']

#apagar db inteira
#cool.delete_many({})

cursor = cool.find({})

for document in cursor:
    print(document)