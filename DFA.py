#transitions is dict
class DFA:
    def __init__(self, alphabet, states, initial, finals, transitions):
        assert initial in states
        for state in finals:
            assert state in states
        for (((old_state, letter), new_state)) in transitions:
            assert old_state in states and new_state in states and letter in alphabet
        self.alphabet = alphabet
        self.states = states
        self.initial = initial
        self.finals = finals
        self.transitions = transitions
    def check_if_word_in_language(self, word):
        actual=self.initial
        for w in word:
            actual=self.transitions[(self.actual, w)]
        return actual in self.finals