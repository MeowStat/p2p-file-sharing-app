import hashlib
import bencodepy

def create_torrent(file_path, tracker_url, piece_length=512*1024):
    # Mở file và đọc dữ liệu
    with open(file_path, "rb") as f:
        data = f.read()
    
    # Tính toán các pieces (hash SHA-1)
    pieces = [hashlib.sha1(data[i:i+piece_length]).digest() for i in range(0, len(data), piece_length)]
    
    # Tạo metainfo
    torrent = {
        "announce": tracker_url,
        "info": {
            "name": file_path.split('/')[-1],  # Tên file
            "length": len(data),             # Kích thước file
            "piece length": piece_length,    # Kích thước mỗi phần
            "pieces": b"".join(pieces)       # Ghép các hash lại
        }
    }
    
    # Ghi file .torrent
    torrent_file = f"{file_path}.torrent"
    with open(torrent_file, "wb") as f:
        f.write(bencodepy.encode(torrent))
    print(f"Torrent file created: {torrent_file}")

# Ví dụ sử dụng
create_torrent("data/example.pdf", "http://your-tracker-portal.local/announce")
