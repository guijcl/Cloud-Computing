from concurrent import futures
from itertools import count
from pickle import FALSE, TRUE
import grpc
import artist_pb2_grpc
import music_pb2_grpc
from prometheus_client import start_http_server, Summary
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask
app = Flask(__name__)

from artist_pb2 import *
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


def health():
    return HTTPResponse(status=200)

class ArtistSearchService(artist_pb2_grpc.ArtistServicer):

    # get artist musics
    def GetArtistMusic(self, request, context):
        print("Get Artist Musics")
        
        
        musicListFull = db.find({ "artist": request.name}) 
        #musicListFull2 = db.find({ "date": "2017-01-01"}) 

        #musicListFull2=musicListFull2.extend(musicListFull)
        

        musicList =[]
        for artista in musicListFull:
            if str(artista.get("artist")) == str(request.name):
             musicList.append(artista)

        if musicList is None:
            return NotFound("No songs from that artist were found in this search")       

        musicTemp = []
        i = 1

        for music in musicList:

            for mus in musicTemp:
                if str(music.get("title")) == str(mus.get("title")):
                    i = 0

            if i == 1:
                musicTemp.append(music)
            i = 1
        
        musicTemp = [music_to_response(music) for music in musicTemp]
    
        return MusicListResponses(musics=musicTemp)
        

    # get top  artist of the top 200 muscis: artist that are on top200 on a certain date
    def GetTop20Artist(self, request, context):
        topArtist = db.find({"date": request.date, "chart": "top200"})

        if topArtist is None:
            return NotFound("No Artists were found in this search")
    
    #remoçao de duplicados
        artistTemp = []
        i = 1
        for artist in topArtist:
            for art in artistTemp:
                if str(artist.get("artist")) == str(art.get("artist")):
                    i = 0
            if i == 1:
                artistTemp.append(artist)
            i = 1
        
        artistTemp = [artist_to_response(artist) for artist in artistTemp]


        return ArtistListResponse(artists=artistTemp)


    

    # get viral 10 artist of the viral 50 muscis: artist that are on viral50 on a certain date
    
    def GetViral10Artist(self, request, context):
        viralArtist = db.find({"date": request.date, "chart": "viral50"})

        if viralArtist is None:
            return NotFound("No Artists were found in this search")
        
        artistTemp = []
        i = 1
    #remoçao de  duplicados
        for artist in viralArtist:
            for art in artistTemp:
                if str(artist.get("artist")) == str(art.get("artist")):
                    i = 0
            if i == 1:
                artistTemp.append(artist)
            i = 1

            
        artistTemp = [artist_to_response(artist) for artist in artistTemp]

        return ArtistListResponse(artists=artistTemp)

    # get a list of artist with the string
    def GetArtistWithLetter(self, request, context):
        getArtist = db.find({}, {'artist': 1})

        if getArtist is None:
            return NotFound("No songs from that artist were found in this search")

        getArtistTemp = []
        string = str(request.string_char)
        string_size = len(string)

        for artist in getArtist:
            stringArtista = str(artist.get("artist"))
            Firstchar = stringArtista[0:string_size]
            bool = FALSE
            if string == Firstchar:
                bool = TRUE

            if bool == TRUE:
                getArtistTemp.append(artist)

        ArtistTemp = []
        i = 1

        for artist in getArtistTemp:

            for art in ArtistTemp:
                if str(artist.get("artist")) == str(art.get("artist")):
                    i = 0

            if i == 1:
                ArtistTemp.append(artist)
            i = 1

        ArtistTemp = [artist_to_response(artist)
                      for artist in ArtistTemp]
        return ArtistListResponse(artists=ArtistTemp)


def artist_to_response(result):
    artist = ArtistResponse(
        name=str(result["artist"])
    )
    return artist

def artist_to_responseV2(result):
        artist = ArtistResponse(
            name=str(result)
        )
        return artist        

def music_to_response(response):

    music = MusicResponses(
        music_id=str(response["_id"]),
        name=str(response["title"]),
        #type=str(response["chart"]),
        streams=int(response["streams"])
    )

    return music


# Create a metric to track time spent  and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

@REQUEST_TIME.time() 
def serve():
    start_http_server(51055)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    artist_pb2_grpc.add_ArtistServicer_to_server(
        ArtistSearchService(), server
    )
    
    server.add_insecure_port("[::]:50055")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
     serve()
