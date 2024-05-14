grammar_tables = {
    "G1": {
        'L': {'id': 'L → id = E'},
        'E': {'id': 'E → F', '(': 'E → F'},
        'E\'': {'+': 'E\' → + F E\'', '-': 'E\' → - F E\'', ')': 'E\' → ε', '#': 'E\' → ε'},
        'F': {'id': 'F → id', '(': 'F → ( E )'}
    }
}

input_string = ["id", "+", "id", ";", "#"]

def parse(grammar, input_string):
    stack = ["#", "L"]
    input_string.append("#")
    pointer = 0
    loop = 0
    while len(stack) > 0:
        top = stack[-1]
        current_input = input_string[pointer]
        print(f"\n第 {loop} 轮迭代")
        loop += 1
        print(f"栈: {stack}")
        print(f"输入: {input_string[pointer]}")
        
        if top == current_input:
            print(f"匹配终结符: {top}")
            stack.pop()
            pointer += 1
            if current_input == "#":
                print("解析成功完成！")
                return True
        elif top in grammar and current_input in grammar[top]:
            rule = grammar[top][current_input]
            print(f"应用规则: {rule}")
            stack.pop()
            if rule != "ε":
                production = rule.split("→")[1].strip().split()
                for symbol in reversed(production):
                    stack.append(symbol)
        else:
            print(f"错误: {top} 与输入 {current_input} 无法匹配")
            return False
    return False

input_string = ["id", "=", "id"]
parse(grammar_tables["G1"], input_string)
