#!/usr/bin/python
# coding: utf-8

import socket
import re
import json
import threading
import time
import random
import os
from code import *


class Client(object):
	'''
	所有功能函数成功返回0，错误返回1
	'''
	def __init__(self,address,port):
		self.address  = address
		self.port	  = port
		self.s 		  = socket.socket()
		self.loginflag  = 0
		self.isonline 	= 0


	def connectServer(self):
		try:
			self.s.connect((self.address,self.port))
		except:
			raise Exception("[!]Fail to connect to the server.")


	def closeSocket(self):
		try:
			self.s.close()
		except Exception as e:
			raise e


	def register(self):
		username = raw_input("[-]Please input your username:")
		#用户名检验
		if not re.findall(r"^[_a-zA-Z]\w{0,15}",username):
			print "[!]The username should start with a character and shorter than 16.\n"
			return 1
		#密码检验
		password1 = raw_input("[-]Please input your password:")
		password2 = raw_input("[-]Please confirm your password:")
		if not (password1 == password2 and password1):
			print "[!]Password illegel."
			return 1
		#封包并序列化
		register_pkg = {"pkg_type":REGISTER,
					  "username":username,
					  "password":password1}
		tosned = json.dumps(register_pkg).encode('utf-8')
		#发包
		try:
			self.s.send(tosned)
			return 0
		except:
			print "[!]Fail to send register package.\n"
			return 1


	def login(self):
		#输入用户信息,其中username上升为属性值
		self.username = raw_input("[-]Please input your username:")
		password = raw_input("[-]Please input your password:")
		#封包并序列化
		login_pkg = {"pkg_type":LOGIN,
					 "username":self.username,
					 "password":password}
		tosned = json.dumps(login_pkg).encode('utf-8')
		#发包
		try:
			self.s.send(tosned)
			return 0
		except:
			print "[!]Fail to send register package.\n"
			return 1


	def logout(self):
		logout_pkg = {"pkg_type":LOGOUT,
					 "username":self.username}
		tosned = json.dumps(logout_pkg).encode('utf-8')		
		#发包
		try:
			self.s.send(tosned)
			self.isonline = 0
		except:
			print "[!]Fail to send logout package.\n"
			return 1
		#后续处理
		#此处不能断开连接，需要返回主界面，以便用其他账号登录
		print "[*]Bye~." 
		return 0


	def listOnline(self):
		listOnline_pkg = {"pkg_type":LISTONLINE}
		tosned = json.dumps(listOnline_pkg).encode('utf-8')
		#发包
		try:
			self.s.send(tosned)
		except:
			print "[!]Fail to send register package.\n"
			return 1


	def sendMessage(self,towho,data):
		sendMessage_pkg = {"pkg_type":MESSAGE,
						  "fromwho"	:self.username,
						  "towho"	:towho,
						  "data"	:data,
						  "time"	:time.strftime("%H:%M:%S",time.localtime())
						  }
		tosned = json.dumps(sendMessage_pkg).encode('utf-8')
		#发包
		try:
			self.s.send(tosned)
			return 0
		except:
			print "[!]Fail to send message.\n"
			return 1


	#主动发送心跳包，防止意外掉线后服务端误认为还在线
	'''
	def sendHeartBeat(self):
		heartBeat_pkg = {"pkg_type":HEARTBEAT，
						 "username" :self.username}
		tosned = json.dumps(heartBeat_pkg).encode('utf-8')
		#发包
		try:
			self.s.send(tosned)
			return 0
		except:
			print "[!]Fail to send heart beat package.\n"
			return 1
	'''


	#供handleInput调用
	#请求传输文件，发给服务器以转发
	def requestSendFile(self,towho,filename,size):
		sendFile_pkg = {"pkg_type":FILE,
						"fromwho" :self.username,
						"towho"	  :towho,
						"filename":filename,
						"size"	  :size
						}
		tosned = json.dumps(sendFile_pkg).encode('utf-8')
		#发包
		try:
			self.s.send(tosned)
			return 0
		except:
			print "[!]Fail to send file request.\n"
			return 1


	#供handleRecv调用
	#与对方连接
	def reaciveFile(self,fromwho,filename,size):
		print fromwho + " wants to send you the file " + filename + "(" + str(size) + "B)\nPress <Enter> to continue."
		while(1):
			choice = raw_input("Would you like to receive?\n[1]Yes\n[2]No\n")
			if choice == "1" or choice == "2":
				break
			else:
				print "Please input a correct choice."
		#拒绝接收
		if choice == "2":
			refuseFile_pkg = {"pkg_type": REFUSE_FILE,
							  "fromwho" : self.username,
							  "towho"   : fromwho,
							  "filename": filename
							  }
			tosned = json.dumps(refuseFile_pkg).encode('utf-8')
			#发包
			try:
				self.s.send(tosned)
				return 0
			except Exception as e:
				raise e
		#同意接收,创建一个socket监听以接收
		if choice == "1":
			file_sock = socket.socket()
			port	  = random.randint(4096,40960)
			file_sock.bind(('127.0.0.1',port))
			file_sock.listen(1)
			#准备一个文件名
			localfilename = "from" + "_" + fromwho + "_" + filename
			#断点续传，如果之前接收过，将文件大小读取并写入包中，默认为0
			try:
				has_reacived = os.path.getsize(localfilename)
			except:
				has_reacived = 0
			#构建同意接收包
			acceptFile_pkg = {"pkg_type": ACCEPT_FILE,
							  "fromwho" : self.username,
							  "towho"   : fromwho,
							  "port"	: port,
							  "filename": filename,
							  "has_reacived": has_reacived
				       		 }
			tosned = json.dumps(acceptFile_pkg).encode('utf-8')
			#发包
			try:
				self.s.send(tosned)
			except Exception as e:
				raise e
			#开始监听并创建文件接收
			file_from,addr = file_sock.accept()
			with open(localfilename,"ab") as f:
				data = file_from.recv(1024)
				f.write(data)
				while(len(data) != 0):
					data = file_from.recv(1024)
					f.write(data)
			print "[*]File has been successfully received.\n"
			file_sock.close()
			return 0


	#供handleRecv调用
	#开始传输文件
	def beginSendFile(self,addr,port,filename,has_reacived):
		tmp_sock = socket.socket()
		try:
			tmp_sock.connect((addr,int(port)))
		except:
			print "[!]Oooops, it seems that (s)he is offline."
		with open(filename,"rb") as f:
			f.seek(has_reacived) #用于断点续传
			data = f.read(1024)
			while(len(data)!=0):
				tmp_sock.send(data)
				data = f.read(1024)
		print "[*]File has been successfully sended.\n"
		tmp_sock.close()
		return 0



	#接受所有的消息并分类处理
	#防止当前接受的响应不是对所需请求的响应
	def handleRecv(self):
		while True:
			recv_pkg = json.loads(self.s.recv(8192).strip().decode('utf-8'))
			code	 = recv_pkg['code']
			#按照响应标识符来输出信息
			if code == HAS_BEEN_REGISTERED:
				print "[!]Sorry, This username has been regietered.\n"
				#return 101 
			elif code == REGISTER_OK:
				print "[*]Congratuations!You can chat now.\n"
				#return 100 
			elif code == UNREGISTERED_USER:
				self.loginflag == UNREGISTERED_USER #设置登录状态标识符
				print "[!]Sorry, This username has not been regietered.\n"
				#return 201
			elif code == HAS_BEEN_LOGINED:
				self.loginflag == HAS_BEEN_LOGINED #设置登录状态标识符
				print "[!]Sorry, This username has been log in.\n"
				#return 202
			elif code == PASSWORD_INCORRECT:
				self.loginflag == PASSWORD_INCORRECT #设置登录状态标识符
				print "[!]Password discorrect.\n"
				#return 203 
			elif code == LOGIN_OK:
				self.loginflag = LOGIN_OK  #设置登录状态标识符
				self.isonline  = 1
				print "[*]You are online now.\n" 
				#return 200
			elif code == LISTONLINE_OK:
				print "[*]Online users: " + str(recv_pkg["online_users"]) + "\n"
				#return 300
			elif code == MSG_NOT_ONLINE:
				print "[!]Fail to send message:" + recv_pkg["towho"] + " is not online."
				#return 401
			elif code == MSG_OK:
				pass
				#return 400 #备用，发送成功
			elif code == LOGOUT_OK:
				self.isonline = 0	#用户退出，在线标志设为0，供给发送线程使用
				break       		#用户退出，线程终止，停止接收
			elif code == FILE_NOT_ONLINE:
				print "[!]Fail to send file:" + recv_pkg["towho"] + " is not online."
				#return 601	
			elif code == FILE_ASK:
				#self.reaciveFile(recv_pkg["fromwho"],recv_pkg["filename"],recv_pkg["size"])
				#开新线程
				tmp_thread = threading.Thread(target=self.reaciveFile,args=(recv_pkg["fromwho"],recv_pkg["filename"],recv_pkg["size"]))
				tmp_thread.start()
				#return 602
			elif code == FILE_REFUSE:
				print "[*]" + recv_pkg["fromwho"] + " refuse to accept your file <" + recv_pkg["filename"] + ">."
				#return 603
			elif code == FILE_ALLOW:
				print "[*]" + recv_pkg["fromwho"] + " allows to accept your file <" + recv_pkg["filename"] + ">."
				print "Now begin to transmit..."
				#self.beginSendFile(recv_pkg["addr"],recv_pkg["port"],recv_pkg["filename"])
				#开新线程
				tmp_thread = threading.Thread(target=self.beginSendFile,args=(recv_pkg["addr"],recv_pkg["port"],recv_pkg["filename"],recv_pkg["has_reacived"]))
				tmp_thread.start()
				#return 604
			elif code == MSG_COME:
				print "[>]From " + recv_pkg['fromwho'] + ": " + recv_pkg['message'] + "   [" + recv_pkg['time'] +']\n'
				#return 999 
			else:
				print "[!!!]SERVER ERROR.\n"
				#return -1 #需要返回主页面


	#查看帮助、登出、列出在线用户、发消息、发文件面板
	#单开一个线程等待输入
	def handleInput(self):
		help()
		while(1):
			if not self.isonline: #用于终止线程
				break  
			command = raw_input()
			if command == "help":
				help()
			elif command == "logout":
				self.logout()
			elif command == "listonline":
				self.listOnline()
			elif command[0:6] == "msg to":
				searchObj = re.search(r"msg to (.*?) (.*)", command, re.I)
				self.sendMessage(searchObj.group(1),searchObj.group(2))
			elif command[0:7] == "file to":
				searchObj = re.search(r"file to (.*?) (.*)", command, re.I)
				try:
					filesize  = os.path.getsize(os.getcwd()+os.sep+searchObj.group(2))
					self.requestSendFile(searchObj.group(1),searchObj.group(2),filesize)
					print "[*]Wait for " + searchObj.group(1) + "'s response.\n" 
				except Exception as e:
					print "[!]Please input the correct filename.\n"
			else:
				print "[!]Incorrect command.\n"


#登录或注册界面
def loginOrRegister(client):
	#选择登录或注册,只有登录成功才会跳出循环
	while(1):
		choose = raw_input("[-]Please type in your choice:\n[1]Login 		[2]Register\n")
		if choose == "1":
			client.login()
			time.sleep(1) #等待接受回复,尽可能避免消息到达延时带来的逻辑错误，但是还是有问题
			if client.loginflag == LOGIN_OK:
				break
			else:
				continue
		elif choose == "2":
			client.register()
			time.sleep(1) #等待接受回复,尽可能避免排版错乱
		else:
			print "Please input the correct choice.\n"
			time.sleep(1) #等待接受回复,尽可能避免排版错乱




def help():
	print "Commands:"
	print "[-]help: Show this commands manual."
	print "[-]logout: Logout."
	print "[-]listonline: Show all online users."
	print "[-]msg to <someone> <data>: <someone> should be inplaced by an online user and <data> is the data you want to send."
	print "[-]file to <someone> <filename>: <someone> should be inplaced by an online user and <filename> is the name of the file that you want to send."
	print "\n"



def main():
	print "[^_^]" + "Welcome~" 
	#连接服务器
	client = Client('127.0.0.1',8888)
	client.connectServer()
	#开始监听服务器信息，单独一个线程
	thread_recv = threading.Thread(target=client.handleRecv,args=())
	thread_recv.start()
	#程序入口，登录或注册，成功登录后才继续
	loginOrRegister(client)
	#已经成功登录，开始监听用户的任意输入
	thread_send = threading.Thread(target=client.handleInput,args=())
	thread_send.start()





if __name__ == "__main__":
	main()

