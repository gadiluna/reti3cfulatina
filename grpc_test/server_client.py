import example_pb2_grpc
import example_pb2
import grpc

channel = grpc.insecure_channel('localhost:50051')
stub = example_pb2_grpc.SumStub(channel)
m=example_pb2.sum_req()
m.x=10
m.y=11
z=stub.Sum(m)
print(z)
a=[m,m,m,m,m]
for x in stub.StreamSum(iter(a)):
    print(x)
channel.close()