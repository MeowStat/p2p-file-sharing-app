from threading import Thread
import socket

def handle_connection(conn):
    with conn:
        while True:
            message = conn.recv(1024).decode("utf-8").strip()
            if not message:
                break  # Connection closed
            print(f"Received message: {message}")

            # if message.startswith("HANDSHAKE:"):
            #     info_hash, worker = handle_handshake(conn, message)
            #     if worker is None:
            #         continue
            #     connection_workers[info_hash] = worker

            # elif message.startswith("Requesting"):
            #     handle_piece_request(conn, message)

            # else:
            #     print(f"Unknown message: {message}")
            #     conn.sendall(b"ERROR: Unknown message\n")

def start_server(address):
    print("Thread server listening on: ", address)
    serversocket = socket.socket()
    serversocket.bind((address.split(':')[0], int(address.split(':')[1])))
    serversocket.listen(10)

    while True:
        conn, addr = serversocket.accept()
        print(f"Connection from {addr}")
    # print("Thread server listening on: {}:{}".format(host,port))

    # serversocket = socket.socket()
    # serversocket.bind((host,port))

    # serversocket.listen(10)
    # while True:
    #     conn, addr = serversocket.accept()
    #     print(f"Connection from {addr}")
    #     nconn = Thread(target=handle_connection, args=(conn))
    #     nconn.start()