import string
import unittest
import os

from dataclasses import dataclass

import grpc

from artistTest import GetArtistMusic,GetArtistsWithLetter,GetTop20Artist,GetViral10Artist
from artist_pb2 import *
from artist_pb2_grpc import ArtistStub

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

@dataclass
class MusicList:
    music: list[MusicInfo]

    @classmethod
    def music_list_found(cls, data: dict) -> "MusicList":
        return cls(music=data)

@dataclass
class ArtistInfo:
    artist_id: str
    name: str

    @classmethod
    def artistfound(cls,data:dict)-> "ArtistInfo":
        return cls(
            artist_id=data.artist_id,
            name=data.name
        )
   

@dataclass
class ArtistList:
    artist:list[ArtistInfo]

    @classmethod
    def artist_list_found(cls, data: dict) -> "ArtistInfo":
        return cls(artist=data)

class TestStringMethods(unittest.TestCase):

    def test_GetArtistMusic(self)-> MusicList:
        data = GetArtistMusic("Adele")
        return MusicList.music_list_found(data)

    def test_GetTop20Artist(self)-> ArtistList:
        data = GetTop20Artist("2017-02-01")
        return ArtistList.artist_list_found(data)

    def test_GetViral10Artist(self)-> ArtistList:
        data = GetViral10Artist("2017-02-01")
        return ArtistList.artist_list_found(data)

    def test_GetArtistsWithLetter(self)-> ArtistList:
        data = GetArtistsWithLetter("Ad")
        return ArtistList.artist_list_found(data)

if __name__ == '__main__':
    unittest.main()