import os
import threading
import torrent 
from client import client
import constant
import bencodepy
from server import server
from threading import Thread

    
if __name__ == "__main__":
   
    peer_ip = server.get_host_default_interface_ip()
    server_port = 8080

    peer_server = Thread(target=server.start_server, args=(peer_ip,server_port))
    peer_server.start()

    peer_id = server.generate_peer_id_with_ip("-MStat-",peer_ip)

    while True:
        command_line = input("\n> ").strip()

        if command_line.startswith("menu"):
            print("Torrent App")
            print("Commands Available:")
            print("     create [tracker-url] [files]")
            print("     seed [torrent-file]")
            print("     getlistofpeers [your torrent-file]")
            print("     getTracker")
            print("     download [your-torrent-file] [file]")
            print("     share")
            print("     exit")

        elif command_line.startswith("getTracker"):
            
            tracker_address = '192.168.56.1:8080'
            # tracker = client.AnnounceToTracker( peer_address, filename)
            print("No trackers connected.")
        
        elif command_line.startswith("share"):
            print("started sharing...")

        elif command_line.startswith("seed"):
            torrent_file = command_line.split(" ")[1]
            client.Seed(peer_id,peer_ip,torrent_file)

        elif command_line.startswith("create"):
            tracker_url = constant.TRACKER_URL
            filepath = ['test.txt']
            torrent.create_torrent(filepath,tracker_url)
            print("started create...")