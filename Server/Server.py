
from socket import *
import sys 


serverSocket = socket(AF_INET, SOCK_STREAM)


serverPort = 12000
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

print('Server Port is at : ',serverPort)

while True:

    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        f.close()
    
        connectionSocket.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n".encode())
 
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
    except IOError:

        connectionSocket.send("Not found \n".encode())

connectionSocket.close()
serverSocket.close()
sys.exit()
