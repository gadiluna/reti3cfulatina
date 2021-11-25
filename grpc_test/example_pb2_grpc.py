# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import example_pb2 as example__pb2


class SumStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Sum = channel.unary_unary(
                '/Sum/Sum',
                request_serializer=example__pb2.sum_req.SerializeToString,
                response_deserializer=example__pb2.sum_rep.FromString,
                )
        self.StreamSum = channel.stream_stream(
                '/Sum/StreamSum',
                request_serializer=example__pb2.sum_req.SerializeToString,
                response_deserializer=example__pb2.sum_rep.FromString,
                )


class SumServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Sum(self, request, context):
        """(Method definitions not shown)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StreamSum(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SumServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Sum': grpc.unary_unary_rpc_method_handler(
                    servicer.Sum,
                    request_deserializer=example__pb2.sum_req.FromString,
                    response_serializer=example__pb2.sum_rep.SerializeToString,
            ),
            'StreamSum': grpc.stream_stream_rpc_method_handler(
                    servicer.StreamSum,
                    request_deserializer=example__pb2.sum_req.FromString,
                    response_serializer=example__pb2.sum_rep.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Sum', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Sum(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Sum(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Sum/Sum',
            example__pb2.sum_req.SerializeToString,
            example__pb2.sum_rep.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StreamSum(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/Sum/StreamSum',
            example__pb2.sum_req.SerializeToString,
            example__pb2.sum_rep.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)