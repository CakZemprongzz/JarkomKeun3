
from socket import *  # Import the socket module
import sys
import mimetypes

serverSocket = socket(AF_INET, SOCK_STREAM)  # Create a server socket

serverPort = 12000  # Prepare a server socket
serverSocket.bind(('', serverPort))  # Associate the server socket with the specified port and the localhost address
serverSocket.listen(1)  # Start listening for incoming client connections (queue up to 1 client)

print('Server Port is at:', serverPort)  # Print the server port

while True:
    print('Ready to serve... waiting for response')  # Wait for incoming connections
    connectionSocket, addr = serverSocket.accept()  # Accept a connection
    status = connectionSocket.recv(1024)  # Receive the status from the client

    if status.decode().startswith('retrieve'):  # If status is "retrieve"
        print('Ready to send to the client!') #Print some Info
        try:
            message = connectionSocket.recv(1024).decode()  # Receive the message from the client
            filename = message.split()[1]  # Extract the filename from the message
            with open(filename[1:], 'rb') as f:  # Open the file in binary mode for reading
                outputdata = f.read()  # Read the content of the file
            connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())  # Send an OK response to the client
            dataLength = str(len(outputdata))  # Convert the length of the output data to a string
            connectionSocket.send(dataLength.encode())  # Send the length of the output data length to the client
            content_type, encoding = mimetypes.guess_type(filename)  # Guess the content type and encoding
            connectionSocket.sendall(outputdata)  # Send the file data to the client
            connectionSocket.close()  # Close the connection socket
        except IOError:  # If the file is not found
            connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())  # Send a 404 Not Found response to the client
            connectionSocket.send("\r\n".encode())  # Send an empty line as part of the response
            connectionSocket.send("File not found".encode())  # Send a message indicating file not found
            connectionSocket.close()  # Close the connection socket

    elif status.decode().startswith('send'):  # If status is "send"
        print('Ready to retrieve from the Client!') #Print some info
        message = connectionSocket.recv(1024).decode()  # Receive the message from the client
        filename = message.split()[1]  # Extract the filename from the message
        request = connectionSocket.recv(1024)  # Receive the request from the client
        if request.decode().startswith('HTTP/1.1 200 OK'):  # If the request is successful
            dataLength = connectionSocket.recv(1024)  # Receive the file data length from the client
            with open(filename[1:], 'wb') as f:  # Open a file to save the received data
                while True:  # Loop to receive and write the file data
                    data = connectionSocket.recv(int(dataLength))  # Receive data of specified length
                    if not data:  # If no more data is received, break the loop
                        break
                    f.write(data)  # Write the received data to the file
            print('File saved to', filename[1:])  # Saving file
        connectionSocket.close()  # Close the connection socket

serverSocket.close()  # Close the server socket
sys.exit()  # Terminate the program sending the corresponding data
