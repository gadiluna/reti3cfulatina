import json
import zmq


def execute_work(msg):
    l=msg['work']
    return sorted(l)


context = zmq.Context()
sock = context.socket(zmq.PULL)
sock.connect("tcp://127.0.0.1:5600")
sock_return = context.socket(zmq.PUB)
sock_return.connect("tcp://127.0.0.1:5700")
with sock:
    while True:
        msg=json.loads(str(sock.recv(),'UTF-8'))
        l=execute_work(msg)
        print(str(l[0:10])[:-1]+'...')
        sock_return.send(bytes(json.dumps(l),'UTF-8'))