from ply import lex
from ply import yacc

# 定义词法规则
tokens = ('ID', 'EQUALS', 'PLUS', 'MINUS', 'LPAREN', 'RPAREN')

t_EQUALS = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

# 忽略空格和换行符
t_ignore = ' \t\n'

# 创建词法分析器
lexer = lex.lex()

# 定义全局变量
id_count = 1
id_map = {}

# 定义语法规则
def p_L(p):
    '''L : E'''
    p[0] = p[1]

def p_E_equals(p):
    '''E : E EQUALS T'''
    p[0] = f'{p[1]}={p[3]}'

def p_E_plus(p):
    '''E : E PLUS T'''
    p[0] = f'{p[1]}+{p[3]}'

def p_E_T(p):
    '''E : T'''
    p[0] = p[1]

def p_T_minus(p):
    '''T : T MINUS F'''
    p[0] = f'{p[1]}-{p[3]}'

def p_T_F(p):
    '''T : F'''
    p[0] = p[1]

def p_F_paren(p):
    '''F : LPAREN E RPAREN'''
    p[0] = f'({p[2]})'

def p_F_id(p):
    '''F : ID'''
    global id_count
    if p[1] not in id_map:
        id_map[p[1]] = f'id{id_count}'
        id_count += 1
    p[0] = id_map[p[1]]

# 处理语法错误
def p_error(p):
    print(f"Syntax error at '{p.value}'")

# 创建解析器
parser = yacc.yacc()

# 解析输入并输出结果
input_string = "x = y + z - (a + b)"
result = parser.parse(input_string, lexer=lexer)  # 将 lexer 传递给 parser.parse()
print(f"L -> {result}")
