import bencodepy
import hashlib

def handle_torrent_file(torrent_file_path):
    try:
        # Mở và đọc nội dung của file torrent
        with open(torrent_file_path, "rb") as f:
            torrent_data = bencodepy.decode(f.read())

        # Kiểm tra các thành phần chính của file torrent
        if b'announce' not in torrent_data:
            raise ValueError("Announce URL missing in torrent file.")
        if b'info' not in torrent_data:
            raise ValueError("Torrent info section is missing.")
        
        # Lấy URL tracker
        tracker_url = torrent_data[b'announce'].decode()

        # Lấy thông tin file
        file_info = torrent_data[b'info']
        file_name = file_info[b'name'].decode()
        file_length = file_info[b'length']
        piece_length = file_info[b'piece length']
        
        # Kiểm tra hash của các phần (pieces)
        pieces = file_info[b'pieces']
        pieces_count = len(pieces) // 20  # Mỗi hash có độ dài 20 byte
        
        # Tạo thông tin torrent chi tiết
        torrent_details = {
            "tracker_url": tracker_url,
            "file_name": file_name,
            "file_size": file_length,
            "piece_length": piece_length,
            "pieces_count": pieces_count
        }

        return torrent_details

    except FileNotFoundError:
        print(f"Error: The file {torrent_file_path} was not found.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Ví dụ sử dụng hàm
torrent_info = handle_torrent_file("data/example.pdf.torrent")
if torrent_info:
    print("Torrent Info:")
    for key, value in torrent_info.items():
        print(f"{key}: {value}")
