import zmq
import random
import time
from uuid import uuid4
from datetime import datetime


context = zmq.Context()
sock = context.socket(zmq.PUSH)
sock.bind("tcp://127.0.0.1:5600")
