import zmq


context = zmq.Context()

sock = context.socket(zmq.SUB)

sock.setsockopt(zmq.SUBSCRIBE, bytes('bulb','UTF-8'))
sock.connect("tcp://127.0.0.1:5600")


while True:
    raw_message = sock.recv()
    print(raw_message)
