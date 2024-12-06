from socket import *

def get_peer_list(tracker_ip, tracker_port):
    try:
        # Tạo socket kết nối đến tracker
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((tracker_ip, tracker_port))
        
        # Gửi yêu cầu lấy danh sách peer
        client_socket.send('GET_LIST_PEER'.encode('utf-8'))
        
        peer_list = []
        while True:
            # Nhận dữ liệu từ tracker
            data = client_socket.recv(1024).decode('utf-8')
            
            if data == 'FINISH':
                break
            
            # Nhận IP
            peer_ip = data
            client_socket.send('OK'.encode('utf-8'))
            
            # Nhận port
            peer_port = client_socket.recv(1024).decode('utf-8')
            client_socket.send('OK'.encode('utf-8'))
            
            # Thêm vào danh sách
            peer_list.append((peer_ip, int(peer_port)))
        
        client_socket.close()
        return peer_list
    
    except Exception as e:
        print(f"Error connecting to tracker: {e}")
        return []

if __name__ == "__main__":
    # Địa chỉ IP và cổng của tracker
    tracker_ip = 'localhost'  # Thay đổi nếu cần
    tracker_port = 22222
    
    print("Requesting peer list from tracker...")
    peers = get_peer_list(tracker_ip, tracker_port)
    
    print("Peer list received:")
    for ip, port in peers:
        print(f"Peer IP: {ip}, Port: {port}")
