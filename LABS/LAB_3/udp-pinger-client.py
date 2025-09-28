#!/usr/bin/python3

from socket import *
import time

serverName = '127.0.0.1'
#serverName = 'gitlab.eng.tru.ca'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

message = input('Hello')

clientSocket.sendto(message.encode(), (serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

print(modifiedMessage.decode())
pings = 0
clientSocket.settimeout(1)

while pings < 10:  
    try:
        send_time = time.time()
        clientSocket.sendto('pings'.encode(), (serverName, serverPort))
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        receive_time = time.time()
        rtt = receive_time - send_time
        finalrtt = rtt * 1000
        print(f'Round-trip time (RTT) for ping {pings + 1}: {finalrtt:.4f} ms')

    except:
        print('REQUEST TIMED OUT')

    pings += 1

clientSocket.close()