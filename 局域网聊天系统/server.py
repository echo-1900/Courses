#!/usr/bin/python
# coding: utf-8

import SocketServer
import socket
import threading
import json
from code import *


#在线用户用户名与对应套接字映射
ONLINEUSER = {}


#已注册用户字典
REGISTERED_USER = {}


#用户心跳字典,每个用户生命值默认为5，每10秒减一，收到置5，到0视为掉线
#USER_HEARTBEAT = {}


#读取及写入已注册用户列表
#文件为当前文件夹下的<registered_user>
def loadRegieteredUser():
	try:
		with open("registered_user","r") as f:
			line = f.readline()
			while line:
				data = line.strip().split('\t')
				REGISTERED_USER[data[0]] = data[1]
				line = f.readline()
	except:
		pass


#重写一，线程不终止，整合到用户退出函数
class MyThreadingMixIn(SocketServer.ThreadingMixIn):
    daemon_threads = False

    def process_request_thread(self, request, client_address):
        try:
            self.finish_request(request, client_address)
            #重写一，线程不终止，整合到用户退出函数
            #self.shutdown_request(request)                 
        except:
            self.handle_error(request, client_address)
            self.shutdown_request(request)

    def process_request(self, request, client_address):
        """为该请求（此处即为新用户）开启一个新线程"""
        t = threading.Thread(target = self.process_request_thread,
                             args = (request, client_address))
        t.daemon = self.daemon_threads
        t.start()
     

#重写二，套接字不关闭，整合到用户退出函数
class MyStreamRequestHandler(SocketServer.BaseRequestHandler):
    rbufsize = -1
    wbufsize = 0

    # A timeout to apply to the request socket, if not None.
    timeout = None

    disable_nagle_algorithm = False

    def setup(self):
        self.connection = self.request
        if self.timeout is not None:
            self.connection.settimeout(self.timeout)
        if self.disable_nagle_algorithm:
            self.connection.setsockopt(socket.IPPROTO_TCP,
                                       socket.TCP_NODELAY, True)
        self.rfile = self.connection.makefile('rb', self.rbufsize)
        self.wfile = self.connection.makefile('wb', self.wbufsize)

    def finish(self):
        if not self.wfile.closed:
            try:
                self.wfile.flush()
            except socket.error:
                # A final socket error may have occurred here, such as
                # the local error ECONNABORTED.
                pass
        #重写二，套接字不关闭，整合到用户退出函数
        #self.wfile.close()                  
        #self.rfile.close()



#重写三，重写请求处理
class MyTCPHandler(MyStreamRequestHandler):
	#处理注册请求
	def __handleRegister(self,data):
		response_register = {}
		#用户已存在
		if data["username"] in REGISTERED_USER:
			response_register['code'] = HAS_BEEN_REGISTERED
		#注册成功
		else:
			REGISTERED_USER[data["username"]] = data["password"]
			#写入已知用户
			with open("registered_user",'a') as f:
				f.write(data["username"]+"	"+data["password"]+'\n')
			response_register['code'] = REGISTER_OK
		#响应发包
		tosend = json.dumps(response_register).encode('utf-8')
		self.request.sendall(tosend)
		return 0

	#处理登陆请求
	def __handleLogin(self,data):
		response_login = {}
		#用户未注册
		if data["username"] not in REGISTERED_USER:
			response_login['code'] = UNREGISTERED_USER
		#用户已登录
		elif data["username"] in ONLINEUSER:
			response_login['code'] = HAS_BEEN_LOGINED
		#密码错误
		elif REGISTERED_USER[data["username"]] != data["password"]:
			response_login['code'] = PASSWORD_INCORRECT
		#登陆成功
		else:
			#在线用户存入用户名和套接字对象
			ONLINEUSER[data["username"]] = self.wfile
			#用户心跳字典中创建该用户的条目，默认生命值为5
			#USER_HEARTBEAT[data["username"]] = 5	
			response_login['code'] = LOGIN_OK
		#响应发包
		tosend = json.dumps(response_login).encode('utf-8')
		self.request.sendall(tosend)
		return 0

	#处理退出请求	
	def __handleLogout(self,data):
		response_logout = {}
		response_logout['code'] = LOGOUT_OK
		tosend = json.dumps(response_logout).encode('utf-8')
		self.request.sendall(tosend)
		try:
			del ONLINEUSER[data["username"]]
			#关闭文件描述符
			self.wfile.close()
			self.rfile.close()
			#此处[不能]断开连接
			#self.request.shutdown(socket.SHUT_WR)
			#修改在线用户列表
			return 0
		except:
			return 1

	#处理列出在线用户
	def __handleListOnline(self):
		response_listonline = {}
		try:
			response_listonline['online_users'] = ONLINEUSER.keys()
			response_listonline['code'] = LISTONLINE_OK
			tosend = json.dumps(response_listonline).encode('utf-8')
			self.request.sendall(tosend)
			return 0
		except:
			response_listonline['code'] = LISTONLINE_FAIL
			tosend = json.dumps(response_listonline).encode('utf-8')
			self.request.sendall(tosend)
			return 0

	#处理消息转发
	def __handleSendMessage(self,data):
		response_sendmessage= {}
		transmmit = {}
		#对方不在线,只发包给请求者
		if data["towho"] not in ONLINEUSER:
			response_sendmessage['code'] = MSG_NOT_ONLINE
			response_sendmessage['towho'] = data['towho']
			tosend = json.dumps(response_sendmessage).encode('utf-8')
			self.request.sendall(tosend)
		#对方在线，一个包发给请求者，一个包转发给接受者
		else:
			#先转发消息
			transmmit['code'] = MSG_COME
			transmmit['fromwho'] = data['fromwho']
			transmmit['message'] = data['data']
			transmmit['time']	 = data['time']
			to_transmmit = json.dumps(transmmit).encode('utf-8')
			ONLINEUSER[data["towho"]].write(to_transmmit)
			#再发给请求者，表明信息发送成功
			response_sendmessage['code'] = MSG_OK
			to_response = json.dumps(response_sendmessage).encode('utf-8')
			self.request.sendall(to_response)
		return 0


	#处理文件发送请求
	def __handleRequestSendFile(self,data):
		response_requestSendFile = {}
		transmmit_sendfile = {}
		
		if data["towho"] not in ONLINEUSER:
			#对方不在线,发包告知请求者
			response_requestSendFile['code'] = FILE_NOT_ONLINE
			response_requestSendFile['towho'] = data['towho']
			tosend = json.dumps(response_requestSendFile).encode('utf-8')
			self.request.sendall(tosend)
		else:
			#发包告知接收方
			transmmit_sendfile['code'] = FILE_ASK
			transmmit_sendfile['fromwho'] = data['fromwho']
			transmmit_sendfile['filename'] = data['filename']
			transmmit_sendfile['size']	   = data['size']
			to_transmmit = json.dumps(transmmit_sendfile).encode('utf-8')
			ONLINEUSER[data["towho"]].write(to_transmmit)
		return 0


	#处理客户端是否同意接收文件
	def __handleReceiveFile(self,data):
		#拒绝接收
		if data['pkg_type']  == REFUSE_FILE:
			transmmit_refusefile = {"code"	 	: FILE_REFUSE,
								    "fromwho"	: data["fromwho"],
								    "filename"	: data["filename"]
								   }
			to_transmmit = json.dumps(transmmit_refusefile).encode('utf-8')
			ONLINEUSER[data["towho"]].write(to_transmmit)
		#同意接收,pkg_type == ACCEPT_FILE
		else:
			transmmit_acceptfile = {"code"		: FILE_ALLOW,
									"fromwho"	: data["fromwho"],
									"filename"	: data["filename"],
									"addr"		: self.client_address[0], 
									"port"		: data["port"],
									"has_reacived": data["has_reacived"]
									}
			to_transmmit = json.dumps(transmmit_acceptfile).encode('utf-8')
			ONLINEUSER[data["towho"]].write(to_transmmit)
		return 0


	#def __handleHeartBeat(self,data):
		#pass


	#handle函数,统一调度各个函数
	def handle(self):
		while(1):
			self.data = json.loads(self.request.recv(8192).strip().decode('utf-8'))
			if self.data['pkg_type'] == REGISTER:
				self.__handleRegister(self.data)
			if self.data['pkg_type'] == LOGIN:
				self.__handleLogin(self.data)
			if self.data['pkg_type'] == LOGOUT:
				self.__handleLogout(self.data)
			if self.data['pkg_type'] == LISTONLINE:
				self.__handleListOnline()
			if self.data['pkg_type'] == MESSAGE:
				self.__handleSendMessage(self.data)
			if self.data['pkg_type'] == FILE:
				self.__handleRequestSendFile(self.data)
			if self.data['pkg_type'] == REFUSE_FILE or self.data['pkg_type'] == ACCEPT_FILE:
				self.__handleReceiveFile(self.data)
			#if self.data['pkg_type'] == HEARTBEAT:
				#self.__handleHeartBeat(self.data)




#多线程类，为每个连接创建一个线程
class ThreadedTCPServer(MyThreadingMixIn, SocketServer.TCPServer):
	pass


#主函数启动服务器：
def main():
	loadRegieteredUser()
	ThreadedTCPServer(('127.0.0.1',8888),MyTCPHandler).serve_forever()


if __name__ == "__main__":
	main()
