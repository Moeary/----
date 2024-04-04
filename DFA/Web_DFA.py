import gradio as gr
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA

nfa1 = NFA(
    states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5'},
    input_symbols={'a', 'b', '+', '-', '1'},
    transitions={
        'q0': {'a': {'q0'}, 'b': {'q0', 'q1'}},
        'q1': {'b': {'q2'}},
        'q2': {'+': {'q3'}, '-': {'q3'}},
        'q3': {'1': {'q4'}},
    },
    initial_state='q0',
    final_states={'q4'}
)

nfa2 = NFA(
    states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8'},
    input_symbols={'a', 'b', '@', '1', '2', '6', '3', 'm'},
    transitions={
        'q0': {'a': {'q0'}, 'b': {'q0'}, '@': {'q1'}},
        'q1': {'1': {'q2', 'q4'}},
        'q2': {'2': {'q3'}},
        'q3': {'6': {'q8'}},
        'q4': {'6': {'q5'}},
        'q5': {'3': {'q8'}},
        'q8': {'m': {'q6'}}
    },
    initial_state='q0',
    final_states={'q6'}
)

nfa3 = NFA(
    states={'q0', 'q1', 'q2', 'q3', 'q4'},
    input_symbols={'a', 'b', '+', '-', '*', '/', '%'},
    transitions={
        'q0': {'a': {'q0'}, 'b': {'q0', 'q1'}},
        'q1': {'b': {'q2'}},
        'q2': {'+': {'q3'}, '-': {'q3'}, '*': {'q3'}, '/': {'q3'}, '%': {'q3'}},
        'q3': {'b': {'q4'}}
    },
    initial_state='q0',
    final_states={'q4'}
)

nfa4 = NFA(
    states={'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'},
    input_symbols={'a', 'b', '>', '<', '=', '!', '1'},
    transitions={
        'A': {'a': {'B'}, 'b': {'B'}},
        'B': {'a': {'B'}, 'b': {'B', 'C'}},
        'C': {'b': {'D'}},
        'D': {'>': {'E', 'H'}, '<': {'E', 'I'}, '=': {'F'}, '!': {'J'}},
        'E': {'1': {'G'}},
        'F': {'=': {'E'}},
        'H': {'=': {'E'}},
        'I': {'=': {'E'}},
        'J': {'=': {'E'}}
    },
    initial_state='A',
    final_states={'G'}
)


def run_dfa(input_str, nfa_choice):
    # Choose the NFA based on the user's choice
    if nfa_choice == '1':
        nfa = nfa1
    elif nfa_choice == '2':
        nfa = nfa2
    elif nfa_choice == '3':
        nfa = nfa3
    elif nfa_choice == '4':
        nfa = nfa4
    else:
        return "错误的NFA选择，请选择1-4之间的数字！"

    # Convert the chosen NFA to a DFA
    dfa = DFA.from_nfa(nfa)

    try:
        final_state = dfa.read_input(input_str)
        steps = dfa.read_input_stepwise(input_str)
        steps_str = "自动机步骤如下\n" + '\n'.join(f"自动机现在在状态: {step}" for step in steps)
        transitions_str = "转移矩阵如下:\n" + '\n'.join(f"{state}: {transitions}" for state, transitions in dfa.transitions.items())
        return f"自动机结束于状态: {final_state}\n\n{steps_str}\n\n{transitions_str}"
    except:
        return "错误的输入，请检查输入是否符合规则！"

iface = gr.Interface(
    fn=run_dfa, 
    inputs=["text", gr.Radio(['1', '2', '3', '4'], label="选择NFA模型")], 
    outputs=gr.Textbox(label="结果")
)

iface.launch()