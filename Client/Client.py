from socket import *

serverName = 'localhost' #input('Enter the IP : ')
serverPort = 12000 #int(input('Enter the Port : '))

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

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
    print('File saved to ',filename)

clientSocket.close()
