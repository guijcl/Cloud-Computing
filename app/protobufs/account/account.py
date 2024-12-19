import grpc
from concurrent import futures

from pymongo import MongoClient

from account_pb2 import *
import account_pb2_grpc

from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound
from flask import Flask
app = Flask(__name__)

from prometheus_client import start_http_server, Summary


# global variables for MongoDB host (default port is 27017)
DOMAIN = '35.232.250.130'
PORT = 27017

print("Connecting to database.....")

    # try to instantiate a client instance
client = MongoClient(
        host = [ str(DOMAIN) + ":" + str(PORT) ],
        serverSelectionTimeoutMS = 3000, # 3 second timeout
        username = "root",
        password = "root",
    )


db1 = client["database"]
db1 = db1["account"]


db2 = client["database"]
# drop everything in there
db2 = db2["music"]

def health():
    return HTTPResponse(status=200)

class AccountService(account_pb2_grpc.AccountServicer):
    #return UserResponse(username=request.username, 
    # listenLater=
    #     AccountMusicListResponse(music=[
    #         AccountMusicResponse(
    #                 music_id="1", type=ChartType.TOP200, name="JOAQUIM"
    #         )
    #     ]), 
    # likes=
    #     AccountMusicListResponse(music=[
    #         AccountMusicResponse(
    #                 music_id="1", type=ChartType.TOP200, name="JOAQUIM"
    #         )
    #     ]))
    

    def GetUserByName(self, request, context):
        res = db1.find_one({ "username": (request.username)})
        return UserResponse(username=res["username"], 
            listenLater= AccountMusicListResponse(music= StrToMusicResponse(res["listenLater"])), 
            likes= AccountMusicListResponse(music=StrToMusicResponse(res["likes"])))

    def CreateUser(self, request, context):
        res = db1.find_one({ "username": (request.username)})
        if(res is not None):
            return Success(success=False)
        db1.insert_one({"username":request.username, "listenLater":[], "likes":[]})
        return Success(success=True)

    def DeleteUser(self, request, context):
        res = db1.find_one({ "username": request.username})
        if(res is None):
            return Success(success=False)
        db1.delete_one({ "username": res["username"]})
        return Success(success=True)

    def LoginUser(self, request, context):
        pass

    def LogoutUser(self, request, context):
        pass

    def ListenLater(self, request, context):
        res = db1.find_one({ "username": request.username})
        if(res is None):
            return Success(success=False)

        res2= db2.find_one({ "title": request.musicname})

        if(res2 is None):
            return Success(success=False)

        listenLater = db1.find_one({ "username": res["username"], 'listenLater': request.musicname})
        
        if listenLater is not None:
            return Success(success= False)
        
        db1.update_one({ "username": res["username"]}, {'$push': {'listenLater': request.musicname}})
        return Success(success=True)
        

    def GetListenLaterMusics(self, request, context):

        user = db1.find_one({ "username": request.username})
        listenLater=user.get("listenLater")

        if listenLater is None:
            raise NotFound("User not found") 

        ret= [] 
         
        for music in listenLater:
            ret.append(AccountMusicResponse(name= music))

        return AccountMusicListResponse (music = ret)

    def Like(self, request, context):

        res = db1.find_one({ "username": request.username})
        if(res is None):
            return Success(success=False)

        res2= db2.find_one({ "title": request.musicname})

        if(res2 is None):
            return Success(success=False)

        #impedir de dar add a uma musica que ja esteja nos Likes

        likes = db1.find_one({ "username": request.username, 'likes': request.musicname})
        
        if likes is not None:
            return Success(success= False)
            
        db1.update_one({ "username": request.username}, {'$push': {'likes':request.musicname}})
        
        return Success(success=True)
        

    def GetLikes(self, request, context):

        user = db1.find_one({ "username": request.username})

        likes=user.get("likes")


        if likes is None:
            raise NotFound("User not found")

        ret= [] 

        for music in likes:
            ret.append(AccountMusicResponse(name= music))

        return AccountMusicListResponse (music = ret)

def StrToMusicResponse(list):
    res = []
    for item in list:
        res.append(AccountMusicResponse(name= item))
    return res

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

@REQUEST_TIME.time()   
def serve():
        interceptors = [ExceptionToStatusInterceptor()]
        server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
        )
        account_pb2_grpc.add_AccountServicer_to_server(
            AccountService(), server
        )

        server.add_insecure_port("[::]:50052")
        server.start()
        server.wait_for_termination()

if __name__ == "__main__":
    #app.run(ssl_context='adhoc')
    start_http_server(51052)
    serve()
