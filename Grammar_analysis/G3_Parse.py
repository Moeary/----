grammar_tables = {
    "G3": {
        'D': {'int': 'T L', 'float': 'T L'},
        'T': {'int': 'int', 'float': 'float'},
        'L': {'id': 'id R'},
        'R': {',': ', id R', '#': 'ε'}
    }
}

def parse(grammar, input_string):
    stack = ["#", "D"]
    input_string.append("#")
    pointer = 0
    
    while len(stack) > 0:
        top = stack[-1]
        current_input = input_string[pointer]
        
        print(f"栈: {stack}")
        print(f"输入: {input_string[pointer:]}")
        
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
                production = rule.split()
                for symbol in reversed(production):
                    stack.append(symbol)
        else:
            print(f"错误: {top} 与输入 {current_input} 无法匹配")
            return False
    return False

input_string = ["int", "id", ",", "id", "#"]
parse(grammar_tables["G3"], input_string)