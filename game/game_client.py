# /usr/bin/env python3

import socket

tries = int(input("Tries: "))
max_number = int(input("Max number: "))
role = input("Role: ")

config_string = f"{tries}-{max_number}-{role}"

# same client as the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 9999))

client.send(config_string.encode())
print(client.recv(1024).decode())
client.send(input().encode())

while True:
    message = client.recv(1024).decode()
    print(message)
    if "tries" in message or "lost" in message or "Invalid" in message:
        break
    if role == "guesser":
        client.send(input().encode())