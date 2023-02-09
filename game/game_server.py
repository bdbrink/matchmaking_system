# /usr/bin/env python3

import socket
import threading

# same IP and port the client is using
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 9999))

server.listen()

connected_client = []

# send to both clients if there is a match
def handle_match(c1, c2):
    tries, max_num = c1[1].split("-")
    tries, max_num = int(tries), int(max_num)

    if c1[2] != "decider":
        c1, c2 = c2, c1

    c1[0].send("Enter the number to be guessed".encode())
    number = int(c1[0].recv(1024).decode())

    if number > max_num:
        c1[0].send("Invalid Range!".encode())
        c2[0].send("Your boo thing messed up! Invalid range!".encode())
        c1[0].close()
        c2[0].close()
    else:
        guessed = False
        try_counter = 0
        c2[0].send("Enter your guess: ".encode())
        while not guessed:
            try_counter += 1
            guess = int(c2[0].recv(1024).decode())
            if guess == number:
                c2[0].send(f"Correct! it took you {try_counter} tries!".encode())
                c1[0].send(f"Your bestie gestie was correct after {try_counter} tries".encode())
                c1[0].close()
                c2[0].close()
                guessed = True
            else:
                if try_counter >= tries:
                    c2[0].send(f"You lost :( The number was {number})".encode())
                    c1[0].send(f"You bestie lost :( The number was {number})".encode())
                    c1[0].close()
                    c2[0].close()
                    break
                else:
                    if guess < number:
                        c2[0].send("Your guess is too low try again: ".encode())
                        c1[0].send(f"Your bestie gestie {guess} is too low try again: ".encode())
                    elif guess > number:
                        c2[0].send("Your guess is too high try again: ".encode())
                        c1[0].send(f"Your bestie gestie {guess} is too low try again: ".encode())

# when client is started this will prompt the user
def handle_client(c):
    config_string = client.recv(1024).decode()
    config = config_string[:config_string.rfind("-")]
    role = config_string[:config_string.rfind("-")+1:]
    
    found_match = False
    for item in range(len(connected_client)):
        if connected_client[item][1] == config:
            if connected_client[item][2] != role:
                print("MATCH")
                threading.Thread(target=handle_match, args=(c, config, role, connected_client[item])).start()
            del connected_client[item]
            found_match = True
            break

    if not found_match:
        connected_client.append((c, config, role))

while True:
    client, addr = server.accept()
    threading.Thread(target=handle_client, args=(client,)).start()
