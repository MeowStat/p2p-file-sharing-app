import os
import threading
import client 
def start_server(peer_adress):
    server_address = f"{peer_address}:8080"

if __name__ == "__main__":
    peer_address = input("Enter your peer address: ").strip()

    server_thread = threading.Thread(target=start_server, args = (peer_address,))
    server_thread.daemon = True
    server_thread.start()

    while True:
        command_line = input("\n> ").strip()

        if command_line.startswith("menu"):
            print("Torrent App")
            print("Commands Available:")
            print("     create [tracker-url] [files]")
            print("     getlistofpeers [your torrent-file]")
            print("     getTracker")
            print("     download [your-torrent-file] [file]")
            print("     share")
            print("     exit")

        elif command_line.startswith("getTracker"):
            filename = "test.txt"
            tracker_address = '192.168.56.1:8080'
            tracker = client.connect_to_tracker(tracker_address, peer_address, filename)
            print("No trackers connected.")
        
        elif command_line.startswith("share"):
            print("started sharing...")

        elif command_line.startswith("create"):
            print("started create...")