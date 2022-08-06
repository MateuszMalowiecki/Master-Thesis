from lib2to3.pytree import LeafPattern
import random

def sum_modulo_n(list, n):
    res=0
    for elem in list:
        res = (res + elem) % n
    return res 

class DWFA:
    def __init__(self, alphabet, states, initial_weight_function, final_weight_function, transitions):
        for key, value in initial_weight_function.items():
            assert key in states and isinstance(value, int) and value >= 0, f"Initial weight function should contain pairs: state, weight"
        for key, value in final_weight_function.items():
            assert key in states and isinstance(value, int) and value >= 0, f"Final weight function should contain pairs: state, weight"
        for (old_state, letter) in transitions:
            weight, new_state=transitions[(old_state, letter)]
            assert old_state in states, f"invalid old state number: {old_state} in transition"
            assert isinstance(weight, int) and weight >= 0, "transition weights should be integers greater than zero"
            assert new_state in states, f"invalid new state number: {new_state} in transition"
            assert letter in alphabet, f"invalid letter: {letter} in transition"
        self.states=states
        self.alphabet = alphabet
        self.initial_weight_function = initial_weight_function
        self.final_weight_function = final_weight_function
        self.transitions = transitions

    def get_path_edges_weights_from_given_state(self, state, word):
        res=[self.initial_weight_function[state]]
        actual_state=state
        for w in word:
            weight, new_state=self.transitions[(actual_state, w)]
            res.append(weight)
            actual_state=new_state
        res.append(self.final_weight_function[actual_state])
        return res

    def weight_of_word_from_given_state(self, state, word):
        path=self.get_path_edges_weights_from_given_state(state, word)
        return sum_modulo_n(path, 1000000000000)

    def weight_of_word(self, word):
        res=0
        for state in self.states:
            res = (res + self.weight_of_word_from_given_state(state, word)) % 1000000000000
        return res

    def give_state_and_weight_when_starting_from_given_configuration(self, state, word):
        actual = state
        weight = self.weight_of_word_from_given_state(state, word)
        for w in word:
            _, new_state=self.transitions[(actual, w)]
            actual = new_state
        return actual, weight

    def is_equal_to(self, other, limit=100):
        for i in range(5000):
            len = random.randint(0, limit)
            word = ''.join(random.choices(self.alphabet, k=len))
            if self.weight_of_word(word) != other.weight_of_word(word):
                return False, word
        return True, ""
