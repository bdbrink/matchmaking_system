# /usr/bin/env python3

import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 9999))

server.listen()

connected_client = []

def handle_match(c1, c2):
    c1.send("MATCH".encode())
    c2.send("MATCH".encode())

def handle_client(c):
    c.send("Enter matching string: ".encode())
    matching_string = client.recv(1024).decode()
    found_match = False
    for item in range(len(connected_client)):
        if connected_client[item][1] == matching_string:
            threading.Thread(target=handle_match, args=(c, connected_client[item][0])).start()
            del connected_client[item]
            found_match = True

    if not found_match:
        connected_client.append((c, matching_string))

while True:
    client, addr = server.accept()
    threading.Thread(target=handle_client, args=(client,)).start()
