from socket import *

serverName = 'localhost'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

filename = input('Enter the name of the file you want to retrieve: ')

request = f"GET /{filename} HTTP/1.1\r\nHost: {serverName}\r\n\r\n"
clientSocket.send(request.encode())

response = clientSocket.recv(1024)


print(response.decode()) # Print the HTTP response message


if response.decode().startswith('HTTP/1.1 200 OK'): # Print the content of the requested file, if available
    filedata = b''
    while True:
        data = clientSocket.recv(1024)
        if not data:
            break
        filedata += data
    print(filedata.decode())

clientSocket.close()

