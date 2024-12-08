import socket
from threading import Thread
import hashlib


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

def generate_peer_id_with_ip(client_prefix, ip_address):
    peer_id_hash = hashlib.sha1(ip_address.encode()).hexdigest()[:12]  # Get first 12 characters of the hash
    return client_prefix + peer_id_hash

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



