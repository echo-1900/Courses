#Token类定义
class Token(object):
    def __init__(self,Token_type="",data="",value=0):
        self.Token_type=Token_type  #类型
        self.data=data              #输入的符号
        self.value=value            #符号的值
    def __str__(self):
        return '[Token_type:%s  data:%s  value:%d]' % (self.Token_type,self.data,self.value)


token=['PI','T','SIN','COS','ORIGIN','SCALE','ROT','IS','FOR','FROM','TO','STEP','DRAW']


token1=[Token('CONST_ID','PI',3.1415926),
        Token('T','T',0.0),
        Token('FUNC','SIN',0.0),
        Token('FUNC','COS',0.0),
        Token('ORIGIN','ORIGIN',0.0),
        Token('SCALE','SCALE',0.0),
        Token('ROT','ROT',0.0),
        Token('IS','IS',0.0),
        Token('FOR','FOR',0.0),
        Token('FROM','FROM',0.0),
        Token('TO','TO',0.0),
        Token('STEP','STEP',0.0),
        Token('DRAW','DRAW',0.0)]


class Scanner(object):
    def __init__(self,filename):
        f=open(filename,'r')
        self.lines=f.read().upper()+'@'
        f.close()

    def show_input(self):
        return self.lines

    def get_Token(self):
        L = iter(self.lines)
        char = L.__next__()
        temp = []  
        while char is not '@':
            #处理空格等无效字符
            while char==' ' or char=='\n' or char=='\t'or char =='\r':
                char = L.__next__()
                if char=='@':
                    print("词法分析成功完成。")

            #处理语言中的操作符
            if char.isalpha():
                while True:
                    if char.isalnum():
                        temp.append(char)
                        char = L.__next__()
                    else:
                        break
                item = ''.join(temp)
                if item in token:
                    for x in token1:
                        if x.data == item:
                            yield x
                temp = []

            #处理数字
            elif char.isdigit():
                while True:
                    if char.isdigit():
                        temp.append(char)
                        char = L.__next__()
                    else:
                        break
                #小数
                if char is '.':
                    temp.append(char)
                    char = L.__next__()
                    while True:
                        if char.isdigit():
                            temp.append(char)
                            char = L.__next__()
                        else:
                            break
                item = ''.join(temp)
                x = Token('CONST_ID', item, float(item))
                yield x
                temp = []

            #各种唯一的符号
            elif char == ';':
                x = Token('SEMICO', char)
                yield x
                char = L.__next__()
            elif char == '(':
                x = Token('L_BRACKET', char)
                yield x
                char = L.__next__()
            elif char == ')':
                x = Token('R_BRACKET', char)
                yield x
                char = L.__next__()
            elif char == '+':
                x = Token('PLUS', char)
                yield x
                char = L.__next__()
            elif char == '-':
                x = Token('MINUS', char)
                yield x
                char = L.__next__()
            elif char == ',':
                x = Token('COMMA', char)
                yield x
                char = L.__next__()
            elif char=='^':
                x = Token('POWER', char)
                char = L.__next__()
                yield x

            #算数除或者注释
            elif char is '/':
                char = L.__next__()
                if char == '/':
                    while char != '\n' and char != '@':
                        char = L.__next__()
                else:
                    x = Token('DIV', data='/')
                    yield x

            #算数乘或者乘方
            elif char == '*':
                x = Token('MUL', char)
                char=L.__next__()
                yield x
            
            #@跳过
            elif char == '@':
                continue
            
            #出错处理
            else:
                yield 'error_token'


if __name__=='__main__':
    import sys
    file = sys.argv[1]
    s=Scanner(file)
    for x in s.get_Token():
       print(x)
