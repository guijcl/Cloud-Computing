# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import artist_pb2 as artist__pb2


class ArtistStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetArtistMusic = channel.unary_unary(
        '/Artist/GetArtistMusic',
        request_serializer=artist__pb2.GetArtistMusicRequest.SerializeToString,
        response_deserializer=artist__pb2.MusicListResponses.FromString,
        )
    self.GetArtistWithLetter = channel.unary_unary(
        '/Artist/GetArtistWithLetter',
        request_serializer=artist__pb2.GetArtistWithLetterRequest.SerializeToString,
        response_deserializer=artist__pb2.ArtistListResponse.FromString,
        )
    self.GetTop20Artist = channel.unary_unary(
        '/Artist/GetTop20Artist',
        request_serializer=artist__pb2.GetTop20ArtistRequest.SerializeToString,
        response_deserializer=artist__pb2.ArtistListResponse.FromString,
        )
    self.GetViral10Artist = channel.unary_unary(
        '/Artist/GetViral10Artist',
        request_serializer=artist__pb2.GetViral10ArtistRequest.SerializeToString,
        response_deserializer=artist__pb2.ArtistListResponse.FromString,
        )


class ArtistServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def GetArtistMusic(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetArtistWithLetter(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetTop20Artist(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetViral10Artist(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ArtistServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetArtistMusic': grpc.unary_unary_rpc_method_handler(
          servicer.GetArtistMusic,
          request_deserializer=artist__pb2.GetArtistMusicRequest.FromString,
          response_serializer=artist__pb2.MusicListResponses.SerializeToString,
      ),
      'GetArtistWithLetter': grpc.unary_unary_rpc_method_handler(
          servicer.GetArtistWithLetter,
          request_deserializer=artist__pb2.GetArtistWithLetterRequest.FromString,
          response_serializer=artist__pb2.ArtistListResponse.SerializeToString,
      ),
      'GetTop20Artist': grpc.unary_unary_rpc_method_handler(
          servicer.GetTop20Artist,
          request_deserializer=artist__pb2.GetTop20ArtistRequest.FromString,
          response_serializer=artist__pb2.ArtistListResponse.SerializeToString,
      ),
      'GetViral10Artist': grpc.unary_unary_rpc_method_handler(
          servicer.GetViral10Artist,
          request_deserializer=artist__pb2.GetViral10ArtistRequest.FromString,
          response_serializer=artist__pb2.ArtistListResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'Artist', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
