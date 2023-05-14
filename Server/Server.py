
from socket import * #import socket module
import sys 
import mimetypes

serverSocket = socket(AF_INET, SOCK_STREAM) # In order to terminate the program

serverPort = 12000 #Prepare a server socket
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

print('Server Port is at :',serverPort)

while True:
    print('Ready to serve... waiting for respond') #Establish the connection
    connectionSocket, addr = serverSocket.accept()
    status = connectionSocket.recv(1024)

    if status.decode().startswith('retrieve'): #Send to the client
        print('Ready to send to the client!')
        try:
            message = connectionSocket.recv(1024).decode()
            filename = message.split()[1]
            print(filename)
            with open(filename[1:], 'rb') as f:
                outputdata = f.read()
            print('Output data length:', len(outputdata))
            connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
            outputdataString = str(len(outputdata))
            connectionSocket.send(outputdataString.encode())    
            content_type, encoding = mimetypes.guess_type(filename)
            print('Content-Type:', content_type)
            connectionSocket.sendall(outputdata)
            connectionSocket.close()
        except IOError:     #Send response message if the file not found
            connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
            connectionSocket.send("\r\n".encode())
            connectionSocket.send("File not found".encode())
            connectionSocket.close() #Close client socket

    elif status.decode().startswith('send'): #Retrieve from the client
        print('Ready to retrieve')
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1] 
        print(filename)
        request = connectionSocket.recv(1024)
        print(request.decode())
        if request.decode().startswith('HTTP/1.1 200 OK'): # Save the content of the requested file to a local file
            responseData = connectionSocket.recv(1024)
            with open(filename, 'wb') as f:
                while True:
                    data = connectionSocket.recv(int(responseData.decode()))
                    if not data:
                        break
                    f.write(data)
            print('File saved to',filename)
        connectionSocket.close()
        
serverSocket.close()
sys.exit() #Terminate the program sending the corresponding data

