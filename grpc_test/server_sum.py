import example_pb2_grpc
import example_pb2
import grpc
import concurrent.futures as futures

class ServerSum(example_pb2_grpc.SumServicer):

    def Sum(self, request, context):
        x=request.x
        y=request.y
        resp=example_pb2.sum_rep()
        resp.z=x+y
        return resp

    def StreamSum(self, request_iterator, context):
        accumulator=0
        for r in request_iterator:
            accumulator=r.x+r.y+accumulator
            print(r)
            yield example_pb2.sum_rep(z=accumulator)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    example_pb2_grpc.add_SumServicer_to_server(
        ServerSum(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

serve()