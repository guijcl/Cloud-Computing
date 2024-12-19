#!/usr/bin/env python

# Copyright 2022 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import uuid

from datetime import datetime
from locust import FastHttpUser, TaskSet, task


# [START locust_test_task]

class MetricsTaskSet(TaskSet):
    _deviceid = None

    def on_start(self):
        self._deviceid = str(uuid.uuid4())
    
    @task
    def getMusic(self):
        self.client.get(
            "/api/music/Faded")

    '''
    @task
    def getArtist(self):
        self.client.get(
            "/api/getArtistMusic/Adele")

    @task
    def getTop20ArtistByDate(self):
        self.client.get(
            "/api/getTop20Artist/2017-01-02")

    
    @task
    def getPage(self):
        self.client.get(
        "/api/swagger.json")
    
    @task
    def getTrendingMusicByDate(self):
        self.client.get(
            "/api/getTrendingMusic/2017-01-01/MOVE_UP")
    
    @task
    def createUser(self):
        self.client.post(
            "/api/user/createUser/userTest")

    @task
    def getUserInfo(self):
        self.client.get(
            "/api/user/GetUserInfo/userTest")
    
    @task
    def markLike(self):
        self.client.put(
            "/api/user/music/userTest/Faded/like")
    '''

    '''@task(1)
    def login(self):
        self.client.post(
            '/login', {"deviceid": self._deviceid})'''

    '''@task(999)
    def post_metrics(self):
        self.client.post(
            "/metrics", {"deviceid": self._deviceid, "timestamp": datetime.now()})'''


class MetricsLocust(FastHttpUser):
    tasks = {MetricsTaskSet}

# [END locust_test_task]
