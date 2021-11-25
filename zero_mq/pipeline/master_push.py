import json
import threading
import time
import multithread
import zmq
import random
from uuid import uuid4



def generate_work():
    id=str(uuid4())
    msg={}
    msg['id']=id
    lista=random.sample(range(0,1000000),1000)
    msg['work']=lista
    return json.dumps(msg)

def collect_work(sock):
    while True:
        job_done=json.loads(str(sock.recv(),'UTF-8'))
        print("Done Job received")




context = zmq.Context()
sock_push = context.socket(zmq.PUSH)
sock_push.bind("tcp://127.0.0.1:5600")
sock_return=context.socket(zmq.SUB)
sock_return.setsockopt(zmq.SUBSCRIBE, bytes('','UTF-8'))
sock_return.bind('tcp://127.0.0.1:5700')
tr=threading.Thread(target=collect_work,args=(sock_return,))
tr.start()
with sock_push:
    while True:
        msg=generate_work()
        sock_push.send(bytes(msg, 'UTF-8'))
        time.sleep(1)


