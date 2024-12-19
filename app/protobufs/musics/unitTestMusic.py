import unittest

from dataclasses import dataclass

import grpc

from musicsTest import GetMusic, GetTrending, GetTrendingMusicsCountry, GetTop200, GetTop200Country, GetViral50, GetViral50Country
from music_pb2 import *

@dataclass
class MusicInfo:
    music_id: str
    name: str
    streams: int
    type: str

    @classmethod
    def music_found(cls, data: dict) -> "MusicInfo":
        return cls(
            music_id=data.music_id,
            name=data.name,
            streams=data.streams,
            type=data.type
        )
    
    @classmethod
    def music_notFound(cls, data: dict) -> "MusicInfo":
        return cls(
            grpc.RpcError
        )

@dataclass
class MusicList:
    music: list[MusicInfo]

    @classmethod
    def music_list_found(cls, data: dict) -> "MusicList":
        return cls(music=data)


class TestStringMethods(unittest.TestCase):

    def test_GetMusicExistent(self)-> MusicInfo:
        data = GetMusic("Faded")
        return MusicInfo.music_found(data)

    def test_GetTrendingMusics(self)-> MusicList:
        data = GetTrending("2017-02-01","MOVE_UP")
        return MusicList.music_list_found(data)

    def test_GetTrendingMusicsCountry(self)-> MusicList:
        data = GetTrendingMusicsCountry("2017-02-01","MOVE_UP","Chile")
        return MusicList.music_list_found(data)

    def test_GetTop200Musics(self)-> MusicList:
        data = GetTop200("2017-02-01")
        return MusicList.music_list_found(data)

    def test_GetTop200MusicsCountry(self)-> MusicList:
        data = GetTop200Country("Chile")
        return MusicList.music_list_found(data)

    def test_GetViral50(self)-> MusicList:
        data = GetViral50("2017-02-01")
        return MusicList.music_list_found(data)

    def test_GetViral50Country(self)-> MusicList:
        data = GetViral50Country("2017-02-01","Chile")
        return MusicList.music_list_found(data)

#    def test_GetMusicNonExistent(self)-> MusicInfo:
#        data = GetMusic("Faded")
#        return MusicInfo.music_found(data)


       
if __name__ == '__main__':
    unittest.main()