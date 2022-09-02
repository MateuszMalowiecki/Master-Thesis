from DFA import DFA
from VPA import DVPA
from Weighted import DWFA
import random

class Automata_generator:
    def generate_random_dfa(self, alphabet, min_limit, max_limit):
        number_of_states = random.randint(min_limit, max_limit)
        states = list(range(number_of_states))
        num_of_finals = 0
        if number_of_states >= 2:
            num_of_finals = random.randint(1, number_of_states - 1)
        else:
            num_of_finals = random.randint(0, 1)
        final_states = random.sample(states, num_of_finals)
        transitions = {}
        while True:
            transitions = self.generate_dfa_transitions(alphabet, states)
            dfa = DFA(alphabet, states, 0, final_states, transitions)
            if len(dfa.get_all_reachable_states()) == number_of_states:
                return dfa

    def generate_dfa_transitions(self, alphabet, states):
        transitions = {}
        number_of_states = len(states)
        for state in states:
            for letter in alphabet:
                transitions[(state, letter)] = random.randint(0, number_of_states - 1)
        return transitions

    def generate_random_dvpa(self, calls_alphabet, return_alphabet, internal_alpahbet, stack_alphabet, min_limit, max_limit):
        number_of_states = random.randint(min_limit, max_limit)
        states = list(range(number_of_states))
        if number_of_states >= 2:
            num_of_finals = random.randint(1, number_of_states - 1)
        else:
            num_of_finals = random.randint(0, 1)
        final_states = random.sample(states, num_of_finals)
        transitions = {}
        while True:
            transitions = self.generate_dvpa_transitions(calls_alphabet, return_alphabet, internal_alpahbet, states, stack_alphabet)
            dvpa = DVPA(calls_alphabet, return_alphabet, internal_alpahbet, states, stack_alphabet, 0, final_states, stack_alphabet[0], transitions)
            if len(dvpa.get_all_reachable_states()) == number_of_states:
                return dvpa

    def generate_dvpa_transitions(self, calls_alphabet, return_alphabet, internal_alpahbet, states, stack_alphabet):
        transitions = {}
        number_of_states = len(states)
        for state in states:
            for letter in calls_alphabet:
                transitions[(state, letter)] = (random.randint(0, number_of_states - 1), stack_alphabet[random.randint(1, len(stack_alphabet) - 1)])
            for letter in return_alphabet:
                for stack_letter in stack_alphabet:
                    transitions[(state, letter, stack_letter)] = random.randint(0, number_of_states - 1)
            for letter in internal_alpahbet:
                transitions[(state, letter)] = random.randint(0, number_of_states - 1)
        return transitions

    def generate_random_dwfa(self, alphabet, max_weight, min_limit, max_limit):
        number_of_states = random.randint(min_limit, max_limit)
        states = list(range(number_of_states))
        final_weight_function = {}
        transitions = {}
        for state in states:
            final_weight_function[state] = random.randint(0, max_weight)
        while True:
            transitions = self.generate_dwfa_transitions(alphabet, max_weight, states)
            dwfa = DWFA(alphabet, states, 0, final_weight_function, transitions)
            if len(dwfa.get_all_reachable_states()) == number_of_states:
                return dwfa

    def generate_dwfa_transitions(self, alphabet, max_weight, states):
        transitions = {}
        number_of_states = len(states)
        for state in states:
            for letter in alphabet:
                transitions[(state, letter)] = random.randint(0, max_weight), random.randint(0, number_of_states - 1)
        return transitions
