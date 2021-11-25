import zmq
import random
import time
from uuid import uuid4
from datetime import datetime

targets=['bulb','camera','fridge']
context = zmq.Context()
sock = context.socket(zmq.PUB)
sock.bind("tcp://127.0.0.1:5600")

def generate_a_random_target():
    return random.sample(targets,1)[0]

def send_message(id, timestamp,publisher):
    # Message [prefix][message]
    target=generate_a_random_target()
    message = "{topic} message id:{id} from: {publisher} generated at: {timestamp}".\
        format(topic=target, id=id, timestamp=timestamp,publisher=publisher)
    sock.send(bytes(message,'UTF-8'))

while True:
    id_messaggio, data = str(uuid4()), datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    send_message(id_messaggio, data, publisher='P1')
    time.sleep(1)
