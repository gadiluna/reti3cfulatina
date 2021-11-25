import socket
import json
import sys


def sendmsg(socket, msg):
    stringa=json.dumps(msg)
    socket.sendall(bytes(stringa,"UTF-8"))
    resp=socket.recv(1024)
    rsp_diz=json.loads(str(resp,'UTF-8'))
    if rsp_diz['rsp'] == "ok":
        if 'name' in rsp_diz:
            print("Name: {}, Number:{}".format(rsp_diz['name'],rsp_diz['number']))
        print('executed')
    else:
        print("error"+ str(rsp_diz['msg']))

if __name__ == "__main__":
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sa = input("server address:")
    si = int(input("server port:"))
    x = sk.connect((sa, si))
    print("Connected with {}:{}".format(sa, si))
    while True:
        command = input("Command like add name number; del name; search name; search number; quit:")
        tokenized_command = command.split(" ")
        cmd = tokenized_command[0]
        if cmd == "add":
            if len(tokenized_command) == 3 and tokenized_command[2].isnumeric():
                message = {'type': 'store', 'name': tokenized_command[1], 'number': tokenized_command[2]}
                sendmsg(sk,message)
            else:
                print("syntax of add - add name number")
        elif cmd == "del":
            if len(tokenized_command) == 2:
                message = {'type': 'delete', 'name': tokenized_command[1]}
                sendmsg(sk,message)
            else:
                print("syntax of del -  del name")
        elif cmd == "search":
            if len(tokenized_command) == 2:
                if tokenized_command[1].isnumeric():
                    message = {'type': 'search', 'number': tokenized_command[1]}
                    sendmsg(sk,message)
                else:
                    message = {'type': 'search', 'name': tokenized_command[1]}
                    sendmsg(sk,message)
            else:
                print("syntax of search -  search name/number")
        elif cmd == 'quit':
            sys.exit(0)
        else:
            print("command non recognized")

    x.close()
