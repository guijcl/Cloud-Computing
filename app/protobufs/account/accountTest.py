from json.tool import main
import os

import grpc

from account_pb2 import *
from account_pb2_grpc import AccountStub


account_host = os.getenv("ACCOUNT_HOST", "34.116.253.35") 
account_channel = grpc.insecure_channel(f"{account_host}:50052")
account_client = AccountStub(account_channel)


def CreateUser (username):
    print("Request - Create a User with the name : " + username)
    account_request = CreateUserRequest(username=username)

    account_response = account_client.CreateUser(account_request)

    return account_response

def GetUser (username):
    print("Request - Get User with the name: "+ username)
    account_request = UserRequest(username=username)

    account_response = account_client.GetUserByName(account_request)

    return account_response

def UserLikesMusic (username, musicname):
    print("Request - The User with the name "+ username +" likes a Music with the name "+ musicname)
    account_request = GetMusicRequestAccount(username= username , musicname = musicname)

    account_response = account_client.Like(account_request)

    return account_response

def UserListenLaterMusic (username, musicname):
    print("Request - The User with the name "+ username + " put the music " + musicname + " as a Listen Later music")
    account_request = GetMusicRequestAccount(username= username , musicname = musicname)

    account_response = account_client.ListenLater(account_request)

    return account_response

def GetUserLikedMusics (username):
    print("Request - Liked Musics of the user " + username)
    
    account_request = UserRequest(username=username)

    account_response = account_client.ListenLater(account_request)

    return account_response

   
def GetUserListenLaterMusics (username):
    print("Request - Listen Later Musics of the user " + username)
    
    account_request =  UserRequest(username=username)
    account_response = account_client.ListenLater(account_request)

    return account_response


if __name__ == "__main__":

#######################################################    
    #print("Request - The User with the name "+ username +" likes a Music with the name "+ musicname)
    #account_request = GetMusicRequestAccount(username= "Sky2" , musicname = "Faded")

    #account_response = account_client.ListenLater(account_request)

    account_request = UserRequest(username="Sky2")

    account_response = account_client.GetUserByName(account_request)

    print(account_response)

