peer_info = {}
def b():
    peer_info["toan"] = []
    peer_info["toan"].append(1)
    peers = peer_info.get("toan", [])
    print(peers)
    
def a(input):
    
    if(input == 1):
        b()
    
    if(input == 2):
        # peers = peer_info.get("toan", [])
        # print(peers)
        print("a")
    

if __name__  == "__main__":
    print("aha")
    args = ['Toan.pdf', '1234', 'info_hash', '5678']
    a = "Toan.pdf: asd"
    print((args[0]) == "Toan.pdf")