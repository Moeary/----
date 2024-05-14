def reverse_and_push(string):
    stack = ['$']  # 初始栈顶为'$'
    stack.append('L')  # 将'L'压入栈中
    return stack

def update_string_pointer_and_stack(matrix, string, stack):
    string_pointer = 0  # 字符串指针初始位置
    round_count = 1
    while string_pointer < len(string) or stack:
        print("\n第", round_count, "轮迭代:")
        
        flag = 0    # 标记是否结束迭代
        if not stack:
            print("栈已为空，结束迭代。")
            break
        else:
            stack_top = stack.pop()  # 获取栈顶元素并弹出
            print("弹出栈顶：" + stack_top)
            if stack_top == '$' and string_pointer == len(string):
                print("栈顶为'$'且字符串指针到达末尾，结束迭代。")
                flag = 1
                break
            elif stack_top == '$' and string[string_pointer] == '#':
                print("栈顶为'$'且当前字符串指向字符为'#'，分析成功完成。")
                flag = 1
                break
        if flag:
            break
        if string_pointer < len(string):
            input_char = string[string_pointer]
            print("当前字符串指向位置的字符: " + input_char)  # 获取当前字符串指向位置的字符
        else:
            print("此时字符串为空了,检查栈顶剩余字符")
            input_char = '$'
        if stack_top == input_char:
            print("栈顶" + stack_top + "和字符串指向字符" + input_char + "相同，执行弹出")
            string_pointer += 1
            if string_pointer < len(string):
                input_char = string[string_pointer]
                print("获取更新后的字符串指向位置的字符: " + input_char)
        elif stack_top in matrix and input_char in matrix[stack_top]:
            next_value = matrix[stack_top][input_char]
            if next_value:  # 如果查询到的值不为空，则继续执行
                print("匹配规则: " + stack_top + " → " + next_value)
                for char in reversed(next_value.split()):
                    if char != 'ε':
                        stack.append(char)
                print("栈更新为：" + ''.join(stack))
            else:
                print("查询到的值为空，跳过当前循环。")
                continue  # 跳过当前循环
        else:
            print("错误：无法匹配当前栈顶与输入字符。")
            break
        round_count += 1

grammar_tables = {
    "G1": {
        'L': {'id': 'L → id = E'},
        'E': {'id': 'E → F E\'', '(': 'E → F E\''},
        'E\'': {'=': 'E\' → ε', '+': 'E\' → + F E\'', '-': 'E\' → - F E\'', ')': 'E\' → ε', '#': 'E\' → ε'},
        'F': {'id': 'F → id', '(': 'F → ( E )'}
    },
    "G2": {
        'L': {'i': 'L → i = E'},
        'E': {'i': 'E → T E\'', '(': 'E → T E\''},
        'E\'': {'=': 'E\' → ε', '*': 'E\' → * T E\'', '/': 'E\' → / T E\'', '%': 'E\' → % T E\'', ')': 'E\' → ε', '#': 'E\' → ε'},
        'T': {'i': 'T → F T\'', '(': 'T → F T\''},
        'T\'': {'=': 'T\' → ε', '*': 'T\' → ε', '/': 'T\' → ε', '%': 'T\' → ε', ')': 'T\' → ε', '#': 'T\' → ε'},
        'F': {'i': 'F → i', '(': 'F → ( E )'}
    },
    "G3": {
        'D': {'int': 'D → T L', 'float': 'D → T L'},
        'T': {'int': 'T → int', 'float': 'T → float'},
        'L': {'id': 'L → id R'},
        'R': {',': 'R → , id R', '#': 'R → ε'}
    },
    "G4": {
        'L': {'(': 'E ; L', 'id': 'E ; L', 'num': 'E ; L', ';': 'ε', '#': 'ε'},
        'E': {'(': 'T E\'', 'id': 'T E\'', 'num': 'T E\''},
        'E\'': {'+': '+ T E\'', '-': '- T E\'', ';': 'ε', ')': 'ε', '#': 'ε'},
        'T': {'(': 'F T\'', 'id': 'F T\'', 'num': 'F T\''},
        'T\'': {'*': '* F T\'', '/': '/ F T\'', 'mod': 'mod F T\'', '+': 'ε', '-': 'ε', ';': 'ε', ')': 'ε', '#': 'ε'},
        'F': {'(': '( E )', 'id': 'id', 'num': 'num'}
    }
}

# 让用户选择文法
grammar_choice = input("请选择文法（输入1使用G1，输入2使用G2，输入3使用G3，输入4使用G4）：")
if grammar_choice == '1':
    grammar = grammar_tables['G1']
elif grammar_choice == '2':
    grammar = grammar_tables['G2']
elif grammar_choice == '3':
    grammar = grammar_tables['G3']
elif grammar_choice == '4':
    grammar = grammar_tables['G4']
else:
    print("无效的输入，使用默认文法G1。")
    grammar = grammar_tables['G1']

#input_string = ["id", "+", "id", ";", "#"]
input_string = ["id", "+", "id", ";", "#"]

stack = reverse_and_push(input_string)
print("输入的字符串为:", input_string)
update_string_pointer_and_stack(grammar, input_string, stack)

if not stack:
    print("根据字符串首位和栈顶内容查询matrix_G后,栈已为空。")
else:
    print("根据字符串首位和栈顶内容查询matrix_G后的栈顶内容为:")
    while stack:
        print(stack.pop(), end='')