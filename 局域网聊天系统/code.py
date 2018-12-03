# coding: utf-8

#请求包包类型定义
REGISTER = 1
LOGIN    = 2
LOGOUT 	 = 3
MESSAGE  = 4
LISTONLINE 	= 5
FILE  	 	= 6
REFUSE_FILE = 7
ACCEPT_FILE = 8




#响应包类型定义
#register
HAS_BEEN_REGISTERED = 101
REGISTER_OK	  		= 100
#login
UNREGISTERED_USER   = 201
HAS_BEEN_LOGINED	= 202
PASSWORD_INCORRECT  = 203
LOGIN_OK			= 200
#listonline
LISTONLINE_OK		= 300
LISTONLINE_FAIL		= 301 	#服务器错误，弃用，归于else
#sendmsg
MSG_NOT_ONLINE		= 401
MSG_OK				= 400
#logout
LOGOUT_OK			= 500
#file
FILE_NOT_ONLINE		= 601
FILE_ASK			= 602
FILE_REFUSE			= 603
FILE_ALLOW			= 604
#receiveMsg
MSG_COME			= 999