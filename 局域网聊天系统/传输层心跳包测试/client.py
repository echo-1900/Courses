import socket

client = socket.socket()
client.connect(("127.0.0.1",9999))
while(1):
	i = raw_input("....input sth")
	client.send(i)