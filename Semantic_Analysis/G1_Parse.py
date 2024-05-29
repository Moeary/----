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
# 符号表
symbol_table = {}
# 地址分配计数器
address_counter = 100

# 为变量分配地址
def allocate_address(var_name):
    global address_counter
    if var_name not in symbol_table:
        symbol_table[var_name] = {
            "address": address_counter
        }
        address_counter += 1

# 生成三元式
temp_count = 1
temp_map = {}
intermediate_code = []

def new_temp():
    global temp_count
    temp = f't{temp_count}'
    temp_count += 1
    return temp

def gen_code(op, arg1, arg2=None, result=None):
    if result is None:  # 如果没有提供 result，则不需要生成赋值操作
        intermediate_code.append((op, arg1, arg2))
    else:
        if arg2 is None:  # 单个操作数
            intermediate_code.append((op, arg1, result))
        else:  # 两个操作数
            intermediate_code.append((op, arg1, arg2, result))



# 处理词法错误
def t_error(t):
    print(f"Illegal character: {t.value[0]}")
    t.lexer.skip(1)


def p_L(p):
    '''L : E'''
    p[0] = p[1]

def p_E_equals(p):
    '''E : E EQUALS T'''
    p[0] = f'{p[1]}={p[3]}'
    gen_code('=', p[3], p[1])

def p_E_plus(p):
    '''E : E PLUS T'''
    temp = new_temp()
    p[0] = temp
    gen_code('+', p[1], p[3], temp)  # 正确调用 gen_code

def p_T_minus(p):
    '''T : T MINUS F'''
    temp = new_temp()
    p[0] = temp
    gen_code('-', p[1], p[3], temp)  # 正确调用 gen_code

def p_E_T(p):
    '''E : T'''
    p[0] = p[1]

def p_T_F(p):
    '''T : F'''
    p[0] = p[1]

def p_F_paren(p):
    '''F : LPAREN E RPAREN'''
    p[0] = p[2]

def p_F_id(p):
    '''F : ID'''
    global id_count
    if p[1] not in id_map:
        id_map[p[1]] = f'id{id_count}'
        id_count += 1
    p[0] = id_map[p[1]]
    allocate_address(p[0])


# 创建解析器
parser = yacc.yacc()

# 解析输入并输出结果
input_string = "x = y + z - (a + b)"
result = parser.parse(input_string, lexer=lexer)
print(f"L -> {result}")
print("符号表:")
for name, entry in symbol_table.items():
    print(f"  {name}: {entry}")
print("\n三元式:")
for code in intermediate_code:
    print(code)
