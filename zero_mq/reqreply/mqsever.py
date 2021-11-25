import zmq
import datetime


context=zmq.Context()

sock = context.socket(zmq.REP)
sock.bind("tcp://*:8080")

while True:
    msg=sock.recv()
    tempo=str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    sock.send(bytes(tempo,'UTF-8'))
