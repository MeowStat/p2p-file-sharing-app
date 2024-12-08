import hashlib
import os
import json
import bencodepy
from typing import List
import hashlib
import os
import json
import bencodepy
from typing import List
def create_torrent(path: List[str], tracker_url: str) -> str:
    # Combine paths into a single string and create a hash for the filename
    if (len(path) > 1):
        combined_path = ",".join(path)
        hash_file_name = hashlib.sha1(combined_path.encode('utf-8')).hexdigest()
        torrent_file_name = f"{hash_file_name}.torrent"
    else:
        torrent_file_name = f"{path[0].split('.')[0]}.torrent"
    
    # Prepare the torrent metadata
    torrent_metadata = {
        'announce': tracker_url,
        'info': {
            'name': os.path.basename(path[0]),  # contain the file/folder name
            'piece length': 256 * 1024,  
            'pieces': b'',  
            'files': [{'length': os.path.getsize(os.path.join("files", file)), 'path': [file]} for file in path]
        }
    }
    # Add pieces to torrent metadata
    pieces = []
    total_size = 0
    for file in path:
        folder_path = "files"
        file = os.path.join(folder_path,file)
        with open(file, 'rb') as f:
            while chunk := f.read(256 * 1024):  # Read in 256KB chunks
                pieces.append(hashlib.sha1(chunk).digest())
                total_size += len(chunk)
    torrent_metadata['info']['pieces'] = b''.join(pieces)
    # Write the torrent file (Bencode format) to the 'torrent_files' directory
    try:
        torrent_dir = "torrent_files"  
        os.makedirs(torrent_dir, exist_ok=True)  
        torrent_file_path = os.path.join(torrent_dir, torrent_file_name)
        
        with open(torrent_file_path, 'wb') as torrent_file:
            torrent_file.write(bencodepy.encode(torrent_metadata))
    except Exception as e:
        print(f"Error creating torrent file: {e}")
        return ""
    return torrent_file_name
# Helper function to decode bytes to strings
def decode_bytes(obj):
    """Recursively decode bytes to strings."""
    if isinstance(obj, bytes):
        return obj.decode('utf-8', errors='ignore')  # Decode bytes to string (ignore errors)
    elif isinstance(obj, dict):
        return {decode_bytes(key): decode_bytes(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [decode_bytes(item) for item in obj]
    else:
        return obj
# Function to read the torrent and convert it to JSON format
def read_torrent_as_json(torrent_file_path: str) -> str:
    try:
        # Open the torrent file in binary mode
        with open(torrent_file_path, 'rb') as torrent_file:
            # Decode the torrent file using bencodepy
            torrent_data = bencodepy.decode(torrent_file.read())
        # Decode bytes to strings
        decoded_data = decode_bytes(torrent_data)
        # Convert the decoded data into JSON format (with pretty-printing)
        json_data = json.dumps(decoded_data, indent=4)
        return json_data
    except Exception as e:
        print(f"Error reading or converting torrent file: {e}")
        return ""
    try:
        # Open the torrent file in binary mode
        with open(torrent_file_path, 'rb') as torrent_file:
            # Decode the torrent file using bencodepy
            torrent_data = bencodepy.decode(torrent_file.read())
        
        # Return the decoded data (torrent metadata as a dictionary)
        return torrent_data
    except Exception as e:
        print(f"Error reading torrent file: {e}")
        return None
    
def get_info_hash(torrent_file_path: str) -> str:
    try:
        # Read the torrent file and decode it from Bencode
        torrent_file_path = os.path.join("torrent_files",torrent_file_path)
        with open(torrent_file_path, 'rb') as f:
            torrent_data = f.read()
        
        # Decode the Bencoded data
        torrent_metadata = bencodepy.decode(torrent_data)
        
        # Extract the 'info' dictionary from the metadata
        info = torrent_metadata.get(b'info')

        if info is None:
            raise ValueError("The 'info' dictionary was not found in the torrent file.")

        # Bencode the 'info' dictionary and compute the SHA1 hash
        info_bencoded = bencodepy.encode(info)
        info_hash = hashlib.sha1(info_bencoded).digest()

        # Return the info_hash as a hex string
        return info_hash.hex()

    except Exception as e:
        print(f"Error reading torrent file: {e}")
        return None
    
def get_total_length_from_torrent(torrent_file):
    # Read the .torrent file
    torrent_file = os.path.join("torrent_files",torrent_file)
    with open(torrent_file, 'rb') as f:
        torrent_data = bencodepy.decode(f.read())

    # Get the 'files' list inside the 'info' dictionary
    files = torrent_data[b'info'][b'files']
    
    # Sum the 'length' of each file to get the total size in bytes
    total_length = sum(file[b'length'] for file in files)
    
    return total_length

def parse_torrent_file(filename):
    try:
        # Mở tệp torrent ở chế độ nhị phân
        with open(f"torrent_files/{filename}", "rb") as f:
            encoded_torrent = f.read()
        
        # Giải mã dữ liệu từ tệp torrent
        torrent_data = bencodepy.decode(encoded_torrent)
        
        # Trích xuất thông tin cần thiết
        announce_url = torrent_data.get(b'announce', b'').decode('utf-8')
        info = torrent_data.get(b'info', {})
        name = info.get(b'name', b'').decode('utf-8')
        piece_length = info.get(b'piece length', 0)
        pieces = info.get(b'pieces', b'')
        files = []

        if b'files' in info:
            for file in info[b'files']:
                length = file.get(b'length', 0)
                path = b'/'.join(file.get(b'path', [])).decode('utf-8')
                files.append({'length': length, 'path': path})
        else:
            # Chế độ đơn tệp
            length = info.get(b'length', 0)
            files.append({'length': length, 'path': name})
        
        # Trả về thông tin đã giải mã
        return {
            'announce': announce_url,
            'name': name,
            'piece_length': piece_length,
            'pieces': pieces,
            'files': files
        }

    except Exception as e:
        print(f"Error parsing torrent file: {e}")
        return None