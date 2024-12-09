from threading import Thread
import socket
import sys
import threading
import keyboard



stop_event = threading.Event()

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

def stop():
    stop_event.set()  # Đặt sự kiện dừng
    print("Stopping the server...")

keyboard.add_hotkey("q", stop )

def start_server(address):
    print("Thread server listening on: ", address)
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(serversocket)
    print("cc")
    try: 
        print(address.split(':')[0].strip())
        print(address.split(':')[1].strip())
        serversocket.bind((address.split(':')[0].strip(),int(address.split(':')[1].strip())))
        print("aaa")
        serversocket.listen(10)

        while not stop_event.is_set():  # Kiểm tra stop_event
            serversocket.settimeout(1)  # Timeout ngắn để không bị chặn lâu trong accept
            try:
                conn, addr = serversocket.accept()
                print(f"Connection from {addr}")
                conn.close()  # Đóng kết nối sau khi xử lý
            except socket.timeout:
                continue
    except Exception as e:
        print(f"Error in server: {e}")
    finally:
        serversocket.close()
        print("Server has been stopped.")
    # print("Thread server listening on: {}:{}".format(host,port))

    # serversocket = socket.socket()
    # serversocket.bind((host,port))

    # serversocket.listen(10)
    # while True:
    #     conn, addr = serversocket.accept()
    #     print(f"Connection from {addr}")
    #     nconn = Thread(target=handle_connection, args=(conn))
    #     nconn.start()