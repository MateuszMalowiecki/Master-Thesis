#transitions is set
class NFA:
    def __init__(self, alphabet, states, initial, finals, transitions):
        assert initial in states
        for state in finals:
            assert state in states
        for (old_state, letter, new_state) in transitions:
            assert old_state in states and new_state in states and letter in alphabet
        self.alphabet = alphabet
        self.states = states
        self.initial = initial
        self.finals = finals
        self.transitions = transitions
    def check_if_word_in_language(self, word):
        actual_states=[self.initial]
        for w in word:
            actual_states_before_iteration=actual_states
            for state in actual_states_before_iteration:
                actual_states.remove(state)
                for (old_state, letter, new_state) in transitions:
                    if old_state == state and letter == w:
                        actual_states.append(new_state)
        return len([state for state in actual_states if state in self.finals]) > 0