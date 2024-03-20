import gradio as gr
import re
import string

KEYWORDS = ['if', 'then', 'else', 'int', 'char', 'for']
SEPARATORS = [',', ';', '"']
OPERATORS = ['=', '>=', '==', '+', '/', '%', '++']
CONSTVAL = []
VAL = []

def set_code(string_s):
    string_s = re.sub(r'#.*', '', string_s)
    string_s = '\n'.join(line.strip() for line in string_s.split('\n') if line.strip())
    return string_s

def collect_constants_and_variables(code):
    state = 0
    buffer = ""
    for char in code.lower() + " ":
        if state == 0:
            if char.isalpha():
                buffer = char   
                state = 1
            elif char.isdigit():
                buffer = char
                state = 2
        elif state == 1:
            if char.isalnum() and len(buffer) < 10:
                buffer += char
            else:
                if buffer not in KEYWORDS and buffer not in VAL and buffer != 'over':
                    VAL.append(buffer)
                buffer = ""
                state = 0
        elif state == 2:
            if char.isdigit():
                buffer += char
            else:
                if buffer not in CONSTVAL:
                    CONSTVAL.append(buffer)
                buffer = ""
                state = 0

def lexical_analysis(code):
    state = 0
    buffer = ""
    symbol_table = []
    used_vars = set()
    for char in code.lower() + " ":
        if state == 0:
            if char.isalpha():
                buffer = char
                state = 1
            elif char.isdigit():
                buffer = char
                state = 2
            elif char in OPERATORS or char in SEPARATORS:
                buffer = char
                state = 3
        elif state == 1:
            if char.isalnum() and len(buffer) < 10:
                buffer += char
            else:
                if buffer in KEYWORDS:
                    symbol_table.append((buffer, '壹' + str(KEYWORDS.index(buffer))))
                elif buffer in VAL:
                    used_vars.add(buffer)
                    symbol_table.append((buffer, '伍' + str(VAL.index(buffer))))
                else:
                    symbol_table.append((buffer, 'err'))
                buffer = ""
                state = 0
        elif state == 2:
            if char.isdigit() or char.isalpha():
                buffer += char
            else:
                if buffer in CONSTVAL:
                    symbol_table.append((buffer, '肆' + str(CONSTVAL.index(buffer))))
                else:
                    symbol_table.append((buffer, 'err'))
                buffer = ""
                state = 0
        elif state == 3:
            if buffer + char in OPERATORS:
                buffer += char
            else:
                if buffer in OPERATORS:
                    symbol_table.append((buffer, '叁' + str(OPERATORS.index(buffer))))
                elif buffer in SEPARATORS:
                    symbol_table.append((buffer, '贰' + str(SEPARATORS.index(buffer))))
                else:
                    symbol_table.append((buffer, 'err'))
                buffer = char if char in OPERATORS or char in SEPARATORS else ""
                state = 0 if buffer == "" else 3
    return symbol_table, used_vars

def process_text(code):
    CONSTVAL.clear()
    VAL.clear()
    code = set_code(code)
    collect_constants_and_variables(code)
    symbol_table, used_vars = lexical_analysis(code)
    VAL[:] = [var for var in VAL if var in used_vars]
    output = "\n".join([f'{token}\t{kind}' for token, kind in symbol_table])
    output += "\nover"
    output += "\n常数表中的内容为:" + ', '.join(CONSTVAL)
    output += "\n变量表(标识符表)中的内容为：" + ', '.join(VAL)
    return output

if __name__ == "__main__":
    iface = gr.Interface(
        fn=process_text, 
        inputs=gr.Textbox(lines=5, placeholder='Input 1 here...'),
        outputs=gr.Textbox()
    )
    iface.launch()