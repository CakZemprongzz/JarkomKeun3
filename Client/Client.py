from socket import *
import sys
import mimetypes

while True :
    serverName = 'localhost' #input('Enter the IP : ')
    serverPort = 12000 #int(input('Enter the Port : '))

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))

    status = input('Retrieve file from server or Send file to the server (Retrieve/Send) : ').lower()
    clientSocket.send(status.encode())

    if status == 'retrieve': #Retrieve from the server
        filename = input('Enter the name of the file you want to retrieve: ')
        request = f"GET /{filename} HTTP/1.1\r\nHost: {serverName}\r\n\r\n"
        clientSocket.send(request.encode())
        response = clientSocket.recv(1024)
        print(response.decode()) # Print the HTTP response message
        if response.decode().startswith('HTTP/1.1 200 OK'): # Save the content of the requested file to a local file
            responseData = clientSocket.recv(1024)
            with open(filename, 'wb') as f:
                while True:
                    data = clientSocket.recv(int(responseData.decode()))
                    if not data:
                        break
                    f.write(data)
            print('File saved to',filename)
        clientSocket.close()

    elif status == 'send': #Uploading to the server
        try: 
            filename = input('Enter the name of the file you want to send: ')
            filename = '/' + filename
            with open(filename[1:], 'rb') as f:
                outputdata = f.read()
            message = f"POST {filename} HTTP/1.1\r\nHost: {serverName}\r\nContent-Length: {outputdata}\r\n\r\n"
            clientSocket.send(message.encode())
            print('Output data length:', len(outputdata))
            clientSocket.send("HTTP/1.1 200 OK\r\n".encode())
            outputdataString = str(len(outputdata))
            clientSocket.send(outputdataString.encode())    
            content_type, encoding = mimetypes.guess_type(filename)
            print('Content-Type:', content_type)
            clientSocket.sendall(outputdata)
            clientSocket.close()
        except IOError:     #Send response message if the file not found
            clientSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
            clientSocket.send("\r\n".encode())
            clientSocket.send("File not found".encode())
            clientSocket.close() #Close client socket

    choice = input('\nDo you want to retrieve another file? (yes/no): ')
    if choice.lower() == 'no':
        break
