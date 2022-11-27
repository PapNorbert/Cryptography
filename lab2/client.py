import socket
import sys
import threading
from socket import *
from streamEncryption import (encrypt, readConfiguration,
                              processKey)


class MyThread(threading.Thread):
    def __init__(self, threadID, clientSocket, host, port):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.clientSocket = clientSocket
        self.host = host
        self.port = port

    def run(self):
        self.connectToClient()

    def connectToClient(self):
        try:
            # print(f'thread {self.threadID} started\n')

            self.clientSocket.connect((self.host, self.port))

            print("Connected to other client socket")

            correctKey = True
            exiting = False
            keyGenerator, key = readConfiguration('configuration.txt')
            processedKey = key

            if keyGenerator == 'solitaire':
                processedKey = processKey(key)
                if not processedKey:
                    print("Wrong key format")
                    correctKey = False
            else:  # blum-blum-shub
                if not processedKey.isdigit():
                    print("Wrong key format")
                    correctKey = False

            if correctKey:
                while not exiting:
                    text = input('Text to send:\n\t')
                    encryptedText, processedKey = encrypt(text, keyGenerator, processedKey)
                    print('Sending text: ', text)
                    print('\tEncrypted text sent: ', encryptedText)
                    self.clientSocket.send(encryptedText.encode())
                    if text.lower() == 'exit':
                        exiting = True
                        print('Stopping communication')
                    else:
                        resp = self.clientSocket.recv(1024).decode()
                        decryptedResp, processedKey = encrypt(resp, keyGenerator, processedKey)
                        # print('Got message: ', resp)
                        print('Got message after decryption: ', decryptedResp)
                        if decryptedResp.lower() == 'exit':
                            exiting = True
                            print('Stopping communication')

        except Exception as exception:
            print(exception)

        finally:
            self.clientSocket.close()
        # print(f'thread {self.threadID} stopped\n')


# run: client.py myPort [portToConnect]
# opens a socket to receive incoming connection, and connects to [portToConnect] if given
def main():
    try:  # 1st paramter - own port number
        myPort = int(sys.argv[1])
        host = "127.0.0.1"
        secondPort = 0
        thread = 0
        connectToOtherClient = False
        try:  # 2nd parameter - other client port
            secondPort = int(sys.argv[2])
            connectToOtherClient = True
        except IndexError:
            pass

        if connectToOtherClient:
            clientSocket = socket(AF_INET, SOCK_STREAM)

            thread = MyThread(1, clientSocket, host, secondPort)
            thread.start()

        mySocket = socket(AF_INET, SOCK_STREAM)
        mySocket.settimeout(10)
        try:
            mySocket.bind((host, myPort))
            print("Listening on my socket at port ", myPort)
            mySocket.listen()
            connection, _address = mySocket.accept()
            print("Other client connected to my socket")

            correctKey = True
            exiting = False
            keyGenerator, key = readConfiguration('configuration.txt')
            processedKey = key

            if keyGenerator == 'solitaire':
                processedKey = processKey(key)
                if not processedKey:
                    print("Wrong key format")
                    correctKey = False
            else:  # blum-blum-shub
                if not processedKey.isdigit():
                    print("Wrong key format")
                    correctKey = False

            if correctKey:
                while not exiting:
                    msg = connection.recv(1024).decode()
                    decryptedMsg, processedKey = encrypt(msg, keyGenerator, processedKey)
                    # print('Got message: ', msg)
                    print('Got message after decryption: ', decryptedMsg)
                    if decryptedMsg.lower() == 'exit':
                        exiting = True
                        print('Stopping communication')
                    else:
                        text = input('Answer:\n\t')
                        encryptedText, processedKey = encrypt(text, keyGenerator, processedKey)
                        print('Sending text: ', text)
                        print('\tEncrypted text sent: ', encryptedText)
                        connection.send(encryptedText.encode())
                        if text.lower() == 'exit':
                            exiting = True
                            print('Stopping communication')

        except TimeoutError:
            # print('\t\tTimeout on own socket')
            pass

        if connectToOtherClient:
            thread.join()

    except IndexError:
        print('Please specifie own port number')
    except ValueError:
        print('First parameter must be a number, own port number')


if __name__ == "__main__":
    main()
