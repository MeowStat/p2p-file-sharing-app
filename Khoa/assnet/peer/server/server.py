import socket
from threading import Thread


def get_host_default_interface_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
       s.connect(('8.8.8.8',1))
       ip = s.getsockname()[0]
    except Exception:
       ip = '127.0.0.1'
    finally:
       s.close()
    return ip

def new_server_incoming(addr, conn):
    print(addr)

def start_server(host,port):
    print("Thread server listening on: {}:{}".format(host,port))

    serversocket = socket.socket()
    serversocket.bind((host,port))

    serversocket.listen(10)
    while True:
        conn, addr = serversocket.accept()
        nconn = Thread(target=new_server_incoming, args=(addr, conn))
        nconn.start()



