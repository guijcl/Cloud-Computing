import unittest

from dataclasses import dataclass

import grpc

from accountTest import CreateUser, GetUser, GetUserLikedMusics, GetUserListenLaterMusics, UserLikesMusic, UserListenLaterMusic
from account_pb2 import *

@dataclass
class MusicInfo:
    name: str

    @classmethod
    def music_found(cls, data: dict) -> "MusicInfo":
        return cls(
            name=data.name
        )
@dataclass
class UserInfo:
    username: str

    @classmethod
    def user_found(cls, data: dict) -> "UserInfo":
        return cls(
            username=data.username
        )

@dataclass
class ListMusicInfo:
    music: list[MusicInfo]

    @classmethod
    def music_list_found(cls, data: dict) -> "MusicInfo":
        return cls(music=data)

@dataclass
class SucessInfo:
    sucess: bool

    @classmethod
    def sucess_request(cls, data: dict) -> "MusicInfo":
        return cls(sucess=data)

class TestStringMethods(unittest.TestCase):

    def test_CreateUser(self)-> SucessInfo:
        data = CreateUser("Joao")
        return SucessInfo.sucess_request(data)

    def test_GetUser(self)-> UserInfo:
        data = GetUser("Joao")
        return UserInfo.user_found(data)


     #GetUserLikedMusics
    def test_UserLikesMusic(self)-> ListMusicInfo:
        data = UserLikesMusic("Joao", "Faded")
        return ListMusicInfo.music_list_found(data) 

     # GetUserListenLaterMusics
    def test_UserListenLaterMusic(self)-> ListMusicInfo:
        data = UserListenLaterMusic("Joao", "Faded")
        return ListMusicInfo.music_list_found(data) 

    #GetUserLikedMusics
    def test_GetUserLikedMusics(self)-> ListMusicInfo:
        data = GetUserLikedMusics("Joao")
        return ListMusicInfo.music_list_found(data) 

     # GetUserListenLaterMusics
    def test_GetUserListenLaterMusics(self)-> ListMusicInfo:
        data = GetUserListenLaterMusics("Joao")
        return ListMusicInfo.music_list_found(data) 


if __name__ == '__main__':
    unittest.main()


