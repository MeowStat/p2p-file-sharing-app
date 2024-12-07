import json
import socket
import threading
from datetime import datetime

def handle_connection(conn):
    try:
        data = conn.recv(1024).decode('utf-8')
        print("-------------------------------------------------------------------")
        print(f"Received data from peer: {data}")

        if not data:
            return
    except Exception as e:
        print(f"Error handling connection: {e}")
    finally:
        conn.close()

if  __name__ == "__main__":
    tracker_address = input("Enter URL: ")
    tracker_address = f"{tracker_address}:8080"

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((tracker_address.split(':')[0], int(tracker_address.split(':')[1])))
        server.listen(5)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Tracker is running at address: {tracker_address}")

        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_connection, args=(conn,)).start()
    except Exception as e:
        print(f"Failed to initialize tracker: {e}")
    finally:
        server.close()