from sly import Parser
from sly import Lexer
import sys


class MyLexer(Lexer):
    tokens = {NAME, NUMBER, STRING, IF, ELSE, ELSEIF, FOR, EQEQ, TO, FUNCTION, TAKES, START, END,
              ASSIGN,LT, GT, LTE, GTE, MOD, PRINT}
    ignore = "\t "

    literals = {"(", ")", "+", "=", "+", "/", "*", "-" }

    IF = r'check if'
    ELSEIF = r'or if'
    ELSE = r'else'
    FOR = r'for'
    PRINT = r'display'
    EQEQ = r'equals'
    LTE = r'<='
    GTE = r'>='
    LT = r'<'
    GT = r'>'
    MOD = r'%'
    ASSIGN = r'assign'
    TO = r'to'
    START = r'start'
    END = r'end'
    FUNCTION = r'function'
    TAKES = r'takes'
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING = r'\".*?\"'
    # NEXT = r'\n'

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'\n+')
    def newline(self, t):
        self.lineno = t.value.count('n')

    @_(r'\*{2}.*')
    def COMMENT(self, t):
        pass

    def error(self, t):
        print("Illegal Character '%s'" % t.value[0])
        self.index += 1


class MyParser(Parser):
    tokens = MyLexer.tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
    )

    def __init__(self):
        self.env = {}

    @_('')
    def statement(self, p):
        pass

    @_('FOR var_assign TO expr START statement END')
    def statement(self, p):
        return 'for_loop', ('for_loop_setup', p.var_assign, p.expr), p.statement

    @_('IF condition START statement END ELSEIF condition START statement END')
    def statement(self, p):
        return 'if_elseif', p.condition0, ('elseif', p.statement0, p.statement1), p.condition1

    @_('IF condition START statement END ELSE START statement END')
    def statement(self, p):
        return 'if_else', p.condition, ('else', p.statement0, p.statement1)

    @_('IF condition START statement END')
    def statement(self, p):
        return 'if_stmt', p.condition, p.statement

    @_('FUNCTION NAME TAKES "(" ")" START statement END')
    def statement(self, p):
        return 'func_defi', p.NAME, p.statement

    @_('PRINT statement')
    def statement(self, p):
        return 'print', p.statement

    @_('NAME "(" ")"')
    def statement(self, p):
        return 'func_call', p.NAME

    @_('var_assign')
    def statement(self, p):
        return p.var_assign

    @_('ASSIGN NAME "=" expr')
    def var_assign(self, p):
        return 'var_assign', p.NAME, p.expr

    @_('ASSIGN NAME "=" STRING')
    def var_assign(self, p):
        return 'var_assign', p.NAME, p.STRING

    @_('expr')
    def statement(self, p):
        return p.expr

    @_('expr EQEQ expr')
    def condition(self, p):
        return 'eqeq', p.expr0, p.expr1

    @_('expr EQEQ expr')
    def expr(self, p):
        return 'eqeq', p.expr0, p.expr1

    @_('expr LTE expr')
    def condition(self, p):
        return 'less_than_equal', p.expr0, p.expr1

    @_('expr LTE expr')
    def expr(self, p):
        return 'less_than_equal', p.expr0, p.expr1

    @_('expr GTE expr')
    def condition(self, p):
        return 'greater_than_equal', p.expr0, p.expr1

    @_('expr GTE expr')
    def expr(self, p):
        return 'greater_than_equal', p.expr0, p.expr1

    @_('expr LT expr')
    def condition(self, p):
        return 'less_than', p.expr0, p.expr1

    @_('expr LT expr')
    def expr(self, p):
        return 'less_than', p.expr0, p.expr1

    @_('expr GT expr')
    def condition(self, p):
        return 'greater_than', p.expr0, p.expr1

    @_('expr GT expr')
    def expr(self, p):
        return 'greater_than', p.expr0, p.expr1

    @_('expr MOD expr')
    def expr(self, p):
        return 'modulo', p.expr0, p.expr1

    @_('expr "+" expr')
    def expr(self, p):
        return 'add', p.expr0, p.expr1

    @_('expr "-" expr')
    def expr(self, p):
        return 'sub', p.expr0, p.expr1

    @_('expr "*" expr')
    def expr(self, p):
        return 'mul', p.expr0, p.expr1

    @_('expr "/" expr')
    def expr(self, p):
        return 'div', p.expr0, p.expr1

    @_('"=" expr %prec UMINUS')
    def expr(self, p):
        return p.expr

    @_('NAME')
    def expr(self, p):
        return 'var', p.NAME

    @_('NUMBER')
    def expr(self, p):
        return 'num', p.NUMBER


class MyExecute:

    def __init__(self, tree, env):

        self.env = env
        result = self.walkTree(tree)
        if result is not None and isinstance(result, int):
            print(result)
        if isinstance(result, str) and result[0] == '"':
            print(result)

    def walkTree(self, node):

        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return node

        if node is None:
            return None

        if node[0] == 'program':
            if node[1] is None:
                self.walkTree(node[2])
            else:
                self.walkTree(node[1])
                self.walkTree(node[2])

        if node[0] == 'num':
            return node[1]

        if node[0] == 'str':
            return node[1]

        if node[0] == 'print':
            out = self.walkTree(node[1])
            print(out)

        if node[0] == 'if_elseif':
            result1 = self.walkTree(node[1])
            result2 = self.walkTree(node[2][2])
            if result1:
                return self.walkTree(node[2][1])
            elif result2:
                return self.walkTree(node[3])

        if node[0] == 'if_else':
            result = self.walkTree(node[1])
            if result:
                return self.walkTree(node[2][1])
            return self.walkTree(node[2][2])

        if node[0] == 'if_stmt':
            result = self.walkTree(node[1])
            if result:
                return self.walkTree(node[2])

        if node[0] == 'eqeq':
            # print(node[0], node[1], node[2])
            return self.walkTree(node[1]) == self.walkTree(node[2])

        if node[0] == 'func_defi':
            self.env[node[1]] = node[2]

        if node[0] == 'func_call':
            try:
                return self.walkTree(self.env[node[1]])
            except LookupError:
                print("Undefined function '%s'" % node[1])
                return 0

        if node[0] == 'modulo':
            return self.walkTree(node[1]) % self.walkTree(node[2])

        if node[0] == 'add':
            return self.walkTree(node[1]) + self.walkTree(node[2])

        if node[0] == 'sub':
            return self.walkTree(node[1]) - self.walkTree(node[2])

        if node[0] == 'mul':
            return self.walkTree(node[1]) * self.walkTree(node[2])

        if node[0] == 'div':
            return self.walkTree(node[1]) / self.walkTree(node[2])

        if node[0] == 'less_than':
            return self.walkTree(node[1]) < self.walkTree(node[2])

        if node[0] == 'greater_than':
            return self.walkTree(node[1]) > self.walkTree(node[2])

        if node[0] == 'less_than_equal':
            return self.walkTree(node[1]) <= self.walkTree(node[2])

        if node[0] == 'greater_than_equal':
            return self.walkTree(node[1]) >= self.walkTree(node[2])

        if node[0] == 'var_assign':
            self.env[node[1]] = self.walkTree(node[2])
            return node[1]

        if node[0] == 'var':
            try:
                return self.env[node[1]]
            except LookupError:
                print("Undefined variable '"+node[1]+"' not found!")
                return 0

        if node[0] == 'for_loop':
            if node[1][0] == 'for_loop_setup':
                loop_setup = self.walkTree(node[1])

                loop_count = self.env[loop_setup[0]]
                loop_limit = loop_setup[1]

                for i in range(loop_count + 1, loop_limit+1):
                    res = self.walkTree(node[2])
                    if res is not None:
                        print(res)
                    self.env[loop_setup[0]] = i
                    del self.env[loop_setup[0]]

        if node[0] == 'for_loop_setup':
            return self.walkTree(node[1]), self.walkTree(node[2])


if __name__ == '__main__':
    lexer = MyLexer()
    parser = MyParser()
    env = {}
    while True:
        try:
            text = input("NATURAL >>> ")
        except EOFError:
            break
        if text:
            tree = parser.parse(lexer.tokenize(text))
            # print(tree)
            MyExecute(tree, env)
