import os

import grpc

from artist_pb2 import *
from artist_pb2_grpc import ArtistStub

#artists_host = os.getenv("ARTIST_HOST", "34.118.41.105")  #sky
artists_host = os.getenv("ARTIST_HOST", "34.118.115.123")  #tope
artists_channel = grpc.insecure_channel(f"{artists_host}:50055")
artists_client = ArtistStub(artists_channel)

# Test 1
# Test the GetArtistMusic method
def GetArtistMusic(name):

    print("Request - Find music with an Artist named: Adele")
    artists_request = GetArtistMusicRequest(name=name)
    
    artists_response = artists_client.GetArtistMusic(artists_request)
       
    return artists_response

# Test 2
# Test the GetArtistsWithLetter method
def GetArtistsWithLetter(string):

    print("Request - Find list of artist with name started by a specific string")

    artists_request = GetArtistWithLetterRequest(string_char=string) #ver no proto que nome dei ao date

    artists_response = artists_client.GetArtistWithLetter(artists_request)

    return artists_response

# Test 3
# Test the GetTop20Artist method
def GetTop20Artist(date):

    print("Request - Find the top 20 artist that are in the top200Musics, by date")

    artists_request = GetTop20ArtistRequest(date=date)

    artists_response = artists_client.GetTop20Artist(artists_request)

    return artists_response

# Test 4 
# Test the GetViral10Artist method
def GetViral10Artist(date):
    print("Request - Find the viral 10 artist that are in the top200Musics, by date")

    artists_request = GetViral10ArtistRequest(date=date)

    artists_response = artists_client.GetViral10Artist(artists_request)

    return artists_response


if __name__ == "__main__":
################################################
    artists_request = GetArtistMusicRequest(name="Adele")

    artists_response = artists_client.GetArtistMusic(artists_request)

    print(artists_response)

    
