
from socket import * #import socket module
import sys 


serverSocket = socket(AF_INET, SOCK_STREAM) # In order to terminate the program

serverPort = 12000 #Prepare a server socket
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

print('Server Port is at : ',serverPort)

while True:

    print('Ready to serve...') #Establish the connection
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        f.close()
        connectionSocket.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n".encode())   #Send one HTTP header line into socket
        for i in range(0, len(outputdata)): #Send the content of the requested file to the client
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
    except IOError:     #Send response message if the file not found
        connectionSocket.send("Not found \n".encode()) 

connectionSocket.close() #Close client socket
serverSocket.close()
sys.exit() #Terminate the program sending the corresponding data

