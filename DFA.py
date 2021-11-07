#transitions is dict
class DFA:
    def __init__(self, alphabet, states, initial, finals, transitions):
        assert initial in states
        for state in finals:
            assert state in states
        for (old_state, letter) in transitions:
            assert old_state in states and transitions[(old_state, letter)] in states and letter in alphabet
        self.alphabet = alphabet
        self.states = states
        self.initial = initial
        self.finals = finals
        self.transitions = transitions
    def check_if_word_in_language(self, word):
        actual=self.initial
        for w in word:
            actual=self.transitions[(actual, w)]
        return actual in self.finals
'''def diff(self, other):
        return DFA(self.alphabet, 
            [(my_state, others_state) for my_state in self.states for others_state in other.states],
            (self.initial, other.initial), 
            [(my_final_state, others_non_final_state) for my_final_state in self.finals for others_non_final_state in other.states if others_non_final_state not in other.finals]
            {((first_old_state, second_old_state), letter) : (first_new_state, second_new_state)})'''