Lab3 - UDP Pinger
===
In this lab, you will learn the basics of socket programming for UDP in Python. You will learn how to
send and receive datagram packets using UDP sockets and also, how to set a proper socket timeout.
Throughout the lab, you will gain familiarity with a Ping application and its usefulness in computing
statistics such as packet loss rate.

You will first study a simple Internet ping server written in the Python, and implement a
corresponding client. The functionality provided by these programs is similar to the functionality
provided by standard ping programs available in modern operating systems. However, these programs
use a simpler protocol, UDP, rather than the standard Internet Control Message Protocol (ICMP) to
communicate with each other. The ping protocol allows a client machine to send a packet of data to a
remote machine, and have the remote machine return the data back to the client unchanged (an action
referred to as echoing). Among other uses, the ping protocol allows hosts to determine round-trip
times to other machines.
You are given the complete code for the Ping server. Your task is to write the Ping client.
