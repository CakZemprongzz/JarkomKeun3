
from socket import * #import socket module
import sys 
import mimetypes

serverSocket = socket(AF_INET, SOCK_STREAM) # In order to terminate the program

serverPort = 12000 #Prepare a server socket
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

print('Server Port is at :',serverPort)

while True:
    print('Ready to serve...') #Establish the connection
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        with open(filename[1:], 'rb') as f:
            outputdata = f.read()
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        content_type, encoding = mimetypes.guess_type(filename)
        connectionSocket.send(f"Content-Type: {content_type}\r\n".encode())
        connectionSocket.send(f"Content-Length: {len(outputdata)}\r\n".encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.sendall(outputdata)
        connectionSocket.close()
    except IOError:     #Send response message if the file not found
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.send("File not found".encode())
        connectionSocket.close() #Close client socket
 
serverSocket.close()
sys.exit() #Terminate the program sending the corresponding data

