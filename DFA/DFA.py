def is_valid_string(dfa_table, input_string):
    current_state = "A"  # Start at the initial state

    for symbol in input_string:
        if symbol not in dfa_table[current_state]:
            return False  # Invalid symbol encountered

        current_state = dfa_table[current_state][symbol]  # Transition to next state

    return current_state == "F"  # Check if we end in the final state

# Minimized DFA table (replace with your actual table if different)
dfa_table = {
    "A": {"a": "A", "b": "A", ">": "B", "<": "C", "=": "D", "!": "E", "1": "A"},
    "B": {"a": "B", "b": "F", ">": "B", "<": "B", "=": "B", "!": "B", "1": "F"},
    "C": {"a": "C", "b": "C", ">": "B", "<": "C", "=": "C", "!": "C", "1": "C"},
    "D": {"a": "D", "b": "D", ">": "B", "<": "D", "=": "D", "!": "D", "1": "D"},
    "E": {"a": "E", "b": "E", ">": "B", "<": "E", "=": "E", "!": "E", "1": "E"},
    "F": {"a": "F", "b": "F", ">": "F", "<": "F", "=": "F", "!": "F", "1": "F"},
}

# Example usage
input_string = "a>!b1"  # Replace with your input string
if is_valid_string(dfa_table, input_string):
    print("The string is valid.")
else:
    print("The string is invalid.")