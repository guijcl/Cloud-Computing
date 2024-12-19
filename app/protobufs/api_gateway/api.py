import os
from music_pb2 import *
from artist_pb2 import *
from account_pb2 import *
import grpc
import json
from grpc_interceptor import ExceptionToStatusInterceptor
from flask import Flask, jsonify, request, url_for, abort, g

from music_pb2_grpc import MusicsStub
from artist_pb2_grpc import ArtistStub
from account_pb2_grpc import AccountStub
from grpc_interceptor.exceptions import NotFound


#with open("api.key", "rb") as fp:
#    api_key = fp.read()
#with open("api.pem", "rb") as fp:
#    api_cert = fp.read()
#with open("ca.pem", "rb") as fp:
#    ca_cert = fp.read()
    
#creds = grpc.ssl_channel_credentials(ca_cert, api_key, api_cert)


#musics_channel = grpc.secure_channel(f"{musics_host}:50051",creds) #funciona

musics_host = os.getenv("MUSICS_HOST", "34.118.24.157") #goncalo 
musics_channel = grpc.insecure_channel(f"{musics_host}:50051")
musics_client = MusicsStub(musics_channel)

#artists_host = os.getenv("ARTISTS_HOST", "130.211.212.130") #tope
artists_host = os.getenv("ARTISTS_HOST", "34.118.115.123") #goncalo
artists_channel = grpc.insecure_channel(f"{artists_host}:50055")
artists_client = ArtistStub(artists_channel)

#accounts_host = os.getenv("ACCOUNTS_HOST", "34.70.169.245") #tope
accounts_host = os.getenv("ACCOUNTS_HOST", "34.116.253.35") #goncalo
accounts_channel = grpc.insecure_channel(f"{accounts_host}:50052")
accounts_client = AccountStub(accounts_channel)

# MUSIC


def GetMusic(musicName):

    request = GetMusicRequest(
        name=musicName
    )

    print("Request - Find music by name:", musicName)

    music = musics_client.GetMusic(request)

    print(music)

    MusicResponse = {
        "music_id": music.music_id,
        "type": music.type,
        "name": music.name,
        "streams": music.streams,
    }

    return MusicResponse


def GetTrendingMusics(date, trend):

    request = GetTrendingMusicsRequest(
        date=date,
        trend=trend
    )

    musics = musics_client.GetTrendingMusics(request)

    result = []

    for music in musics.music:
        MusicResponse = {
            "music_id": music.music_id,
            "type": music.type,
            "name": music.name,
            "streams": music.streams,
        }
        
        result.append(MusicResponse)

    return result


def GetTrendingMusicsByCountry(date, trend, country):

    request = GetTrendingMusicsByCountryRequest(
        date=date,
        trend=trend,
        country=country
    )

    musics = musics_client.GetTrendingMusicsByCountry(request)

    result = []

    for music in musics.music:
        MusicResponse = {
            "music_id": music.music_id,
            "type": music.type,
            "name": music.name,
            "streams": music.streams,
        }

        result.append(MusicResponse)

    return result


def GetTop200Musics(date):

    request = GetTop200MusicsRequest(
        date=date,

    )

    musics = musics_client.GetTop200Musics(request)

    result = []

    for music in musics.music:
        MusicResponse = {
            "music_id": music.music_id,
            "type": music.type,
            "name": music.name,
            "streams": music.streams,
        }
        result.append(MusicResponse)

    return result


def GetTop200MusicsByCountry(date, country):

    request = GetTop200MusicsByCountryRequest(
        date=date,
        country=country
    )

    musics = musics_client.GetTop200MusicsByCountry(request)

    result = []

    for music in musics.music:
        MusicResponse = {
            "music_id": music.music_id,
            "type": music.type,
            "name": music.name,
            "streams": music.streams,
        }

        result.append(MusicResponse)

    return result


def GetViral50Musics(date):
    
    request = GetViral50MusicsRequest(
        date=date
    )

    musics = musics_client.GetViral50Musics(request)

    result = []

    for music in musics.music:
        MusicResponse = {
            "music_id": music.music_id,
            "type": music.type,
            "name": music.name,
            "streams": music.streams,
        }

        result.append(MusicResponse)

    return result


def GetViral50MusicsByCountry(date, country):

    musics_trending = GetViral50MusicsByCountryRequest(
        date=date,
        country=country
    )

    musics = musics_client.GetViral50MusicsByCountry(musics_trending)

    result = []

    for music in musics.music:
        MusicResponse = {
            "music_id": music.music_id,
            "type": music.type,
            "name": music.name,
            "streams": music.streams,
        }

        result.append(MusicResponse)

    return result

# ARTIST


def GetArtistMusic(name):
    request = GetArtistMusicRequest(
        name=name
    )

    print("Request - Find musics of the artist:", name)
    name = artists_client.GetArtistMusic(request)
    ret = []
    for r in name.musics:
        MusicResponses = {
            "music_id": r.music_id,
            #"type": r.type,
            "name": r.name,
            "streams": r.streams,
        }
        ret.append(MusicResponses)

    return ret


def GetTop20Artist(date):
    request = GetTop20ArtistRequest(
        date=date
    )

    print("Request - Find top 20 artists in the day:", date)

    artist = artists_client.GetTop20Artist(request)

    ret = []
    for r in artist.artists:
        ArtistResponse = {
            #"artist_id": r.id,
            "name": r.name
        }
        ret.append(ArtistResponse)

    return ret


def GetViral10Artist(date):
    request = GetViral10ArtistRequest(
        date=date
    )

    print("Request - Find viral 10 artists in the day:", date)

    artist = artists_client.GetViral10Artist(request)

    ret = []
    for r in artist.artists:
        ArtistResponse = {
            #"artist_id": r.id,
            "name": r.name
        }
        ret.append(ArtistResponse)

    return ret


def GetArtistWithLetter(string):
    request = GetArtistWithLetterRequest(
        string_char=string
    )

    print("Request - Find musics of the artists started with the letters:", string)
    artist = artists_client.GetArtistWithLetter(request)
    ret = []
    for r in artist.artists:
        ArtistResponse = {
            #"artist_id": r.id,
            "name": r.name
        }
        ret.append(ArtistResponse)

    return ret

# ACCOUNT

def GetUserByName(username):
    request = UserRequest(
        username=username
    )
    print("Request - get user by name:", username)

    account = accounts_client.GetUserByName(request)
  
    likes = []

    for music in account.likes.music:
        AccountMusicResponse = {
            "music_name": music.name
        }
        likes.append(AccountMusicResponse)

    listenLater = []
    for music in account.listenLater.music:
        AccountMusicResponse = {
            "music_name": music.name
        }
        listenLater.append(AccountMusicResponse)

    response = {"username": account.username, "likes:": likes,"listenLater:" : listenLater}

    return response


def CreateUser(username):
    request = CreateUserRequest(
        username=username
    )
    print("Request - create user:", username)

    account = accounts_client.CreateUser(request)

    Success = {
        "success": account.success
    }
    return Success


def DeleteUser(username):
    request = CreateUserRequest(
        username=username
    )

    print("Request - create user:", username)

    account = accounts_client.DeleteUser(request)

    Success = {
        "success": account.success
    }
    return Success

def ListenLater(username, musicname):
    user = username
    music = musicname

    print("Request -  listen later:", music)

    account_request = GetMusicRequestAccount(username=user, musicname=music)
    account = accounts_client.ListenLater(account_request)
    Success = {
        "success": account.success
    }

    return Success


def Like(username, musicname):

    user = username
    music = musicname

    print("Request - like:", music)

    account_request = GetMusicRequestAccount(username=user, musicname=music)
    account = accounts_client.Like(account_request)

    Success = {
        "success": account.success
    }
    return Success





def LoginUser(self, request, context):
    user = request.username

    print("Request -  login user by name:", user)

    if user is None:
        return NotFound("No user Input")

    account_request = UserRequest(username=user)
    account = accounts_client.LoginUser(account_request)

    return account


def LogoutUser(self, request, context):
    user = request.username

    print("Request -  logout user by name:", user)

    if user is None:
        return NotFound("No user Input")

    account_request = UserRequest(username=user)
    account = accounts_client.LogoutUser(account_request)

    return account

