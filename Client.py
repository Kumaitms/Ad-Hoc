import socket
import threading
import os
from datetime import datetime
import pytz

# --- Configuration ---
SERVER_IP   = '172.20.10.4'  # CHANGE THIS to Server's actual Wi-Fi IP
PORT        = 50000
MY_NAME     = 'Client'
REMOTE_NAME = 'Server'
RIYADH_TZ   = pytz.timezone('Asia/Riyadh')

def timestamp():
    return datetime.now(RIYADH_TZ).strftime('%H:%M:%S')

def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if not message:
                break

            # Server sent a clean quit signal
            if message.strip() == '/quit':
                print(f"\n[{timestamp()}] [{REMOTE_NAME}] has left the chat.")
                client.close()
                break

            # Server sent /chrome command — open KFU Blackboard
            if message.strip() == '/chrome':
                print(f"\n[!] CONTROL RECEIVED: Server is opening KFU Blackboard on this machine!")
                os.system("start chrome https://bblms.kfu.edu.sa/")
                continue

            print(f"\n[{REMOTE_NAME}]: {message}")

        except:
            print("\n[-] SENSING: Connection to Server lost.")
            client.close()
            break

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((SERVER_IP, PORT))
        print(f"[+] SENSING: Successfully connected to Server!")
    except Exception as e:
        print(f"Could not find Server. Error: {e}")
        return

    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.daemon = True
    thread.start()

    print("--- CHAT STARTED --- (Type '/quit' to disconnect)")

    while True:
        try:
            msg = input()

            if msg.strip() == '/quit':
                client.send('/quit'.encode('utf-8'))
                print(f"\n[{timestamp()}] You left the chat.")
                client.close()
                break

            client.send(f"[{timestamp()}] {msg}".encode('utf-8'))
        except:
            break

if __name__ == "__main__":
    start_client()