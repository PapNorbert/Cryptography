import socket
import sys
import threading
from socket import *

from lab3.knapsack import generate_private_key_knapsack, create_public_key_knapsack


class MyThread(threading.Thread):
    def __init__(self, threadID, clientSocket, host, port, keyServerPort):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.clientSocket = clientSocket
        self.host = host
        self.port = port
        self.keyServerPort = keyServerPort

    def run(self):
        self.connectToClient()

    def connectToClient(self):
        try:
            # print(f'thread {self.threadID} started\n')

            self.clientSocket.connect((self.host, self.port))

            print("Connected to other client socket")

        except Exception as exception:
            print(exception)

        finally:
            self.clientSocket.close()
        # print(f'thread {self.threadID} stopped\n')


# run: client.py myPort
def main():
    try:  # 1st paramter - own port number
        myPort = int(sys.argv[1])
        host = "127.0.0.1"
        keyServerPort = 8000

        privateKey = generate_private_key_knapsack()
        publicKey = create_public_key_knapsack(privateKey)
        registerToKeyServer(host, keyServerPort, myPort, publicKey)

        thread = -1
        secondPort = -1
        connectToOtherClient = False
        try:  # 2nd parameter
            secondPort = int(sys.argv[2])
            connectToOtherClient = True
        except IndexError:
            pass

        if connectToOtherClient:
            clientSocket = socket(AF_INET, SOCK_STREAM)

            thread = MyThread(1, clientSocket, host, secondPort, keyServerPort)
            thread.start()

        mySocket = socket(AF_INET, SOCK_STREAM)
        mySocket.settimeout(10)
        try:
            mySocket.bind((host, myPort))
            print("Listening on my socket at port ", myPort)
            mySocket.listen()
            connection, _address = mySocket.accept()
            print("Other client connected to my socket")

            connection.close()

            mySocket.close()

        except TimeoutError:
            # print('\t\tTimeout on own socket')
            pass

        if connectToOtherClient:
            thread.join()

    except IndexError:
        print('Please specifie own port number')
    except ValueError:
        print('First parameter must be a number, own port number')


def registerToKeyServer(host, keyServerPort, myPort, myKey):
    keyServerSocket = socket(AF_INET, SOCK_STREAM)
    keyServerSocket.connect((host, keyServerPort))
    message = "REGISTER " + myPort + " " + myKey
    keyServerSocket.send(message.encode())
    response = keyServerSocket.recv(1024).decode()
    print(response)


if __name__ == "__main__":
    main()
