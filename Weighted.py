from lib2to3.pytree import LeafPattern
import random
import numpy
import time

def sum_modulo_n(list, n):
    res=0
    for elem in list:
        res = (res + elem) % n
    return res 

def product_modulo_n(list, n):
    res=1
    for elem in list:
        res = (res * elem) % n
    return res 

#TODO: Ask JMi if there is any way to check equality of two WFAs
# and maybe consider automata over tropical semiring.
class DWeighted_Automata:
    def __init__(self, alphabet, states, initial_weight_function, final_weight_function, transitions):
        for key, value in initial_weight_function.items():
            print(f"KEY: {key}, VALUE: {value}")
            assert key in states and isinstance(value, int) and value >= 0, f"Initial weight function should contain pairs: state, weight"
        for key, value in final_weight_function.items():
            assert key in states and isinstance(value, int) and value >= 0, f"Final weight function should contain pairs: state, weight"
        for (old_state, letter) in transitions:
            weight, new_state=transitions[(old_state, letter)]
            assert old_state in states, f"invalid old state number: {old_state} in transition"
            assert new_state in states, f"invalid new state number: {new_state} in transition"
            assert letter in alphabet, f"invalid letter: {letter} in transition"
        self.states=states
        self.alphabet = alphabet
        self.initial_weight_function = initial_weight_function
        self.final_weight_function = final_weight_function
        self.transitions = transitions

    #TODO: Porozmawiac z JMi na temat tej funkcji
    def is_equal_to(self, other, limit=500):
        for i in range(5000):
            len=random.randint(0, limit)
            word=''.join(random.choices(self.alphabet, k=len))
            #print(f"I: {i}")
            #print(f"Len: {len}, word: {word}")
            if self.weight_of_word(word) != other.weight_of_word(word):
                return False, word
        return True, ""

    def get_path_weights_from_given_state(self, state, word):
        res=[self.initial_weight_function[state]]
        actual_state=state
        for w in word:
            weight, new_state=self.transitions[(actual_state, w)]
            res.append(weight)
            actual_state=new_state
        res.append(self.final_weight_function[actual_state])
        return res

    def weight_of_word_from_given_state(self, state, word):
        path=self.get_path_weights_from_given_state(state, word)
        return product_modulo_n(path, 1000000000000)

    def weight_of_word(self, word):
        res=0
        for state in self.states:
            res = (res + self.weight_of_word_from_given_state(state, word)) % 1000000000000
        return res

    def give_state_and_weight_when_starting_from_given_configuration(self, state, word):
        actual = state
        for w in word:
            _, new_state=self.transitions[(actual, w)]
            actual = new_state
        return actual, self.weight_of_word_from_given_state(state, word)

class Weighted_Automata:
    def __init__(self, alphabet, states, initial_weight_function, final_weight_function, transitions):
        for key, value in initial_weight_function.items():
            assert key in states and isinstance(value, int) and value >= 0
        for key, value in final_weight_function.items():
            assert key in states and isinstance(value, int) and value >= 0
        self.states=states
        self.alphabet = alphabet
        self.initial_weight_function = initial_weight_function
        self.final_weight_function = final_weight_function
        self.transitions = {}
        for (old_state, letter, weight, new_state) in transitions:
            old_state = int(old_state) if isinstance(old_state, str) else old_state
            new_state = int(new_state) if isinstance(new_state, str) else new_state
            if letter == "eps":
                letter = ""
            assert old_state in states, f"invalid old state number: {old_state} in transition"
            assert new_state in states, f"invalid new state number: {new_state} in transition"
            assert isinstance(weight, int) and weight >= 0
            assert letter in alphabet, f"invalid letter: {letter} in transition"
            if not old_state in self.transitions.keys():
                self.transitions[old_state] = []
            self.transitions[old_state].append((letter, weight, new_state))

    def get_transitions_from_state(self, state):
        return self.transitions[state] if state in self.transitions.keys() else []

    def is_equal_to(self, other, limit=500):
        for i in range(5000):
            len=random.randint(0, limit)
            word=''.join(random.choices(self.alphabet, k=len))
            print(f"I: {i}")
            #print(f"Len: {len}, word: {word}")
            if self.weight_of_word(word) != other.weight_of_word(word):
                return False
        return True
    
    def get_all_paths_weights_from_given_state(self, state, word):
        def get_paths_weights_from_given_state(state, word):
            if word == "":
                return [[self.final_weight_function[state]]]
            transitions = self.get_transitions_from_state(state)
            res = []
            for (letter, weight, new_state) in transitions:
                if letter == word[0]:
                    res += [[weight] + path for path in get_paths_weights_from_given_state(new_state, word[1:])]
            return res
        return [[self.initial_weight_function[state]] + path for path in get_paths_weights_from_given_state(state, word)]

    def get_weights_of_paths_from_given_state(self, state, word):
        paths=self.get_all_paths_weights_from_given_state(state, word)
        res=[]
        for path in paths:
            #print("Debug1")
            res.append(product_modulo_n(path, 1000000000000))
        return res
    
    def weight_of_word_from_given_state(self, state, word):
        return sum_modulo_n(self.get_weights_of_paths_from_given_state(state, word), 1000000000000)

    def weight_of_word(self, word):
        res=0
        for state in self.states:
            print("Debug")
            res = (res + self.weight_of_word_from_given_state(state, word)) % 1000000000000
        return res

    def get_possible_moves(self, state, input):
        possible_transitions=self.get_transitions_from_state(state)
        possible_moves=[]
        for transition in possible_transitions:
            (letter, _, new_state) = transition
            state_after_transition = new_state
        
            input_after_transition = ""
            if len(input) > 0 and input[0] == letter:
                input_after_transition = input[1:]
            else:
                continue

            possible_moves.append((state_after_transition, input_after_transition))
        return possible_moves

    #Generate all states in which automata can finish from given state and input
    def generate_all_configs_from_given_configuration(self, state, input):

        if input == "":
            return [state]

        all_configs=[]

        moves=self.get_possible_moves(state, input)
        
        for move in moves:
            all_configs += self.generate_all_configs_from_given_configuration(move[0], move[1])  
        return all_configs

    #As above, but with duplicates removing
    def give_states_when_starting_from_given_configuration(self, state, input):
        return list(dict.fromkeys(self.generate_all_configs_from_given_configuration(state, input)))

'''
dweighted = DWeighted_Automata(["a", "b"], [0, 1, 2, 3], {0 : 3, 1 : 5, 2 : 7, 3: 11}, {0 : 2, 1 : 6, 2 : 4, 3 : 1},
        {(0, "a") : (7, 1), (0, "b") : (5, 2), (1, "a") : (8, 0), (1, "b") : (6, 3), 
            (2, "a") : (3, 3), (2, "b") : (2, 0), (3, "a") : (11, 2), (3, "b") : (9, 1)})
dweighted2 = DWeighted_Automata(["a", "b"], [0, 1, 2, 3], {0 : 3, 1 : 5, 2 : 7, 3: 11}, {0 : 2, 1 : 6, 2 : 4, 3 : 1},
        {(0, "a") : (7, 1), (0, "b") : (6, 2), (1, "a") : (8, 0), (1, "b") : (6, 3), 
            (2, "a") : (3, 3), (2, "b") : (2, 0), (3, "a") : (11, 2), (3, "b") : (9, 1)})
dweighted3 = DWeighted_Automata(["a", "b"], [0, 1, 2, 3], {0 : 8, 1 : 5, 2 : 7, 3: 11}, {0 : 2, 1 : 6, 2 : 4, 3 : 1},
        {(0, "a") : (7, 1), (0, "b") : (5, 2), (1, "a") : (8, 0), (1, "b") : (6, 3), 
            (2, "a") : (3, 3), (2, "b") : (2, 0), (3, "a") : (11, 2), (3, "b") : (9, 1)})
dweighted4 = DWeighted_Automata(["a", "b"], [0, 1, 2, 3], {0 : 3, 1 : 5, 2 : 7, 3: 11}, {0 : 2, 1 : 6, 2 : 7, 3 : 1},
        {(0, "a") : (7, 1), (0, "b") : (5, 2), (1, "a") : (8, 0), (1, "b") : (6, 3), 
            (2, "a") : (3, 3), (2, "b") : (2, 0), (3, "a") : (11, 2), (3, "b") : (9, 1)})

print(dweighted.is_equal_to(dweighted))
print(dweighted.is_equal_to(dweighted2))
print(dweighted.is_equal_to(dweighted3))
print(dweighted.is_equal_to(dweighted4))
print(dweighted2.is_equal_to(dweighted3))
print(dweighted2.is_equal_to(dweighted4))
print(dweighted3.is_equal_to(dweighted4))
print("---------------------------")

print(dweighted.get_path_weights_from_given_state(0, "abbbaaabbbaaabababab"))
print(dweighted.get_path_weights_from_given_state(1, "abbbaaabbbaaabababab"))
print(dweighted.get_path_weights_from_given_state(2, "abbbaaabbbaaabababab"))
print(dweighted.get_path_weights_from_given_state(3, "abbbaaabbbaaabababab"))
print(dweighted.weight_of_word_from_given_state(0, "abbbaaabbbaaabababab"))
print(dweighted.weight_of_word_from_given_state(1, "abbbaaabbbaaabababab"))
print(dweighted.weight_of_word_from_given_state(2, "abbbaaabbbaaabababab"))
print(dweighted.weight_of_word_from_given_state(3, "abbbaaabbbaaabababab"))
print(dweighted.weight_of_word("abbbaaabbbaaabababab"))
print(dweighted.give_state_when_starting_from_given_configuration(0, "abbbaaabbbaaabababab"))
print(dweighted.give_state_when_starting_from_given_configuration(1, "abbbaaabbbaaabababab"))
print(dweighted.give_state_when_starting_from_given_configuration(2, "abbbaaabbbaaabababab"))
print(dweighted.give_state_when_starting_from_given_configuration(3, "abbbaaabbbaaabababab"))


weighted = Weighted_Automata(["a", "b"], [0, 1], {0 : 3, 1 : 5}, {0 : 1, 1 : 4},
        [(0, "a", 7, 0), (0, "b", 0, 0), (0, "b", 4, 1), (1, "a", 10, 0), (1, "b", 16, 0)])
weighted2 = Weighted_Automata(["a", "b"], [0, 1], {0 : 3, 1 : 5}, {0 : 1, 1 : 4},
        [(0, "a", 8, 0), (0, "b", 0, 0), (0, "b", 4, 1), (1, "a", 10, 0), (1, "b", 16, 0)])
weighted3 = Weighted_Automata(["a", "b"], [0, 1], {0 : 3, 1 : 7}, {0 : 1, 1 : 4},
        [(0, "a", 7, 0), (0, "b", 0, 0), (0, "b", 4, 1), (1, "a", 10, 0), (1, "b", 16, 0)])
weighted4 = Weighted_Automata(["a", "b"], [0, 1], {0 : 3, 1 : 5}, {0 : 2, 1 : 4},
        [(0, "a", 7, 0), (0, "b", 0, 0), (0, "b", 4, 1), (1, "a", 10, 0), (1, "b", 16, 0)])
print(weighted.is_equal_to(weighted))
print(weighted.is_equal_to(weighted2))
print(weighted.is_equal_to(weighted3))
print(weighted.is_equal_to(weighted4))
print(weighted2.is_equal_to(weighted3))
print(weighted2.is_equal_to(weighted4))
print(weighted3.is_equal_to(weighted4))
print(weighted.get_all_paths_weights_from_given_state(0, "abbbaaabbbaaabababab"))
print(weighted.get_all_paths_weights_from_given_state(1, "abbbaaabbbaaabababab"))
print(weighted.get_weights_of_paths_from_given_state(0, "abbbaaabbbaaabababab"))
print(weighted.get_weights_of_paths_from_given_state(1, "abbbaaabbbaaabababab"))
print(weighted.weight_of_word_from_given_state(0, "abbbaaabbbaaabababab"))
print(weighted.weight_of_word_from_given_state(1, "abbbaaabbbaaabababab"))
print(weighted.weight_of_word("abbbaaabbbaaabababab"))
print(weighted.give_states_when_starting_from_given_configuration(0, "abbbaaabbbaaabababab"))
print(weighted.give_states_when_starting_from_given_configuration(1, "abbbaaabbbaaabababab"))
'''