import time
import threading
import random

class RWLock():

    def __init__(self):
        self.lock_m=threading.Lock()
        self.lock_b=threading.Lock()
        self.b=0
        self.writer_waiting=0

    def lockread(self):
        while self.writer_waiting==1:
            nop=0
        self.lock_b.acquire()
        self.b=self.b+1
        print("Number readers"+str(self.b))
        if self.b==1:
            self.lock_m.acquire()
        self.lock_b.release()

    def unlockread(self):
        self.lock_b.acquire()
        self.b=self.b-1
        if self.b==0:
            self.lock_m.release()
        self.lock_b.release()

    def lockwrite(self):
        self.writer_waiting=1
        self.lock_m.acquire()

    def unlockwrite(self):
        self.lock_m.release()
        self.writer_waiting=0


class Writer():

    def __init__(self,rwlock,lista):
        self.rwlock=rwlock
        self.lista=lista


    def run(self):
        while True:
            self.rwlock.lockwrite()
            print("Write writing")
            self.lista.append(random.randint(0,10))
            if len(self.lista)>100:
                #self.lista=lista[60:100]
                for i in range(0,40):
                    del self.lista[1]
            self.rwlock.unlockwrite()
            time.sleep(0.001)

class Reader():

    def __init__(self,rwlock,lista):
        self.rwlock=rwlock
        self.lista=lista

    def run(self):
        while True:
            self.rwlock.lockread()
            print(self.lista)
            self.rwlock.unlockread()

if __name__ == "__main__":
    rwlock=RWLock()
    lista=[]
    w=Writer(rwlock,lista)
    rt=threading.Thread(target=w.run)
    rt.start()
    readers=[]
    for x in range(0,20):
        r=Reader(rwlock,lista)
        readers.append(threading.Thread(target=r.run))
        readers[-1].start()
    while True:
        time.sleep(10)
