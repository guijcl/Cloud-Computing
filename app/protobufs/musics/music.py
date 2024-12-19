from distutils.log import debug
from queue import Empty
import grpc
from concurrent import futures

from pymongo import MongoClient
from bson.objectid import ObjectId

import music_pb2_grpc

from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from prometheus_client import start_http_server, Summary


from music_pb2 import * 
# global variables for MongoDB host (default port is 27017)
DOMAIN = '34.118.107.95'
PORT = 27017

print("Connecting to database.....")

    # try to instantiate a client instance
client = MongoClient(
        host = [ str(DOMAIN) + ":" + str(PORT) ],
        serverSelectionTimeoutMS = 3000, # 3 second timeout
        username = "root",
        password = "root",
    )


db = client["database"]
db = db["music"]


db2 = client["database"]
# drop everything in there
db2 = db2["music"]

class MusicService(music_pb2_grpc.MusicsServicer):

    # Function to get the song given its name
    def GetMusic(self, request, context):

        #Query to find the song given the name
        response = db.find_one({ "title": (request.name)})

        #In case the song is not on the chart
        if response is None:
            raise NotFound("Music not found")

        #Returns the details of the song
        return music_to_response(response)
    

    # Function to get the trending songs given a certain date and trend
    # Date: Its format should be "yyyy-MM-dd"
    # Trend: Possible types are "MOVE_UP", "MOVE_DOWN" and "SAME_POSITION"
    def GetTrendingMusics(self, request, context):

        #Query to find all songs given some restraints
        response = db.find({"date": request.date, "trend": request.trend})

        #In case there is no songs, the response should be that it didn't find any songs
        if response is None:
            return NotFound("No songs were found in this search")

        #For each song, transform it into a "music" object
        response = [music_to_response(music) for music in response]

        #Return the list of musics
        return MusicListResponse(music = response)


    # Function to get the trending songs given a certain date, trend and country
    # Date: Its format should be "yyyy-MM-dd"
    # Trend: Possible types are "MOVE_UP", "MOVE_DOWN" and "SAME_POSITION"
    # Country: Full name of the country
    def GetTrendingMusicsByCountry(self, request, context):

        #Query to find all songs given some restraints
        response = db.find({ "date": request.date, 
                                    "trend": request.trend, 
                                    "region": request.country})

        #In case there is no songs, the response should be that it didn't find any songs
        if response is None:
            return NotFound("No songs were found in this search")

        #For each song, transform it into a "music" object
        response = [music_to_response(music) for music in response]

        #Return the list of musics
        return MusicListResponse(music = response)


    # Function to get the top200 songs given a certain date
    # Date: Its format should be "yyyy-MM-dd"
    def GetTop200Musics(self, request, context):

        #Query to find the songs given the restraints
        response = db.find({"date": request.date, "chart": "top200"})

        #In case there is no songs, the response should be that it didn't find any songs
        if response is None:
            return NotFound("No songs were found in this search")

        #For each song, transform it into a "music" object
        response = [music_to_response(music) for music in response]

        #Return the list of musics
        return MusicListResponse(music = response)


    # Function to get the top200 songs given a certain date and country
    # Date: Its format should be "yyyy-MM-dd"
    # Country: Full name of the country
    def GetTop200MusicsByCountry(self, request, context):

        #Query to find the songs given the restraints
        response = db.find({"date": request.date, "region": request.country, "chart": "top200"})
        
        #In case there is no songs, the response should be that it didn't find any songs
        if response is None:
            return NotFound("No songs were found in this search")

        #For each song, transform it into a "music" object
        response = [music_to_response(music) for music in response]

        #Return the list of musics
        return MusicListResponse(music = response)

    # Function to get the viral50 songs given a certain date
    # Date: Its format should be "yyyy-MM-dd"
    def GetViral50Musics(self, request, context):
        
        #Query to find the songs given the restraints
        response = db.find({"date": request.date, "chart": "viral50"})
        
        #In case there is no songs, the response should be that it didn't find any songs
        if response is None:
            return NotFound("No songs were found in this search")

        #For each song, transform it into a "music" object
        response = [music_to_response(music) for music in response]

        #Return the list of musics
        return MusicListResponse(music = response)

    # Function to get the viral50 songs given a certain date and country
    # Date: Its format should be "yyyy-MM-dd"
    # Country: Full name of the country
    def GetViral50MusicsByCountry(self, request, context):

        #Query to find the songs given the restraints
        response = db.find({"date": request.date, "region": request.country, "chart": "viral50"})
        #In case there is no songs, the response should be that it didn't find any songs
        if response is None:
            return NotFound("No songs were found in this search")

        #For each song, transform it into a "music" object
        response = [music_to_response(music) for music in response]

        #Return the list of musics
        return MusicListResponse(music = response)


    #Not working
    def GetMostStreamedMusics(self, request, context):
        response = list(db.find({"date": request.date, "chart": "top200"}))
        
        #In case there is no songs, the response should be that it didn't find any songs
        if response is None:
            return NotFound("No songs were found in this search")

        #Sort and get 5 of the most streamed songs
        response = response.sort(key=lambda x: x[0]['streams'],reverse=True)

        #For each song, transform it into a "music" object
        response = [music_to_response(music) for music in response]

        #Return the list of musics
        return MusicListResponse(music = response)


def music_to_response(response):

    music = MusicResponse (
        music_id = str(response["_id"]),
        name = str(response["title"]),  
        type = str(response["chart"]),
        streams = int(response["streams"])    
        
         
    )

    return music   

REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

@REQUEST_TIME.time()  

def serve():
        interceptors = [ExceptionToStatusInterceptor()]
        server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
        )
        music_pb2_grpc.add_MusicsServicer_to_server(
            MusicService(), server
        )

        #with open("music.key", "rb") as fp:
        #    music_key = fp.read()
        #with open("music.pem", "rb") as fp:
        #    music_cert = fp.read()
        #with open("ca.pem", "rb") as fp:
        #    ca_cert = fp.read()

        #creds = grpc.ssl_server_credentials(((music_key, music_cert),))

        #creds = grpc.ssl_server_credentials(
        #    [(music_key,music_cert )],
        #    root_certificates=ca_cert) #workload funciona mas handshake protocol error troquei o ca pelo music

        #creds = grpc.ssl_server_credentials(
        #    [(music_key,music_cert)],
        #    root_certificates=ca_cert
        #    )

        #creds = grpc.ssl_server_credentials(
        #    [(music_key, music_cert)],
        #    root_certificates=ca_cert,
        #    require_client_auth=True,
        #)

        

        #server.add_secure_port("[::]:50051", creds) # funciona :D
        
        server.add_insecure_port("[::]:50051")
        server.start()
        server.wait_for_termination()

if __name__ == "__main__":
    #app.run(ssl_context='adhoc') #se tirar ssl_context dara para http  ssl_context='adhoc'
    start_http_server(51051)
    serve()