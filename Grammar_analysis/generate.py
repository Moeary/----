import re

def tokenize(expression):
    return re.findall(r'\b(id)\b|-', expression) + ['$']


# 定义文法 G 的产生式
grammar = {
    'L': ['E;L', 'ε'],
    'E': ['TE\'',],
    'E\'': ['+TE\'', '-TE\'', 'ε'],
    'T': ['FT\'',],
    'T\'': ['*FT\'', '/FT\'', 'mod FT\'', 'ε'],
    'F': ['(E)', 'id', 'num']
}

# 定义分析表（与上面表格一致）
action_table = {
    0: {'id': 'S1', 'num': 'S2', '(': 'S4'},
    1: {'$': 'R6', ';': 'R6', '+': 'R6', '-': 'R6', '*': 'R6', '/': 'R6', 'mod': 'R6', ')': 'R6'},
    2: {'$': 'R6', ';': 'R6', '+': 'R6', '-': 'R6', '*': 'R6', '/': 'R6', 'mod': 'R6', ')': 'R6'},
    3: {'id': 8, 'num': 2, '(': 4},
    4: {'id': 9, 'num': 2, '(': 4},
    5: {'$': 'R8', ';': 'R8', '+': 'R8', '-': 'R8', '*': 'R8', '/': 'R6', 'mod': 'R8', ')': 'R8'},
    6: {'id': 10, 'num': 2, '(': 4},
    7: {'+': 11, '-': 12, ')': 13},
    8: {'$': 'R6', ';': 'R6', '+': 'R6', '-': 'R6', '*': 'R6', '/': 'R6', 'mod': 'R6', ')': 'R6'},
    9: {'$': 'R6', ';': 'R6', '+': 'R6', '-': 'R6', '*': 'R6', '/': 'R6', 'mod': 'R6', ')': 'R6'},
    10: {'$': 'R8', ';': 'R8', '+': 'R8', '-': 'R8', '*': 'R8', '/': 'R6', 'mod': 'R8', ')': 'R8'},
    11: {'id': 14, 'num': 2, '(': 4},
    12: {'id': 15, 'num': 2, '(': 4},
    13: {'$': 'R4', ';': 'R4', '+': 'R4', '-': 'R4', '*': 'R4', '/': 'R4', 'mod': 'R4', ')': 'R4'},
    14: {'$': 'R6', ';': 'R6', '+': 'R6', '-': 'R6', '*': 'R6', '/': 'R6', 'mod': 'R6', ')': 'R6'},
    15: {'$': 'R8', ';': 'R8', '+': 'R8', '-': 'R8', '*': 'R8', '/': 'R6', 'mod': 'R8', ')': 'R8'}
}

# 定义分析函数
def analyze(expression):
    # 初始化栈和输入串
    if length > len(stack):
        return False  # 出错
    else:
        stack = stack[:-length]

    # 分析过程
    while True:
        state = stack[-1]
        symbol = input_string[0]

        # 根据分析表进行操作
        action = action_table[state].get(symbol)

        if action is None:
            return False  # 出错

        elif action[0] == 'S':  # 移进
            stack.append(int(action[1:]))
            input_string.pop(0)

        elif action[0] == 'R':  # 归约
            production_num = int(action[1:])
            production = list(grammar.values())[production_num - 1][0]
            length = len(production)

            # 弹出栈中对应产生式的符号
            stack = stack[:-length]

            # 根据产生式左部符号找到新的状态
            state = stack[-1]
            nonterminal = list(grammar.keys())[production_num - 1]
            new_state = action_table[state].get(nonterminal)

            # 将新状态入栈
            stack.append(new_state)

            print(f"归约: {production}")

        elif action == 'acc':
            return True  # 接受


# 测试语句
expression = "id"

input_string = tokenize(expression)
result = analyze(input_string)

if result:
    print("语句分析成功！")
else:
    print("语句分析失败！")