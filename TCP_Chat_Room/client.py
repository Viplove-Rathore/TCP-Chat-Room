import socket
import threading


nickname = input("Enter your nickname: ")

if nickname == 'admin' :
    password = input("Enter your password for admin: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 4545))

stop_thread = False

def receive():
    while True:
        global stop_thread
        if stop_thread :
            break

        try:
            message = client.recv(1024).decode('UTF-8')
            if message == 'NICK':
                client.send(nickname.encode('UTF-8'))
                next_message = client.recv(1024).decode('UTF-8')
                if next_message == 'PASS':
                    client.send(password.encode('UTF-8'))
                    if client.recv(1024).decode('UTF-8') == 'REFUSE':
                        print("Connection refused!")
                        stop_thread = True
                elif next_message == 'BAN':
                    print("Connection banned!")
                    client.close()
                    break
            else:
                print(message)
        except:
            print("An error occured")
            client.close()
            break

def write():
    while True:
        if stop_thread:
            break

        message = f'{nickname} : {input("->")}'
        if message[len(nickname) + 3: ].startswith('/'):
            print("Just Joking")
            
            if nickname == 'admin':
                if message[len(nickname): ].find('/kick'):
                    client.send(f'KICK {message[len(nickname) + 2 + 6:]}'.encode('UTF-8'))
                    print(f'Remove {message[len(nickname) + 2 + 6:]}'.encode('UTF-8'))
                elif message[len(nickname) + 5: ].startswith('/ban'):
                    client.send(f'BAN {message[len(nickname) + 2 + 3:]}'.encode('UTF-8'))
                    print(f'Remove {message[len(nickname) + 2 + 3:]}'.encode('UTF-8'))
            else:
                print("bye bye")

        client.send(message.encode('UTF-8'))

recieve_thread = threading.Thread(target=receive)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
