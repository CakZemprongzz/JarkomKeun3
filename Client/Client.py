from socket import *  # Importing the necessary modules
import mimetypes  # Importing the mimetypes module

while True:  # Start an infinite loop
    serverName = 'localhost'  # Server name or IP address 
    serverPort = 12000  # Server port number

    clientSocket = socket(AF_INET, SOCK_STREAM)  # Create a client socket
    clientSocket.connect((serverName, serverPort))  # Connect to the server

    status = input('Retrieve file from server or Send file to the server (Retrieve/Send) : ').lower()  # Choose to retrieve or send a file
    clientSocket.send(status.encode())  # Send the chosen option to the server

    if status == 'retrieve':  # If retrieving a file from the server
        print('\nThe maximum is 100MB !')
        filename = input('Enter the name of the file you want to retrieve: ')  # Input the file name to retrieve
        request = f"GET /{filename} HTTP/1.1\r\nHost: {serverName}\r\n\r\n"  # Create the HTTP GET request

        clientSocket.send(request.encode())  # Send the request to the server
        response = clientSocket.recv(1024)  # Receive the response from the server
        print(response.decode())  # Print the HTTP response message
        if response.decode().startswith('HTTP/1.1 200 OK'):  # If the response indicates success (file found)
            with open(filename, 'wb') as f:  # Open a file to save the received data
                while True:  # Loop to receive and write the file data
                    data = clientSocket.recv(104857600)  # Receive data of specified length
                    if not data:  # If no more data is received, break the loop
                        break
                    f.write(data)  # Write the received data to the file
            print('File saved to', filename)  # Print a message indicating successful file retrieval
        clientSocket.close()  # Close the client socket after retrieval

    elif status == 'send':  # If sending a file to the server
        try:
            print('\nThe maximum is 100MB !') #Print max data info
            filename = '/' + input('Enter the name of the file you want to send: ')  # Input the file name to send
            with open(filename[1:], 'rb') as f:  # Open the file in binary mode for reading
                outputdata = f.read()  # Read the content of the file
            dataLength = str(len(outputdata))  # Convert the length of the output data to a string
            if int(dataLength) > 100 * 1024 * 1024:  # Check if the file size exceeds 100MB

                raise IOError("File size exceeds the limit")
            message = f"POST {filename} HTTP/1.1\r\nHost: {serverName}\r\n\r\n"  # Create the HTTP POST request
            clientSocket.send(message.encode())  # Send the request to the server
            clientSocket.send("HTTP/1.1 200 OK\r\n".encode())  # Send an OK response to the server
            content_type, encoding = mimetypes.guess_type(filename)  # Guess the content type and encoding
            clientSocket.sendall(outputdata)  # Send the file data to the server
            clientSocket.close()  # Close the client socket after sending
        except IOError:  # If the file is not found or too big
            print("\nThe file size is too big, please choose smaller file!")
            errorMessage = f"HTTP/1.1 404 Not Found\r\nFile not found or exceeds size limit\r\n"
            clientSocket.send(errorMessage.encode())  # Send a 404 Not Found response to the client
            clientSocket.close()  # Close the connection socket

    choice = input('\nDo you want to retrieve/send another file? (yes/no): ')  # Ask if the user wants to retrieve another file
    if choice.lower() == 'no':  # If the answer is no
        break  # Exit the loop and end the program