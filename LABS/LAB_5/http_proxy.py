from socket import *
import os

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)

# Fill in start.
tcpSerSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
tcpSerSock.bind(('', 8000))
tcpSerSock.listen(1)
# Fill in end.

print('Proxy Server is ready to serve on port 8000...')

while 1:
    # Start receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = tcpCliSock.recv(4096).decode()  # Fill in start. # Fill in end.
    print(message)

    # Extract the filename from the given message
    print(message.split()[1])
    filename = message.split()[1].partition("/")[2] 
    print(filename)
    fileExist = "false"
    filetouse = "/" + filename
    print(filetouse)

    try:
        # Check whether the file exists in the cache
        f = open(filetouse[1:], "rb")
        outputdata = f.read()
        fileExist = "true"

        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send(b"HTTP/1.1 200 OK\r\n")
        tcpCliSock.send(b"Content-Type: text/html\r\n\r\n")

        # Fill in start.
        tcpCliSock.send(outputdata)
		# Fill in end.

        print('Read from cache')

    # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":
            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM) # Fill in start. # Fill in end.
            hostn = filename.replace("www.", "", 1).split("/")[0]
            print(hostn)

            try:
                # Connect to the socket to port 80
                # Fill in start.
                c.connect((hostn, 80))
                # Fill in end.

                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                fileobj = c.makefile('rwb', 0)
                fileobj.write(f"GET http://{filename} HTTP/1.0\n\n".encode())

                # Read the response into buffer
                # Fill in start.
                response_data = fileobj.read()
                # Fill in end.

                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to the client socket and the corresponding file in the cache
                os.makedirs(os.path.dirname("./" + filename), exist_ok=True)
                with open("./" + filename, "wb") as tmpFile:
                    tmpFile.write(response_data)

                # Fill in start.
                tcpCliSock.send(b"HTTP/1.1 200 OK\r\n")
                tcpCliSock.send(b"Content-Type: text/html\r\n\r\n")
                tcpCliSock.send(response_data)
                # Fill in end.

                print(f"File saved to cache: {filename}")

            except:
                print("Illegal request")
                
        else:
            # HTTP response message for file not found
            # Fill in start.
            print("File not found in cache, failed to fetch from the server.")
            tcpCliSock.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
            # Fill in end.

    # Close the client and the server sockets
    tcpCliSock.close()

# Fill in start.
tcpSerSock.close()
# Fill in end.