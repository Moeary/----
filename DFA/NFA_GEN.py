from pyformlang.regular_expression import Regex

def regex_to_transitions(regex_str):
    regex = Regex(regex_str)
    enfa = regex.to_epsilon_nfa().remove_epsilon_transitions()
    transitions = {}
    for state in enfa.states:
        transitions[state] = {}
        for symbol in enfa._input_symbols:
            next_states = enfa(state, symbol)
            if next_states:
                transitions[state][symbol] = next_states
    return transitions

regex_str = "(a|b)*bb(>|<|>=|<=|==)1"
transitions = regex_to_transitions(regex_str)
print(transitions)