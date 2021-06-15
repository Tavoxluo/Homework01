# import

from socket import *
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys #In order to terminate the program
import time
import socket

# Create a TCP server socket
# (socket.AF_INET is used for IPv4 protocols)
# (socket.SOCK_STREAM is used for TCP)

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Assign a host and port number
serverHost, serverPort = '', 8080

listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to server address and server port
listen_socket.bind((serverHost, serverPort))

# Listen to at most 1 connection at a time
listen_socket.listen(1)


# Server should be up and running and listening to the incoming connections
while True:
    print('Serving HTTP on port ' + str(serverPort) + '...')

    # Set up a new connection from the client
    client_connection, client_address = listen_socket.accept()

    # If an exception occurs during the execution of try clause
    # the rest of the clause is skipped
    # If the exception type matches the word after except
    # the except class is executed

    try:
        # Receives the request message from the client
        requst_date = client_connection.recv(1024).decode()
        print('receiving a new request')

        # Let webserverText be the page's name
        f = open('webserverText.html', 'rb')

        # Store the entire contenet of the requested file in a temporary buffer
        output_data = f.read()

        # Send the HTTP response header line to the connection socket
        client_connection.send("HTTP/1.1 200 OK \r\n\r\n".encode())

        # Send the content of the requested file to the client connection socket
        # for i in range (0, len(output_data)-10) ?
        #   client_connection.send(output_data[i],encode())
        # client_connection.send('\r\n'.encode())
        # Or use client_connection.sendall(output_data)

        client_connection.send(output_data[0:1000]) 

        # close the client connection socket
        client_connection.close()


    except IOError:
        # Send HTTP response message for file not found
        client_connection.send("HTTP/1.1 404 Not Found \r\n\r\n".encode())
        client_connection.send("<html><body><h1>404 Not Found</h1></body></html\r\n>".encode())

        # Close the client connection socket
        client_connection.close()
        
# Terminate the program after sending the corresponding data
listen_socket.close()
sys.exit()
