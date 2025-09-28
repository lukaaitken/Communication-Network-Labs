from socket import *
import datetime
msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = 'mail-relay.tru.ca'
serverport = 25

# Create socket called clientSocket and establish a TCP connection with mailserver
#Fill in start
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, serverport))
#Fill in end

recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
	print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
	print('250 reply not received from server.')


# Send MAIL FROM command and print server response.
# Fill in start
mailFrom = "MAIL FROM:<aitkenl19@mytru.ca>\r\n"
clientSocket.send(mailFrom.encode())
recv2 = clientSocket.recv(1024).decode()
print(recv2)
if recv2[:3] != '250':
    print('250 reply not received from server.')
# Fill in end

# Send RCPT TO command and print server response.
# Fill in start
rcptTo = "RCPT TO:<aitkenl19@mytru.ca>\r\n"
clientSocket.send(rcptTo.encode())
recv3 = clientSocket.recv(1024).decode()
print(recv3)
if recv3[:3] != '250':
    print('250 reply not received from server.')
# Fill in end

# Send DATA command and print server response.
# Fill in start
dataCommand = "DATA\r\n"
clientSocket.send(dataCommand.encode())
recv4 = clientSocket.recv(1024).decode()
print(recv4)
if recv4[:3] != '354':
    print('354 reply not received from server.')
# Fill in end

# Send message data.
# Fill in start
message = f"From: \"Luka1\" <aitkenl19@mytru.ca>\r\n" \
          f"To: \"Luka2\" <aitkenl19@mytru.ca>\r\n" \
          f"Cc: \r\n" \
		  f"Date: Tue, 15 Jan 2008 16:02:43 -0500\r\n" \
          f"Subject: Python email\r\n" \
          f"\r\n" \
          f"Hello Luka2, its Luka1 sending you an email.\r\n" \
		  "\r\n.\r\n"
clientSocket.send(message.encode())
# Fill in end

# Message ends with a single period.
# Fill in start
recv5 = clientSocket.recv(1024).decode()
print(recv5)
if recv5[:3] != '250':
    print('250 reply not received from server.')
# Fill in end

# Send QUIT command and get server response.
# Fill in start
quitCommand = "QUIT\r\n"
clientSocket.send(quitCommand.encode())
recv6 = clientSocket.recv(1024).decode()
print(recv6)
if recv6[:3] != '221':
    print('221 reply not received from server.')
# Fill in end