import socket

server = socket.socket()
'''
#linux
keepalive = 1
keepidle = 3
keepinterval = 3
keepcount   = 3
server.setsockopt(socket.SOL_SOCKET,socket.SO_KEEPALIVE,keepalive)
server.setsockopt(socket.SOL_TCP,socket.TCP_KEEPIDLE,keepidle)
server.setsockopt(socket.SOL_TCP,socket.TCP_KEEPINTVL,keepcount)
server.setsockopt(socket.SOL_TCP,socket.TCP_KEEPCNT,keepcount)
'''

#windows
#有问题
#This will enable socket keep alive, with a 10 second keep alive time and a 3 second keep alive interval.
server.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 10000, 3000))


server.bind(("127.0.0.1",9999))
server.listen(1)
client,address = server.accept()
while(1):
	data = client.recv(1024)
	print data