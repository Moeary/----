from collections import defaultdict

# 输入的产生式
productions = {
    'L': [['i','=', 'E']],
    'E': [['E', '+', 'F'], ['E', '-', 'F'], ['F']],
    'F': [['(', 'E', ')'], ['i']]
}

# 计算FIRST集
def first(symbol, visited=None):
    if visited is None:
        visited = set()
    if symbol in terminals:
        return {symbol}
    if symbol in visited:
        return set()
    visited.add(symbol)
    result = set()
    for production in productions[symbol]:
        for s in production:
            if s in terminals:
                result.add(s)
                break
            f = first(s, visited)
            result.update(f)
            if 'ε' not in f:
                break
    else:
        result.add('ε')
    return result

# 计算FOLLOW集
def follow(symbol):
    result = set()
    if symbol == start_symbol:
        result.add('$')
    for lhs, rhs in productions.items():
        for production in rhs:
            try:
                position = production.index(symbol)
            except ValueError:
                continue
            if position + 1 < len(production):
                result.update(first(production[position + 1]) - {'ε'})
            if position + 1 == len(production) or 'ε' in first(production[position + 1]):
                result.update(follow(lhs))
    return result

# 生成LL(1)解析表
def generate_table():
    table = defaultdict(dict)
    for lhs, rhs in productions.items():
        for production in rhs:
            for symbol in production:  # 遍历每个字符
                if symbol != 'ε':
                    table[lhs][symbol] = production
                if 'ε' in first(symbol):  # 将符号作为参数传递给first函数
                    for symbol in follow(lhs):
                        table[lhs][symbol] = production
    return table

# 测试
start_symbol = 'L'
terminals = {'i', '=', '+', '-', '(', ')', 'ε', '$'}
non_terminals = {'L', 'E', 'F'}
print(generate_table())