import gradio as gr

def parse_G1(grammar, input_string):
    stack = ["#", "L"]
    input_string.append("#")
    pointer = 0
    loop = 0
    output_string = ""
    while len(stack) > 0:
        top = stack[-1]
        current_input = input_string[pointer]
        output_string += f"\n第 {loop} 轮迭代\n"
        print(f"\n第 {loop} 轮迭代")
        loop += 1
        output_string += f"栈: {stack}\n"
        print(f"栈: {stack}")
        output_string += f"输入: {input_string[pointer]}\n"
        print(f"输入: {input_string[pointer]}")
        
        if top == current_input:
            output_string += f"匹配终结符: {top}\n"
            print(f"匹配终结符: {top}")
            stack.pop()
            pointer += 1
            if current_input == "#":
                print("解析成功完成！")
                return "输入正确\n"+output_string
        elif top in grammar and current_input in grammar[top]:
            rule = grammar[top][current_input]
            output_string += f"应用规则: {rule}\n"
            print(f"应用规则: {rule}")
            stack.pop()
            if rule != "ε":
                production = rule.split("→")[1].strip().split()
                for symbol in reversed(production):
                    stack.append(symbol)
        else:
            output_string += f"错误: {top} 与输入 {current_input} 无法匹配\n"
            print(f"错误: {top} 与输入 {current_input} 无法匹配")
            return "解析失败！\n"+output_string
    return "解析失败！\n"+output_string

def parse_G2_G3_G4(grammar, input_string):
    stack = ["#", "L"]
    input_string.append("#")
    pointer = 0
    output_string = ""
    while len(stack) > 0:
        top = stack[-1]
        current_input = input_string[pointer]
        output_string += f"\n栈: {stack}\n"
        print(f"栈: {stack}")
        output_string += f"输入: {input_string[pointer]}\n"
        print(f"输入: {input_string[pointer]}")
        
        if top == current_input:
            output_string += f"匹配终结符: {top}\n"
            print(f"匹配终结符: {top}")
            stack.pop()
            pointer += 1
            if current_input == "#":
                output_string += "解析成功完成！\n"
                print("解析成功完成！")
                return "True\n"+output_string
        elif top in grammar and current_input in grammar[top]:
            rule = grammar[top][current_input]
            output_string += f"应用规则: {rule}\n"
            print(f"应用规则: {rule}")
            stack.pop()
            if rule != "ε":
                production = rule.split()
                for symbol in reversed(production):
                    stack.append(symbol)
        else:
            output_string += f"错误: {top} 与输入 {current_input} 无法匹配\n"
            print(f"错误: {top} 与输入 {current_input} 无法匹配")
            return "False"+output_string
    return "False"+output_string

grammar_tables = {
    "G1": {
        'L': {'id': 'L → id = E'},
        'E': {'id': 'E → F', '(': 'E → F'},
        'E\'': {'+': 'E\' → + F E\'', '-': 'E\' → - F E\'', ')': 'E\' → ε', '#': 'E\' → ε'},
        'F': {'id': 'F → id', '(': 'F → ( E )'}
    },
    "G2": {
        'L': {'id': 'id = E'},
        'E': {'id': 'T', '(': 'T'},
        'E\'': {'*': '* T E\'', '/': '/ T E\'', '%': '% T E\'', '+': 'ε', '-': 'ε', ';': 'ε', ')': 'ε', '#': 'ε'},
        'T': {'id': 'F', '(': 'F'},
        'T\'': {'*': '* F T\'', '/': '/ F T\'', '%': '% F T\'', '+': 'ε', '-': 'ε', ';': 'ε', ')': 'ε', '#': 'ε'},
        'F': {'id': 'id', '(': '( E )'}
    },
    "G3": {
        'D': {'int': 'T L', 'float': 'T L'},
        'T': {'int': 'int', 'float': 'float'},
        'L': {'id': 'id R'},
        'R': {',': ', id R', '#': 'ε'}
    },
    "G4": {
        'L': {'(': 'E ; L', 'id': 'E ; L', 'num': 'E ; L', ';': 'ε', '#': 'ε'},
        'E': {'(': 'T E\'', 'id': 'T E\'', 'num': 'T E\''},
        'E\'': {'+': '+ T E\'', '-': '- T E\'', ';': 'ε', ')': 'ε', '#': 'ε'},
        'T': {'(': 'F T\'', 'id': 'F T\'', 'num': 'F T\''},
        'T\'': {'*': '* F T\'', '/': '/ F T\'', '%': '% F T\'', '+': 'ε', '-': 'ε', ';': 'ε', ')': 'ε', '#': 'ε'},
        'F': {'(': '( E )', 'id': 'id', 'num': 'num'}
    },
}

Vt ={
    "G1": ["id", "=", "+", "-", "(", ")", "#"],
    "G2": ["id", "=", "+", "-", "*", "/", "%", "(", ")", "#"],
    "G3": ["int", "float", "id", ",", "#"],
    "G4": ["id", "num", "+", "-", "*", "/", "%", "(", ")", ";", "#"]
}

def parse_interface(input_string, grammar_choice):
    input_list = input_string.split()
    if grammar_choice == '1':
        for element in input_list:
            if element not in Vt['G1']:
                return f"错误：'{element}' 不在文法G1的终结符列表中。"
        return parse_G1(grammar_tables['G1'], input_list)
    elif grammar_choice == '2':
        for element in input_list:
            if element not in Vt['G2']:
                return f"错误：'{element}' 不在文法G2的终结符列表中。"
        return parse_G2_G3_G4(grammar_tables['G2'], input_list)
    elif grammar_choice == '3':
        for element in input_list:
            if element not in Vt['G3']:
                return f"错误：'{element}' 不在文法G3的终结符列表中。"
        return parse_G2_G3_G4(grammar_tables['G3'], input_list)
    elif grammar_choice == '4':
        for element in input_list:
            if element not in Vt['G4']:
                return f"错误：'{element}' 不在文法G4的终结符列表中。"
        return parse_G2_G3_G4(grammar_tables['G4'], input_list)
    else:
        for element in input_list:
            if element not in Vt['G1']:
                return f"错误：'{element}' 不在文法G1的终结符列表中。"
        return "无效的输入,使用默认文法G1。"+parse_G1(grammar_tables['G1'], input_list)

iface = gr.Interface(
    fn=parse_interface, 
    inputs=[
        gr.Textbox(label="Input String"),
        gr.Dropdown(choices=['1', '2', '3', '4'], label="Grammar Choice")
    ], 
    outputs="text",
    title="Parser",
    description="请输入字符串和选择语法模型，然后查看解析过程。"
)

iface.launch()