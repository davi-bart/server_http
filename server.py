import signal
import sys
from socket import *
import threading
SERVER_PORT = 8080
SERVER_ADDRESS = ('', SERVER_PORT)
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
serverSocket.bind(SERVER_ADDRESS)


def serve_request(connection):
    try:
        message = connection.recv(1024)
        if len(message.split()) > 0:
            print(message.split()[0], ':', message.split()[1])
            filename = message.split()[1]
            if filename == b'/':
                filename = b'/index.html'
            f = open(filename[1:], 'r+')
            outputdata = f.read()

            connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
            connectionSocket.send(outputdata.encode())
            connectionSocket.send("\r\n".encode())
            connectionSocket.close()
    except IOError:
        # File non trovato
        connectionSocket.send(bytes("HTTP/1.1 404 Not Found\r\n\r\n", "UTF-8"))
        connectionSocket.send(bytes("<html><head></head><body><h1>404 Not Found :(</h1></body></html>\r\n", "UTF-8"))
        connectionSocket.close()


serverSocket.listen(1)
print('the web server is up on port:', SERVER_PORT)


def signal_handler(signal, frame):
    print('Exiting http server (Ctrl+C pressed)')
    try:
        serverSocket.close()
    finally:
        sys.exit(0)


# interrompe l’esecuzione se da tastiera arriva la sequenza (CTRL + C)
signal.signal(signal.SIGINT, signal_handler)

while True:
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    print(connectionSocket, addr)
    threading.Thread(target=serve_request, args=(connectionSocket,), daemon=True).start()
