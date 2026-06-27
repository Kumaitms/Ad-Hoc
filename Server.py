import socket
import threading
import os
from datetime import datetime
import pytz

# --- Configuration ---
HOST        = '172.20.10.5'   # Listens on all available Wi-Fi interfaces
PORT        = 50000        # Ensure this port is free
MY_NAME     = 'Server'
REMOTE_NAME = 'Client'
RIYADH_TZ   = pytz.timezone('Asia/Riyadh')

def timestamp():
    return datetime.now(RIYADH_TZ).strftime('%H:%M:%S')

def handle_client(conn, addr):
    print(f"\n[+] SENSING: Node sensed and connected from {addr}!")

    while True:
        try:
            message = conn.recv(1024).decode('utf-8')
            if not message:
                break

            # /quit — remote client disconnected cleanly
            if message.strip() == '/quit':
                print(f"\n[{timestamp()}] [{REMOTE_NAME}] has left the chat.")
                break

            print(f"\n[{REMOTE_NAME}]: {message}")

        except ConnectionResetError:
            break

    print(f"\n[-] SENSING: Node disconnected/moved away.")
    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print("[*] Server is online and sensing for nearby nodes...")

    conn, addr = server.accept()

    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.daemon = True
    thread.start()

    print(f"--- CHAT STARTED --- (Type '/quit' to disconnect | '/chrome' to open KFU Blackboard on Client)")

    while True:
        try:
            msg = input()

            if msg.strip() == '/quit':
                conn.send('/quit'.encode('utf-8'))
                print(f"\n[{timestamp()}] You left the chat.")
                conn.close()
                break

            # /chrome — send command to client to open KFU Blackboard
            if msg.strip() == '/chrome':
                conn.send('/chrome'.encode('utf-8'))
                print(f"\n[!] CONTROL TRIGGERED: Sent command to open KFU Blackboard on {REMOTE_NAME}!")
                continue

            conn.send(f"[{timestamp()}] {msg}".encode('utf-8'))
        except:
            break

if __name__ == "__main__":
    start_server()