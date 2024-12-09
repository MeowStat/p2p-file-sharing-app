import socket
import struct
import threading
import hashlib
import json
import bencodepy
import torrent

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

def start_download(torrent_file, peer_list, mypeer_address):
    torrent_info = torrent.parse_torrent_file(torrent_file)
    print(f"Starting download for: {torrent_file}")

    if not torrent_info:
        print("Fail to parse torrent file.")
        return
    
    active_peer = []
    for peer in peer_list:
        print(f"Testing connection to peer: {peer}")
        if test_connection(peer):
            print(f"Peer {peer} is available")
        else:
            print(f"Peer {peer} is not available")
    # if not active_peers:
    #     print("No active peers found!")
    #     return
    
def get_list_of_peer(tracker_url, filename):
    print(tracker_url)
    try:
        conn = socket.create_connection((tracker_url.split(":")[0], int(tracker_url.split(":")[1])))
    except Exception as e:
        return f"Connection failed: {e}"
    
    try:
        message = f"LIST:{filename}"

        conn.sendall(message.encode())

        response = b""
        while True:
            chunk = conn.recv(1024)
            if not chunk or b"!" in chunk:
                response += chunk
                break
        
        print(response)
    except Exception as e:
        return f"Failed to communicate with tracker: {e}"
    finally:
        conn.close()


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

def test_connection(peer):
    try:
        with socket.create_connection((peer, 8080), timeout=5) as conn:
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

        print("peer address: ", peer_address)

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

def connect_to_tracker(tracker_address, peer_address, filename):
    try:
        with socket.create_connection((tracker_address.split(":")[0], int(tracker_address.split(":")[1]))) as conn:
            message = f"START:{peer_address}:{filename}\n".encode()
            conn.sendall(message)
            print(f"Connected to tracker {tracker_address} for file {filename}")
    except Exception as e:
        print(f"Connection to tracker failed: {e}")

# Remaining functions like `disconnect_to_tracker` and `get_list_of_peers` can be implemented similarly.
