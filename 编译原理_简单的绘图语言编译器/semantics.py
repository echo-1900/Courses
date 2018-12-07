import math,random,sys
import matplotlib.pyplot as plt
from pkg_parser import Parser
from pkg_parser import Scanner


#继承Parser类
class Semantics(Parser):
    #递归求值
    @staticmethod
    def get_expr_value(root, T=0.0):
        if root.data == 'PLUS':
            return Semantics.get_expr_value(root.left, T) + Semantics.get_expr_value(root.right, T)
        elif root.data == 'MINUS':
            return Semantics.get_expr_value(root.left, T) - Semantics.get_expr_value(root.right, T)
        elif root.data == 'MUL':
            return Semantics.get_expr_value(root.left, T) * Semantics.get_expr_value(root.right, T)
        elif root.data == 'DIV':
            return Semantics.get_expr_value(root.left, T) / Semantics.get_expr_value(root.right, T)
        elif root.data == 'POWER':
            return Semantics.get_expr_value(root.left, T) ** Semantics.get_expr_value(root.right, T)
        elif root.data == 'FUNC':
            if root.value == 'SIN':
                return math.sin(Semantics.get_expr_value(root.child, T))
            elif root.value == 'COS':
                return math.cos(Semantics.get_expr_value(root.child, T))
            else:
                print('Unknown function', root.value, end='')
                exit()
        elif root.data == 'CONST_ID':
            return root.value
        elif root.data == 'T':
            return T
        else:
            return 0.0


    ###重写Parser类中的各个语句，将值求出来
    def origin_statement(self):
        self.MatchToken('ORIGIN')
        self.MatchToken('IS')
        self.MatchToken('L_BRACKET')
        tmp = self.expression()
        self.x_origin = Semantics.get_expr_value(tmp)
        self.MatchToken('COMMA')
        tmp= self.expression()
        self.y_origin = Semantics.get_expr_value(tmp)
        self.MatchToken('R_BRACKET')

    def scale_statement(self):
        self.MatchToken('SCALE')
        self.MatchToken('IS')
        self.MatchToken('L_BRACKET')
        tmp=self.expression()
        self.x_scale=Semantics.get_expr_value(tmp)
        self.MatchToken('COMMA')
        tmp=self.expression()
        self.y_scale=Semantics.get_expr_value(tmp)
        self.MatchToken('R_BRACKET')

    def rot_statement(self):
        self.MatchToken('ROT')
        self.MatchToken('IS')
        tmp=self.expression()
        self.rot=Semantics.get_expr_value(tmp)

    #计算坐标并画点
    def for_statement(self):
        self.MatchToken('FOR')
        self.MatchToken('T')
        self.MatchToken('FROM')
        tmp=self.expression()
        self.start=Semantics.get_expr_value(tmp)
        self.MatchToken('TO')
        tmp=self.expression()
        self.end=Semantics.get_expr_value(tmp)
        self.MatchToken('STEP')
        tmp=self.expression()
        self.step=Semantics.get_expr_value(tmp)
        self.MatchToken('DRAW')
        self.MatchToken('L_BRACKET')
        self.x=self.expression()
        self.MatchToken('COMMA')
        self.y=self.expression()
        self.MatchToken('R_BRACKET')
        self.draw()


    #画点，一次一个
    #只有for语句能画，所以只在for语句中被调用
    def draw(self):
        T = self.start
        while T <= self.end:
            #求表达式的值
            x = Semantics.get_expr_value(self.x, T)
            y = Semantics.get_expr_value(self.y, T)
            #旋转
            x_tmp = x * math.cos(self.rot) + y * math.sin(self.rot)
            y = y * math.cos(self.rot) - x * math.sin(self.rot)
            x = x_tmp
            #缩放
            x *= self.x_scale
            y *= self.y_scale
            #相对原点坐标
            x += self.x_origin
            y += self.y_origin
            #画点
            plt.scatter(x, y)
            T += self.step

    def show(self):
        plt.figure(figsize=(10, 10))
        plt.title('My Compiler')
        self.FetchToken()
        self.program()
        plt.show()


if __name__ == '__main__':
    file = sys.argv[1]
    scanner_test = Scanner(file)
    semantics_test=Semantics(scanner_test)
    semantics_test.show()	