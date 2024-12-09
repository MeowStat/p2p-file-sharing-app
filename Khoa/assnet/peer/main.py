import os
import threading
import torrent 
from client import client
import constant
import bencodepy
from server.server import start_server
import bencodepy










    
if __name__ == "__main__":
   

    filename = '4b6fcb2d521ef0fd442a5301e7932d16cc9f375a.torrent'
    # Sử dụng hàm để đọc tệp torrent
    

    # # tracker_url = constant.TRACKER_URL
    # # torrent.create_torrent(filename,tracker_url)


    peer_address = input("Enter your peer address: ").strip()   
    
    server_address = f"{peer_address}:8080"
    threading.Thread(target=start_server, args=(server_address,)).start()

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

        elif command_line.startswith("getlistpeers"):
            args = command_line.split(" ")
            if len(args) != 2:
                print("Usage: getlistofpeers [one torrent-file]")
                continue
            
            torrent_filename = args[1]
            try:
                torrent_info = torrent.parse_torrent_file(torrent_filename)
            except Exception as e:
                print(f"Error opening torrent file: {e}")
                continue

            tracker_url = torrent_info['announce']
            filename = torrent_info['name']
            try:    
                client.get_list_of_peer(tracker_url, filename)
            except Exception as e:
                print(f"Failed to get list of peers: {e}")
                continue

        elif command_line.startswith("getTracker"):
            
            tracker_address = '10.0.11.78:8080'
            # tracker = client.AnnounceToTracker( peer_address, filename)
            tracker = client.connect_to_tracker(tracker_address, peer_address, filename)
            # print("No trackers connected.")
        elif command_line.startswith("Download"):
            args = command_line.split(" ")
            if len(args) != 2:
                print("Usage: announcetotracker [only one torrent-file]")
                continue
            torrent_file = args[1]
            peer_list = ['127.213.12', '182.112.871.1']
            client.start_download(torrent_file, peer_list, peer_address)

        elif command_line.startswith("Seeding"):
            args = command_line.split(" ")

            if len(args) != 2:
                print("Usage: announcetotracker [only one torrent-file]")
                continue
            
            torrent_filename = args[1]
            try:
                tracker = client.AnnounceToTracker(peer_address, torrent_filename)
            except Exception as e:
                print(f"Failed to announce to tracker: {e}")


        elif command_line.startswith("create"):
            args = command_line.split(" ")

            if len(args) <= 2:
                print("Usage: create [tracker-address] [files]")
                continue

            tracker_url = args[1]
            tracker_url = tracker_url + ":4040"
            source_files = args[2:]
            source_files = [file.strip() for file in source_files] 
            print(source_files)
            # source_files2 = ['Lab.pdf']
            try:
                torrent_file_name = torrent.create_torrent(source_files ,tracker_url)
                print(f"Torrent file created successfully: {torrent_file_name}")
            except Exception as e:
                print(f"Failed to create torrent file: {e}")
            