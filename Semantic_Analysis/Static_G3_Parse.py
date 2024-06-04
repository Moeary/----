from ply import lex
from ply import yacc

# 词法规则
tokens = ('INT', 'FLOAT', 'ID', 'COMMA', 'SEMICOLON')

def t_KEYWORD(t):
    r'int|float'
    if t.value == 'int':
        t.type = 'INT'
    elif t.value == 'float':
        t.type = 'FLOAT'
    return t

t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_COMMA = r','
t_SEMICOLON = r';'

t_ignore = ' \t\n'

def t_error(t):
    print(f"非法字符: {t.value[0]} at line {t.lineno}, position {t.lexpos}")
    t.lexer.skip(1)

lexer = lex.lex()

# 符号表
symbol_table = {}

# 当前地址
current_address = 1024

# 语法规则和语义动作
def p_D(p):
    '''D : T L SEMICOLON'''
    global current_address  # 声明 current_address 是全局变量
    # 获取类型和变量列表
    var_type = p[1]
    var_list = p[2]
    
    # 将变量添加到符号表
    for var in var_list:
        if var in symbol_table:
            print(f"错误: 变量 '{var}' 重复定义")
        else:
            symbol_table[var] = {'type': var_type, 'address': current_address}
            current_address += 4

def p_T(p):
    '''T : INT
       | FLOAT'''
    p[0] = p[1]

def p_L(p):
    '''L : ID R'''
    p[0] = [p[1]] + p[2]

def p_R(p):
    '''R : COMMA ID R
       | '''
    if len(p) == 4:
        p[0] = [p[2]] + p[3]
    else:
        p[0] = []

def p_error(p):
    if p:
        print(f"语法错误， unexpected token: {p.value} at line {p.lineno}, position {p.lexpos}")
    else:
        print("语法错误: 意外的文件结束")

parser = yacc.yacc()

# 测试代码
input_string = "int a,b,c,disc,x1;float x2,p,q;"
statements = input_string.split(';')

for statement in statements:
    statement = statement+';'
    if statement and statement !=";" :  # 忽略空语句
        parser.parse(statement)

# 打印符号表
print("符号表:")
for name, var_info in symbol_table.items():
    print(f"  {name}: address={var_info['address']}, type={var_info['type']}")