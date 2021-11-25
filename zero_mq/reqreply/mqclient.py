import zmq


context=zmq.Context()

sock = context.socket(zmq.REQ)
sock.connect("tcp://127.0.0.1:8080")

while True:
    msg=sock.send(b"Ping")
    print(sock.recv())