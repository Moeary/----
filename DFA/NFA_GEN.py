from automata.fa.nfa import NFA
from automata.fa.gnfa import GNFA

nfa=NFA.from_regex('(a|b)*aa')

gnfa=GNFA.from_nfa(nfa).to_regex()

print(gnfa)