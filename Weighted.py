import math

def sum_modulo_n(list, n):
    res=0
    for elem in list:
        res = (res + elem) % n
    return res 

class DWFA:
    def __init__(self, alphabet, states, initial_state, final_weight_function, transitions):
        for key, value in final_weight_function.items():
            assert key in states and isinstance(value, int), f"Final weight function should contain pairs: state, weight"
        for (old_state, letter) in transitions:
            weight, new_state=transitions[(old_state, letter)]
            assert old_state in states, f"invalid old state number: {old_state} in transition"
            assert isinstance(weight, int), "transition weights should be integers"
            assert new_state in states, f"invalid new state number: {new_state} in transition"
            assert letter in alphabet, f"invalid letter: {letter} in transition"
        self.states=states
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.final_weight_function = final_weight_function
        self.transitions = transitions

    def get_path_edges_weights_from_given_state(self, state, word):
        res=[]
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
        return self.weight_of_word_from_given_state(self.initial_state, word)

    def give_state_and_weight_when_starting_from_given_configuration(self, state, word):
        actual = state
        weight = self.weight_of_word_from_given_state(state, word)
        for w in word:
            _, new_state=self.transitions[(actual, w)]
            actual = new_state
        return actual, weight

    def is_equal_to(self, other, limit=100):
        are_not_equal, word = self.take_difference_automaton(other).has_word_with_weight_lower_than(0)
        if are_not_equal:
            return False, word
        are_not_equal, word = other.take_difference_automaton(self).has_word_with_weight_lower_than(0)
        if are_not_equal:
            return False, word
        return True, ""

    def take_difference_automaton(self, other):
        assert self.alphabet == other.alphabet, "Alphabets of differentitated automata should be the same."
        states=[]
        final_weight_function={}
        transitions={}
        for our_state in self.states:
            for other_state in other.states:
                states.append((our_state, other_state))
                final_weight_function[(our_state, other_state)] = self.final_weight_function[our_state] - other.final_weight_function[other_state]
                for letter in self.alphabet:
                    our_weight, our_new_state=self.transitions[(our_state, letter)]
                    other_weight, other_new_state=other.transitions[(other_state, letter)]
                    transitions[((our_state, other_state), letter)] = (our_weight - other_weight, (our_new_state, other_new_state))
        return DWFA(self.alphabet, states, (self.initial_state, other.initial_state), final_weight_function, transitions)

    def has_word_with_weight_lower_than(self, threshold):
        dist = {}
        for state in self.states:
            dist[state] = (math.inf, "")
        dist[self.initial_state] = (0, "")
        for _ in range(len(self.states) - 1):
            for (old_state, letter) in self.transitions:
                weight, new_state=self.transitions[(old_state, letter)]
                old_dist_weight, old_dist_word = dist[old_state]
                new_dist_weight, _ = dist[new_state]
                if new_dist_weight > old_dist_weight + weight:
                    dist[new_state] = (old_dist_weight + weight, old_dist_word + letter)
            for state, info in dist.items():
                weight, word = info
                if weight + self.final_weight_function[state] < threshold:
                    return True, word
        for (old_state, letter) in self.transitions:
            weight, new_state=self.transitions[(old_state, letter)]
            old_dist_weight, old_dist_word = dist[old_state]
            new_dist_weight, _ = dist[new_state]
            if new_dist_weight > old_dist_weight + weight:
                return True, old_dist_word + letter
        for state, info in dist.items():
            weight, word = info
            if weight + self.final_weight_function[state] < threshold:
                return True, word
        return False, ""
