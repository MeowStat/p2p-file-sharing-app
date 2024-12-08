import socket
import struct
import threading
import hashlib
import json
import time
import bencodepy
import torrent
import requests

connected_tracker_addresses = []

class AddrAndFilename:
    def __init__(self, addr, filename):
        self.addr = addr
        self.filename = filename

class PieceWork:
    def __init__(self, index, hash, size):
        self.index = index
        self.hash = hash
        self.size = size

class PieceResult:
    def __init__(self, index, data, error):
        self.index = index
        self.data = data
        self.error = error

# def start_download(torrent_file, another_peer_addresses, peer_address):
#     print(f"Starting download for: {torrent_file}")

#     tfs = torrent.open_torrent(f"torrent_files/{torrent_file}")
#     if not tfs:
#         print("Error opening torrent file.")
#         return

#     active_peers = []
#     for peer in another_peer_addresses:
#         print(f"Testing connection to peer: {peer}")
#         if test_connection(peer):
#             print(f"Peer {peer} is available")
#             if perform_handshake(peer, tfs[0]["InfoHash"]):
#                 active_peers.append(peer)
#         else:
#             print(f"Peer {peer} is not available.")

#     if not active_peers:
#         print("No available active peers found!")
#         return

#     for tf in tfs:
#         print(f"Downloading file: {tf['Name']}")
#         num_workers = 3
#         work_queue = [PieceWork(i, h, tf["PieceLength"]) for i, h in enumerate(tf["PieceHashes"])]
#         results = []

#         threads = []
#         for i in range(num_workers):
#             peer = active_peers[i % len(active_peers)]
#             thread = threading.Thread(target=download_worker, args=(peer, work_queue, results, tf["InfoHash"]))
#             thread.start()
#             threads.append(thread)

#         for thread in threads:
#             thread.join()

#         pieces_by_index = {result.index: result.data for result in results if not result.error}
#         for result in results:
#             if result.error:
#                 print(f"Error downloading piece {result.index}: {result.error}")
#             else:
#                 calculated_hash = hashlib.sha1(result.data).digest()
#                 if calculated_hash != tf["PieceHashes"][result.index]:
#                     print(f"Piece {result.index} hash mismatch!")
#                 else:
#                     print(f"Successfully downloaded piece {result.index} of {tf['Name']}")

#         if torrent.merge_pieces(tf["Name"], pieces_by_index):
#             print(f"Download complete for file: {tf['Name']}")
#             tracker_address = tf["Announce"]
#             torrent.create([tf["Name"]], tracker_address)
#             connect_to_tracker(tracker_address, peer_address, tf["Name"])
#         else:
#             print(f"Error merging pieces for {tf['Name']}.")

#     print("All downloads complete!")

def download_worker(peer, work_queue, results, info_hash):
    while work_queue:
        piece = work_queue.pop(0)
        print(f"Downloading piece {piece.index} from peer {peer}")
        data, error = request_piece_from_peer(peer, piece.index, info_hash)
        results.append(PieceResult(piece.index, data, error))

def request_piece_from_peer(address, piece_index, info_hash):
    try:
        with socket.create_connection((address.split(":")[0], int(address.split(":")[1])), timeout=60) as conn:
            perform_handshake(address, info_hash)
            message = f"Requesting:{info_hash.hex()}:{piece_index}\n".encode()
            conn.sendall(message)

            size_header = conn.recv(8)
            piece_size = struct.unpack(">Q", size_header)[0]

            data = conn.recv(piece_size)
            return data, None
    except Exception as e:
        return None, str(e)

def test_connection(address):
    try:
        with socket.create_connection((address.split(":")[0], int(address.split(":")[1])), timeout=5) as conn:
            conn.sendall(b"test:\n")
            response = conn.recv(1024).decode()
            print(f"Received response: {response}")
            return True
    except Exception as e:
        print(f"Test connection failed: {e}")
        return False

def perform_handshake(address, info_hash):
    try:
        with socket.create_connection((address.split(":")[0], int(address.split(":")[1])), timeout=5) as conn:
            handshake_msg = f"HANDSHAKE:{info_hash.hex()}\n".encode()
            conn.sendall(handshake_msg)
            response = conn.recv(1024).decode()
            return response.strip() == "OK"
    except Exception as e:
        print(f"Handshake failed: {e}")
        return False
    
def AnnounceToTracker( peer_address, filename):
    try:
        torrent_info = torrent.parse_torrent_file(filename)

        tracker_url = torrent_info['announce']
        filename = torrent_info['name']

        print(tracker_url)

        connect_to_tracker(tracker_url, peer_address, filename)

        exist = any(
                    tracker["address"] == tracker_url and tracker["filename"] == filename 
                    for tracker in connected_tracker_addresses
                )
        if not exist:
                connected_tracker_addresses.append({
                    "address": tracker_url,
                    "filename": filename
                })
                print(f"Tracker {tracker_url} added for file {filename}")
        else:
                print("Already connected to this tracker for this file")
    except Exception as e:
        print(f"Failed to announce to tracker: {e}")
    # try:
    #     with open(f"torrent_files/{filename}", "r") as f:
    #     #     torrent_files = json.load(f)
        
    #     # for tf in torrent_files:
    #     #     tracker_address = tf["announce"]
    #         # filename = tf["FileName"]
    #         bencoded_data = f.read()
    #         tracker_address = bencodepy.decode(bencoded_data)
    #         print(tracker_address)
            # print(filename)
            # connect_to_tracker(tracker_address, peer_address, filename)
            
            # exist = any(
            #     tracker["Addr"] == tracker_address and tracker["Filename"] == filename 
            #     for tracker in connected_tracker_addresses
            # )
            
            # if not exist:
            #     connected_tracker_addresses.append({
            #         "Addr": tracker_address,
            #         "Filename": filename
            #     })
            #     print(f"Tracker {tracker_address} added for file {filename}")
            # else:
            #     print("Already connected to this tracker for this file")
    # except Exception as e:
    #     print(f"Failed to announce to tracker: {e}")

def connect_to_tracker(tracker_address, peer_address, filename):
    try:
        with socket.create_connection((tracker_address.split(":")[0], int(tracker_address.split(":")[1]))) as conn:
            message = f"START:{peer_address}:{filename}\n".encode()
            conn.sendall(message)
            print(f"Connected to tracker {tracker_address} for file {filename}")
    except Exception as e:
        print(f"Connection to tracker failed: {e}")

def Seed(peer_id, peer_address, filename ):
    try:
        torrent_info = torrent.parse_torrent_file(filename)

        tracker_url = torrent_info['announce']

        print(tracker_url)

        print(seedToTracker(tracker_url,peer_id, peer_address, filename))

        exist = any(
                    tracker["address"] == tracker_url and tracker["filename"] == filename 
                    for tracker in connected_tracker_addresses
                )
        if not exist:
                connected_tracker_addresses.append({
                    "address": tracker_url,
                    "filename": filename
                })
                print(f"Tracker {tracker_url} added for file {filename}")
        else:
                print("Already connected to this tracker for this file")
    except Exception as e:
        print(f"Failed to announce to tracker: {e}")

def seedToTracker(tracker_url, peer_id, peer_ip, filename):
    info_hash = torrent.get_info_hash(filename)
    total_length = torrent.get_total_length_from_torrent(filename)

    from threading import Thread

    def periodic_seed_announce():
        while True:
            tracker_request(
                tracker_url=tracker_url,
                info_hash=info_hash,
                peer_id=peer_id,
                peer_ip=peer_ip,
                downloaded=total_length,
                event="completed"
            )
            time.sleep(1800)

    seed_announce_thread = Thread(target=periodic_seed_announce, daemon=True)
    seed_announce_thread.start()

def Download(peer_id, peer_ip, torrentfile):
    try:
        torrent_info = torrent.parse_torrent_file(torrentfile)
        tracker_url = torrent_info['announce']

        info_hash = torrent.get_info_hash(torrentfile)
        total_length = torrent.get_total_length_from_torrent(torrentfile)

        tracker_response = tracker_request(tracker_url=tracker_url,
                                           info_hash=info_hash,
                                           peer_id=peer_id,
                                           peer_ip=peer_ip,
                                           left=total_length
                                       )
        
        peers = getPeerList(tracker_response)
        peers.remove(peer_ip)
        print(peers)
        
    except Exception as e:
        print(f"DOWNLOAD: Failed to announce to tracker: {e}")

def getPeerList(response: str):
    peers_line = next(line for line in response.splitlines() if line.startswith('peers='))
    peers = peers_line[len("peers="):].split(',')
    print(peers)
    return peers



def tracker_request(tracker_url, info_hash, peer_id, peer_ip, port=8080, downloaded=0, left=0, event="started"):
    """Send a request to the tracker."""
    # Construct the query parameters
    params = {
        'info_hash': info_hash,
        'peer_id': peer_id,
        'peer_ip': peer_ip,
        'port': port,
        'downloaded': downloaded,
        'left': left,
        'compact': 0,  # Request compact response (can also be 0 for verbose response)
        'event': event  # Can be 'started', 'completed', 'stopped', or omitted
    }

    # Send the GET request to the tracker
    response = requests.get(f"{tracker_url}/announce", params=params)

    # Check if the request was successful
    if response.status_code == 200:
        print("Tracker response:")
        print(response.text)  # Print the raw text response from the tracker
        return response.text
    else:
        print(f"Failed to connect to tracker. Status code: {response.status_code}")
        return None
# Remaining functions like `disconnect_to_tracker` and `get_list_of_peers` can be implemented similarly.
