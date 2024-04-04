from automata.fa.dfa import DFA
from automata.fa.nfa import NFA

# 定义NFA
nfa = NFA(
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


# 将NFA转换为DFA
dfa = DFA.from_nfa(nfa)

print(dfa)

# 读取输入
input_str = 'aabb!=1'

final_state = dfa.read_input(input_str)
# 读取输入的每一步
steps = dfa.read_input_stepwise(input_str)
# 打印最终状态
print("The automaton ends in state:", final_state)
# 打印每一步的状态
print("The automaton steps are:")
for step in steps:
    print("The automaton is in state:", step)