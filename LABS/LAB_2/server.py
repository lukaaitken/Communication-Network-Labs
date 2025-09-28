# http://localhost:8080/helloworld.html
#!/usr/bin/env python3
import socket
#other optional modules include sys, argparse, threading
serverPort = 8080
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#Prepare a sever socket
#Fill in start
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
#Fill in end
while True:
    #Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()#Fill in start #Fill in end
    try:
        message = connectionSocket.recv(1024).decode()
        print(message)
        filename = message.split()[1]
        f = open(filename[1:], 'rb')
        outputdata = f.read()
        f.close()
        #Fill in start #Fill in end
		#Send one HTTP header line into socket
		#Fill in start
        header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        connectionSocket.send(header.encode())
        #Fill in end
		#Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(bytes([outputdata[i]]))
        connectionSocket.close()

    except IOError:
        #Send response message for file not found
		#Fill in start
		#Fill in end
		#Close client socket
		#Fill in start
        header = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n"
        body = "<html><body><h1>404 Not Found</h1></body></html>"
        connectionSocket.send(header.encode())
        connectionSocket.send(body.encode())

        connectionSocket.close()
        #Fill in end
serverSocket.close()