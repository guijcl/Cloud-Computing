import os
import unittest

import grpc

from music_pb2 import *
from music_pb2_grpc import MusicsStub

musics_host = os.getenv("MUSICS_HOST", "localhost") 
musics_channel = grpc.insecure_channel(f"{musics_host}:50051") 
musics_client = MusicsStub(musics_channel)


class musicTestCases(unittest.TestCase):

# Test 1
# Test the GetMusic method
    def test_GetMusic(self):

        print("Request - Find music by name: Faded")

        musics_request = GetMusicRequest(name="Faded")
        
        self.assertTrue(musics_client.GetMusic(musics_request).music_id, "62b3920b988e6a0fad1951df")

        self.assertTrue(musics_client.GetMusic(musics_request).name, "Faded")

        self.assertTrue(musics_client.GetMusic(musics_request).streams, 18903)



# Test 2
# Test the GetTrendingMusics method
    def test_GetTrending(self):

        print("Request - Find list of songs by trend and date")

        musics_request = GetTrendingMusicsRequest(date="2017-01-02", trend="MOVE_UP")

        self.assertTrue(len(musics_client.GetTrendingMusics(musics_request)),635)


# Test 3
# Test the GetTrendingMusicsByCountry method
    def test_GetTrendingMusicsCountry(self):

        print("Request - Find the list of songs by date, trend and country")

        musics_request = GetTrendingMusicsByCountryRequest(date="2017-01-02", trend="MOVE_UP", country="Chile")

        self.assertTrue(len(musics_client.GetTrendingMusicsByCountry(musics_request)),66)


# Test 4 
# Test the GetTop200Musics method
    def test_GetTop200(self):
        print("Request - Find the list of songs that are in the top200, by date")

        musics_request = GetTop200MusicsRequest(date="2017-01-02")

        self.assertTrue(len(musics_client.GetTop200Musics(musics_request)),1360)




# Test 5 
# Test the GetTop200MusicsByCountry method
    def test_GetTop200Country(self):
        print("Request - Find the list of songs that are in the top200, by country")

        musics_request = GetTop200MusicsByCountryRequest(date="2017-01-02",country="Chile")

        self.assertTrue(len(musics_client.GetTop200MusicsByCountry(musics_request)), 93)

if __name__ == '__main__':
    unittest.main()

    
