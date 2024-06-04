from ply import lex
from ply import yacc

# 词法规则
tokens = (
    'INT', 'FLOAT', 'ID', 'EQUALS', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
    'LPAREN', 'RPAREN', 'COMMA', 'SEMICOLON'
)

def t_KEYWORD(t):
    r'int|float'
    if t.value == 'int':
        t.type = 'INT'
    elif t.value == 'float':
        t.type = 'FLOAT'
    return t

t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_EQUALS = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'mod'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_SEMICOLON = r';'

t_ignore = ' \t\n'

def t_error(t):
    print(f"非法字符: {t.value[0]} at line {t.lineno}, position {t.lexpos}")
    t.lexer.skip(1)

lexer = lex.lex()

# 符号表和地址分配
symbol_table = {}
address_counter = 1024

def allocate_address(symbol, var_type=None):
    """为符号分配地址并更新符号表"""
    global address_counter
    if symbol in symbol_table:
        print(f"错误: 变量 '{symbol}' 重复定义")
        return
    symbol_table[symbol] = {'address': address_counter, 'type': var_type}
    address_counter += 4  # 假设每个变量占用 4 个字节

# 三地址码生成
temp_count = 1
intermediate_code = []

def new_temp():
    global temp_count
    temp = f't{temp_count}'
    temp_count += 1
    return temp

def gen_code(op, arg1, arg2=None, result=None):
    if result is None:
        intermediate_code.append((op, arg1, arg2))
    else:
        if arg2 is None:
            intermediate_code.append((op, arg1, result))
        else:
            intermediate_code.append((op, arg1, arg2, result))

# 语法规则和语义动作

def p_program(p):
    '''program : declaration_list statement_list'''
    pass

def p_declaration_list(p):
    '''declaration_list : declaration declaration_list
                       | declaration'''
    pass

def p_declaration(p):
    '''declaration : INT L SEMICOLON
                   | FLOAT L SEMICOLON'''
    var_type = p[1]
    for var in p[2]:
        allocate_address(var, var_type)

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

def p_statement_list(p):
    '''statement_list : statement statement_list
                      | statement'''
    pass

def p_statement(p):
    '''statement : E SEMICOLON'''
    pass

def p_E_assign(p):
    '''E : ID EQUALS E'''
    if p[1] not in symbol_table:
        allocate_address(p[1])
    p[0] = p[3]
    gen_code('=', p[3], p[1])

def p_E_plus(p):
    '''E : E PLUS T'''
    temp = new_temp()
    p[0] = temp
    gen_code('+', p[1], p[3], temp)

def p_E_minus(p):
    '''E : E MINUS T'''
    temp = new_temp()
    p[0] = temp
    gen_code('-', p[1], p[3], temp)

def p_E_T(p):
    '''E : T'''
    p[0] = p[1]

def p_T_times(p):
    '''T : T TIMES F'''
    temp = new_temp()
    p[0] = temp
    gen_code('*', p[1], p[3], temp)

def p_T_divide(p):
    '''T : T DIVIDE F'''
    temp = new_temp()
    p[0] = temp
    gen_code('/', p[1], p[3], temp)

def p_T_mod(p):
    '''T : T MOD F'''
    temp = new_temp()
    p[0] = temp
    gen_code('mod', p[1], p[3], temp)

def p_T_F(p):
    '''T : F'''
    p[0] = p[1]

def p_F_paren(p):
    '''F : LPAREN E RPAREN'''
    p[0] = p[2]

def p_F_id(p):
    '''F : ID'''
    if p[1] not in symbol_table:
        print(f"错误：变量 '{p[1]}' 未定义")
        p[0] = 0  # 可以考虑抛出异常
    else:
        p[0] = p[1]

def p_error(p):
    if p:
        print(f"语法错误， unexpected token: {p.value} at line {p.lineno}, position {p.lexpos}")
    else:
        print("语法错误: 意外的文件结束")

parser = yacc.yacc()

# 测试代码
input_string = """
int a, b, c, disc, x1, x2, p, q;
disc = b * b - a * c;
"""
# 调用 p_program 规则来解析输入
parser.parse(input_string)

# 打印符号表和三地址码
print("符号表:")
for name, entry in symbol_table.items():
    print(f"  {name}: address={entry['address']}, type={entry['type']}")

print("\n三地址码:")
for code in intermediate_code:
    print(code)
