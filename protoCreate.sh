
#rm ./app/protobufs/*/*pb2*
### Musics
python3 -m grpc_tools.protoc -I ./app/protobufs --python_out=./app/protobufs/musics/ --grpc_python_out=./app/protobufs/musics/ ./app/protobufs/music.proto --experimental_allow_proto3_optional


### Artists
python3 -m grpc_tools.protoc -I ./app/protobufs --python_out=./app/protobufs/artist/ --grpc_python_out=./app/protobufs/artist/ ./app/protobufs/artist.proto --experimental_allow_proto3_optional


### Accounts
python3 -m grpc_tools.protoc -I ./app/protobufs --python_out=./app/protobufs/account/ --grpc_python_out=./app/protobufs/account/ ./app/protobufs/account.proto --experimental_allow_proto3_optional








