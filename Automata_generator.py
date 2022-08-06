from DFA import DFA
from VPA import DVPA
from Weighted import DWFA
import random

class Automata_generator:
    def generate_random_dfa(self, alphabet, min_limit, max_limit):
        number_of_states = random.randint(min_limit, max_limit)
        states = list(range(number_of_states))
        num_of_finals = random.randint(0, number_of_states - 1)
        final_states = random.sample(states, num_of_finals)
        transitions = {}
        for state in states:
            for letter in alphabet:
                transitions[(state, letter)] = random.randint(0, number_of_states - 1)
        return DFA(alphabet, states, 0, final_states, transitions)

    def generate_random_dvpa(self, calls_alphabet, return_alphabet, internal_alpahbet, stack_alphabet, min_limit, max_limit):
        number_of_states = random.randint(min_limit, max_limit)
        states = list(range(number_of_states))
        num_of_finals = random.randint(0, number_of_states - 1)
        final_states = random.sample(states, num_of_finals)
        transitions = {}
        for state in states:
            for letter in calls_alphabet:
                transitions[(state, letter)] = (random.randint(0, number_of_states - 1), stack_alphabet[random.randint(1, len(stack_alphabet) - 1)])
            for letter in return_alphabet:
                for stack_letter in stack_alphabet:
                    transitions[(state, letter, stack_letter)] = random.randint(0, number_of_states - 1)
            for letter in internal_alpahbet:
                transitions[(state, letter)] = random.randint(0, number_of_states - 1)            
        return DVPA(calls_alphabet, return_alphabet, internal_alpahbet, states, stack_alphabet, 0, final_states, stack_alphabet[0], transitions)

    def generate_random_dwfa(self, alphabet, max_weight, min_limit, max_limit):
        number_of_states = random.randint(min_limit, max_limit)
        states = list(range(number_of_states))
        initial_weight_function = {}
        final_weight_function = {}
        transitions = {}
        for state in states:
            initial_weight_function[state] = random.randint(0, max_weight)
            final_weight_function[state] = random.randint(0, max_weight)
            for letter in alphabet:
                transitions[(state, letter)] = random.randint(0, max_weight), random.randint(0, number_of_states - 1)
        return DWFA(alphabet, states, initial_weight_function, final_weight_function, transitions)
