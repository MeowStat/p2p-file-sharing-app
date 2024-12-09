import json
import socket
import threading
import keyboard
from datetime import datetime
import sys
import os

peer_info = {}
event = threading.Event()


def handle_connection(conn):
    # print("have connect")
    # peers = peer_info.get("Lab.pdf", [])
    # print(peers)
    try:
        # data = conn.recv(1024).decode('utf-8')
        # print("-------------------------------------------------------------------")
        # print(f"Received data from peer: {data}")

        # if not data:
        #     return
        buffer = conn.recv(1024)
        if not buffer:
            print("No data received from peer.")
            return

        data = buffer.decode('utf-8')
        print("-------------------------------------------------------------------")
        print(f"Received data from peer: {data}")

        args = data.split(":")
        if len(args) < 2:
            print("Invalid command format")
            return
        peer_addr = args[1]
        
        
        if data.startswith("START:"):
            if len(args) < 3:
                print("Invalid START command format")
                return
            file_name = (args[2]).strip()
            file_name2 = str(file_name)
            # print("file name:",file_name)
            # print(file_name2 == "Lab.pdf")
            add_peer(peer_addr, file_name2)
            peers = peer_info.get(file_name2, [])
        elif data.startswith("LIST:"):
            if len(args) < 2:
                print("Invalid LIST command format")
                return
            file_name = str(args[1]).strip()
            print("Name of in: ", file_name)
            peers = peer_info.get(file_name, [])
            # print("peer info :", peer_info[file_name])
            response = f"LIST:{file_name}:{peers}!\n"
            conn.sendall(response.encode('utf-8'))
            print(f"Sent response to peer: {response}")
            response = json.dumps(peer_info)
            conn.sendall((response + "!").encode('utf-8'))  # Thêm '!' làm dấu kết thúc thông điệp
        
    except Exception as e:
        print(f"Error handling connection: {e}")
    finally:
        conn.close()

def add_peer(peer_addr, file_name):
    global peer_info
    if file_name not in peer_info:
        peer_info[(file_name)] = [  ]
        print("new peer info")
    if peer_addr not in peer_info[file_name]:
        peer_info[(file_name)].append(peer_addr)
        print(f"Peer '{peer_addr}' added to file '{file_name}'")
        peers = peer_info.get((file_name), [])
        print(peers)
    

def stop():
    event.set()
    print("Stop")
    os._exit()

keyboard.add_hotkey("q", stop )

if  __name__ == "__main__":
    # tracker_address = input("Enter URL: ")
    tracker_address = "192.168.1.7"
    tracker_address = f"{tracker_address}:8080"

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((tracker_address.split(':')[0], int(tracker_address.split(':')[1])))
        server.listen(5)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Tracker is running at address: {tracker_address}")

        while not event.is_set():
            conn, addr = server.accept()
            threading.Thread(target=handle_connection, args=(conn,)).start()
    except Exception as e:
        print(f"Failed to initialize tracker: {e}")
    finally:
        server.close()