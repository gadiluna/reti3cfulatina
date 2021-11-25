import socket
import threading
import json
import signal
import sys
import time

class Handler:

    def __init__(self, phonebook, lock,event):
        self.phonebook = phonebook
        self.phone_lock = lock
        self.quit_event=event

    def add_entry(self, name, number):
        with self.phone_lock:
            self.phonebook[name] = number
            return {'rsp':'ok'}

    def delete_entry(self, name):
        with self.phone_lock:
            del self.phonebook[name]
            return {'rsp':'ok'}



    def get_entry_by_name(self, name):
        with self.phone_lock:
            if name in self.phonebook:
                return {'rsp':'ok', 'name':name, 'number': self.phonebook[name]}
        return {'rsp':'ok'}

    def get_entry_by_number(self, number):
        with self.phone_lock:
            for x, y in self.phonebook.items():
                if y == number:
                    return {'rsp':'ok', 'name':x, 'number': y}
            return {'rsp':'ok'}

    def handle_msg(self, request):
        try:
            if request['type'] == "store" and 'name' in request and 'number' in request:
                return self.add_entry(request['name'], request['number'])
            elif request['type'] == "delete" and 'name' in request:
                return self.delete_entry(request['name'])
            elif request['type'] == "search" and 'name' in request:
                return self.get_entry_by_name(request['name'])
            elif request['type'] == "search" and 'number' in request:
                return self.get_entry_by_number(request['number'])
        except:
            return {'rsp': 'error','msg':'unkown_cmd'}

    def handle(self, connection):
        connection.settimeout(0.01) #wait 10 ms second
        try:
            while True:
                try:
                    data = connection.recv(2048)
                    msg = json.loads(str(data, 'UTF-8'))
                    rsp = self.handle_msg(msg)
                    if rsp is not None:
                        connection.send(bytes(json.dumps(rsp), "UTF-8"))
                    if rsp is None:
                        break
                    if self.quit_event.is_set():
                        break
                except socket.timeout:
                    if self.quit_event.is_set():
                        break
            connection.close()
        except Exception as e:
            print(str(e))
            connection.close()


class Server:

    def __init__(self, host, port, persistence_file=None,max_con=10):
        self.max_con=max_con
        self.host = host
        self.port = port
        self.quit_event=threading.Event()
        self.persistence_file = persistence_file
        self.phonebook = self.load_persistence()
        if self.phonebook is None:
            self.phonebook = dict()
        self.lock = threading.Lock()
        self.threads=[]

    def load_persistence(self):
        if self.persistence_file is None:
            return None
        try:
            with open(self.persistence_file) as f:
                return json.load(f)
        except:
            return None

    def save_persistence(self):
        if self.persistence_file is None:
            return
        with self.lock:
            with open(self.persistence_file, 'w+') as f:
                json.dump(self.phonebook, f)

    def shutdown(self,signum,frame):
        self.stop_threads()
        self.save_persistence()
        self.socket.close()
        sys.exit(0)

    def stop_threads(self):
        self.quit_event.set()
        for i in range(0,2):
            self.threads=[t for t in self.threads if t.is_alive()]
            if len(self.threads)==0:
                break
            time.sleep(0.1) #sleep 50ms
        return

    def house_keeping(self):
        self.threads = [t for t in self.threads if t.is_alive()]

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket=s
        s.bind((self.host, self.port))
        s.listen()
        while True:
            connected_socket, address = s.accept()
            print("Received connection from {}", str(address))
            if len(self.threads) < self.max_con:
                h = Handler(self.phonebook, self.lock,self.quit_event)
                t = threading.Thread(target=h.handle, args=(connected_socket,))
                t.start()
                self.threads.append(t)
            else:
                connected_socket.send(bytes(json.dumps({'rsp': 'error','msg':'too_many_connection'}), "UTF-8"))
            self.house_keeping()

if __name__ == "__main__":
    s = Server('127.0.0.1', 8090,'persistence.json')
    signal.signal(signal.SIGINT,s.shutdown)
    s.run()
