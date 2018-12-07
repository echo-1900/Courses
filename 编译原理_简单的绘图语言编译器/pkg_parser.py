from scanner import Scanner
from scanner import Token
import sys


#Node类定义
class Node(object):
    def __init__(self, data,value=None):
        self.data=data	   #节点类型
        self.value =value  #节点值
        self.left = None   #左孩子
        self.right = None  #右孩子
        self.child=None    #cos等数学函数专用
    def __str__(self):
        return self.value


#接收一个scanner类以实例化
class Parser(object):
    #方便没必要实例化的时候直接当函数调用
    @staticmethod
    def make_tree(token_type, arg1=None, arg2=None):
    	#token_type: 节点类型
    	#arg1	  ： 常数值或函数名
    	#arg2	  ：	 函数的参数表达式

    	#常数节点
        if token_type == 'CONST_ID':
            t = Node(token_type, arg1)
        #参数T节点
        elif token_type == 'T':
            t = Node('T')
        #函数节点
        elif token_type == 'FUNC':
            t = Node('FUNC', arg1)
            t.child = arg2
        #其他节点
        else:
            t = Node(token_type)
            t.left = arg1
            t.right = arg2
        return t

    @staticmethod
    def print_tree(root, indent):
        for x in range(indent):
            print('-', end='')
        if root.data == 'PLUS':
            print('+')
        elif root.data == 'MINUS':
            print('-')
        elif root.data == 'MUL':
            print('*')
        elif root.data == 'DIV':
            print('/')
        elif root.data == 'POWER':
            print('^')
        elif root.data == 'FUNC':
            print(root.value)
        elif root.data == 'CONST_ID':
            print(root.value)
        elif root.data == 'T':
            print('T')
        else:
            sys.exit('节点错误，无法构造树')
        if root.data == 'CONST_ID' or root.data == 'T':
            return
        if root.data == 'FUNC':
            Parser.print_tree(root.child, indent + 1)
        else:
            Parser.print_tree(root.left, indent + 1)
            Parser.print_tree(root.right, indent + 1)


    def __init__(self,scanner):
        self.it=scanner.get_Token()
        self.token=Token()
        #具体的一些数值
        self.x=None
        self.y=None
        self.x_scale=None
        self.y_scale=None
        self.rot=None
        self.start=None#T的起始
        self.end=None#T的终点
        self.step=None#步长
        self.x_origin=None
        self.y_origin=None

    def FetchToken(self):
        self.token=next(self.it)

    def MatchToken(self,token_type):
        if self.token.Token_type!=token_type:
            sys.exit('符号使用错误:{}'.format(self.token.data))
        self.FetchToken()

    def program(self):
        while True:
            try:
                self.statement()
                self.MatchToken('SEMICO')
            except StopIteration:
                break
            if self.token=='error_token':
                sys.exit('未知符号')
                break

    def statement(self):
        if self.token.Token_type=='ORIGIN':
            self.origin_statement()
        elif self.token.Token_type=='SCALE':
            self.scale_statement()
        elif self.token.Token_type=='ROT':
            self.rot_statement()
        elif self.token.Token_type=='FOR':
            self.for_statement()
        else:
            sys.exit('不能以{}的上一个符号开头 '.format(self.token.Token_type))

    def origin_statement(self):
        self.MatchToken('ORIGIN')
        self.MatchToken('IS')
        self.MatchToken('L_BRACKET')
        self.x_origin=self.expression()
        self.MatchToken('COMMA')
        self.y_origin=self.expression()
        self.MatchToken('R_BRACKET')


    def scale_statement(self):
        self.MatchToken('SCALE')
        self.MatchToken('IS')
        self.MatchToken('L_BRACKET')
        self.x_scale=self.expression()
        self.MatchToken('COMMA')
        self.y_scale=self.expression()
        self.MatchToken('R_BRACKET')

    def rot_statement(self):
        self.MatchToken('ROT')
        self.MatchToken('IS')
        self.rot=self.expression()

    def for_statement(self):
        self.MatchToken('FOR')
        self.MatchToken('T')
        self.MatchToken('FROM')
        self.start=self.expression()
        self.MatchToken('TO')
        self.end=self.expression()
        self.MatchToken('STEP')
        self.step=self.expression()
        self.MatchToken('DRAW')
        self.MatchToken('L_BRACKET')
        self.x=self.expression()
        self.MatchToken('COMMA')
        self.y=self.expression()
        self.MatchToken('R_BRACKET')

    def expression(self):
        left=self.term()
        while self.token.Token_type=='PLUS' or self.token.Token_type=='MINUS':
            token_tmp=self.token.Token_type
            self.MatchToken(token_tmp)
            right=self.term()
            left=Parser.make_tree(token_tmp,left,right)
        Parser.print_tree(left,1)
        return left

    def term(self):
        left=self.factor()
        while self.token.Token_type=='MUL' or self.token.Token_type=='DIV':
            token_tmp = self.token.Token_type
            self.MatchToken(token_tmp)
            right=self.factor()
            left=Parser.make_tree(token_tmp,left,right)
        return left

    def factor(self):
        if self.token.Token_type=='PLUS':
            self.MatchToken('PLUS')
            right=self.factor()
        elif self.token.Token_type=='MINUS':
            self.MatchToken('MINUS')
            right=self.factor()
            left=Node('CONST_ID')
            left.value=0.0
            right=Parser.make_tree('MINUS',left,right)
        else:
            right=self.component()
        return right

    def component(self):
        left=self.atom()
        if self.token.Token_type=='POWER':
            self.MatchToken('POWER')
            right=self.component()
            left=Parser.make_tree('POWER',left,right)
        return left

    def atom(self):
        tmp=self.token
        if self.token.Token_type=='CONST_ID':
            self.MatchToken('CONST_ID')
            t=Parser.make_tree('CONST_ID',tmp.value)
        elif self.token.Token_type=='T':
            self.MatchToken('T')
            t=Parser.make_tree('T')
        elif self.token.Token_type=='FUNC':
            func_name=self.token.data
            self.MatchToken('FUNC')
            self.MatchToken('L_BRACKET')
            s=self.expression()
            t=Parser.make_tree('FUNC',func_name,s)
            self.MatchToken('R_BRACKET')
        elif self.token.Token_type=='L_BRACKET':
            self.MatchToken('L_BRACKET')
            t=self.expression()
            self.MatchToken('R_BRACKET')
        else:
            sys.exit('算数表达式错误')
        return t
    def __str__(self):
        return '[start:%s end:%s step:%s rot:%s x_origin:%s y_origin:%s]'%(self.start,self.end,self.step,self.rot,self.x_origin,self.y_origin)



if __name__ == '__main__':
    file = sys.argv[1]
    scanner_test = Scanner(file)
    parser_test=Parser(scanner_test)
    parser_test.FetchToken()
    parser_test.program()
