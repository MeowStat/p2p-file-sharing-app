import os
import threading
import torrent 
from client import client
import constant
import bencodepy

def start_server(peer_adress):
    server_address = f"{peer_address}:8080"
import bencodepy










    
if __name__ == "__main__":
   

    filename = '4b6fcb2d521ef0fd442a5301e7932d16cc9f375a.torrent'
    # Sử dụng hàm để đọc tệp torrent
    

    # # tracker_url = constant.TRACKER_URL
    # # torrent.create_torrent(filename,tracker_url)


    peer_address = input("Enter your peer address: ").strip()

    # server_thread = threading.Thread(target=start_server, args = (peer_address,))
    # server_thread.daemon = True
    # server_thread.start()

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
            
            tracker_address = '192.168.56.1:8080'
            tracker = client.AnnounceToTracker( peer_address, filename)
            print("No trackers connected.")
        
        elif command_line.startswith("share"):
            print("started sharing...")

        elif command_line.startswith("create"):
            tracker_url = constant.TRACKER_URL
            filepath = ['test.txt']
            torrent.create_torrent(filepath,tracker_url)
            print("started create...")