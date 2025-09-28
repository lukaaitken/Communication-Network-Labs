
import socket
import os
import sys
import struct
import time
import select

ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY = 0

def checksum(packet_bytes):
	csum = 0
	countTo = (len(packet_bytes) // 2) * 2
	count = 0
	while count < countTo:
		thisVal = packet_bytes[count+1] * 256 + packet_bytes[count]
		csum = csum + thisVal
		csum = csum & 0xffffffff
		count = count + 2

	if countTo < len(packet_bytes):
		csum = csum + packet_bytes[len(packet_bytes) - 1]
		csum = csum & 0xffffffff

	csum = (csum >> 16) + (csum & 0xffff)
	csum = csum + (csum >> 16)
	answer = ~csum
	answer = answer & 0xffff
	answer = answer >> 8 | (answer << 8 & 0xff00)

	return answer


def receiveOnePing(mySocket, ID, timeout, destAddr):

	whatReady = select.select([mySocket], [], [], timeout)
	if whatReady[0] == []: # Timeout
		return "Request timed out."


	timeReceived = time.time()
	recPacket, addr = mySocket.recvfrom(1024)

	#Fill in start

	#Fetch the ICMP header from the IP packet
	ICMP_Header = recPacket[20:28]
	type, code, checksum, packetID, sequence = struct.unpack("bbHHh", ICMP_Header)
	#Verify Correct ICMP Header fields
	if type == ICMP_ECHO_REPLY and packetID == ID:
		sentTime = struct.unpack("d", recPacket[28:36])[0]
		rtt = (timeReceived - sentTime) * 1000
		return f"Reply from {destAddr}: time={rtt:.2f}ms"
	#Calculate time difference
	return "Invalid response received."
	#Fill in end


def sendOnePing(mySocket, destAddr, ID):
	# Header is type (8), code (8), checksum (16), id (16), sequence (16)

	# Make a dummy header with a 0 checksum
	# struct interpret strings as packed binary data
	header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, 0, ID, 1)
	data = struct.pack("d", time.time())
	packet = header + data

	# Calculate the checksum on the data and the dummy header.
	myChecksum = checksum(packet)

	# Get the right checksum, and put in the header
	if sys.platform == 'darwin':
	# Convert 16bit integers from host to network byte order
		myChecksum = socket.htons(myChecksum) & 0xffff
	else:
		myChecksum = socket.htons(myChecksum)

	header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
	packet = header + data
	mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str

	# Both LISTS and TUPLES consist of a number of objects
	# which can be referenced by their position number within the object.


def doOnePing(destAddr, timeout):
	icmp = socket.getprotobyname("icmp")

	# SOCK_RAW is a powerful socket type. For more details: https://sock-raw.org/papers/sock_raw
	mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
	myID = os.getpid() & 0xFFFF # Return the current process id
	sendOnePing(mySocket, destAddr, myID)
	delay = receiveOnePing(mySocket, myID, timeout, destAddr)
	mySocket.close()

	return delay


def ping(host, timeout=1, count=4):
	# timeout=1 means: If one second goes by without a reply from the server,
	# the client assumes that either the client's ping or the server's pong is lost

	dest = socket.gethostbyname(host)
	print(f"Pinging {dest} using Python:")
	print("")

	rtt_list = []
	packet_sent = 0
	packet_received = 0

	while packet_sent < count:
		packet_sent += 1
		delay = doOnePing(dest, timeout)
		if "Request timed out." not in delay:
			packet_received += 1
			rtt = float(delay.split('=')[1].split('ms')[0].strip())
			rtt_list.append(rtt)
		print(delay)
		time.sleep(1)

	if packet_sent > 0:
		packet_loss = (packet_sent - packet_received) / packet_sent * 100
		min_rtt = min(rtt_list) if rtt_list else None
		max_rtt = max(rtt_list) if rtt_list else None
		avg_rtt = sum(rtt_list) / len(rtt_list) if rtt_list else None

		print("\nPing statistics:")
		print(f"Packets sent = {packet_sent}, Packets received = {packet_received}, Packet loss = {packet_loss:.2f}%")
		print(f"Minimum RTT = {min_rtt}ms, Maximum RTT = {max_rtt}ms, Average RTT = {avg_rtt:.2f}ms")

ping("google.ca")