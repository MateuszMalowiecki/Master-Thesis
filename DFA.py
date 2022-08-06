from itertools import chain, combinations

class DFA:
    def __init__(self, alphabet, states, initial_state, final_states, transitions):
        assert initial_state in states, f"invalid initial state number: {initial_state}"
        for state in final_states:
            assert state in states, f"invalid final state number: {state}"
        for (old_state, letter) in transitions:
            new_state=transitions[(old_state, letter)]
            assert old_state in states, f"invalid old state number: {old_state} in transition"
            assert new_state in states, f"invalid new state number: {new_state} in transition"
            assert letter in alphabet, f"invalid letter: {letter} in transition"
        self.alphabet = alphabet
        self.states=states
        self.initial_state = initial_state
        self.final_states = final_states
        self.transitions = transitions

    #Check if automaton accepts given word
    def check_if_word_in_language(self, word):
        actual=self.initial_state
        for w in word:
            actual=self.transitions[(actual, w)]
        return actual in self.final_states

    #Give state in which automaton will finish from given state and input
    def give_state_when_starting_from_given_configuration(self, state, word):
        actual = state
        for w in word:
            actual=self.transitions[(actual, w)]
        return actual
    
    def take_complement(self):
        return DFA(self.alphabet, self.states, self.initial_state, 
            [state for state in self.states if state not in self.final_states], self.transitions)

    def take_intersection(self, other):
        assert self.alphabet == other.alphabet, "Alphabets of intersected automata should be the same."
        states=[]
        final_states=[]
        transitions={}
        for our_state in self.states:
            for other_state in other.states:
                states.append((our_state, other_state))
                if our_state in self.final_states and other_state in other.final_states:
                    final_states.append((our_state, other_state))
                for letter in self.alphabet:
                    transitions[((our_state, other_state), letter)] = (self.transitions[(our_state, letter)], other.transitions[(other_state, letter)])
        return DFA(self.alphabet, states, (self.initial_state, other.initial_state), final_states, transitions)

    def get_all_reachable_states(self):
        reachable=[self.initial_state]
        for _ in range(len(self.states)):
            for state in reachable:
                for letter in self.alphabet:
                    new_state=self.transitions[(state,letter)]
                    if new_state not in reachable:
                        reachable.append(new_state)
        return reachable

    def find_word_in_language(self, actual_state, reachable, visited_states):
        if actual_state == self.initial_state:
            return ""
        for state in self.states:
            if state not in visited_states and state in reachable:
                for letter in self.alphabet:
                    if self.transitions[(state, letter)] == actual_state:
                        subword = self.find_word_in_language(state, reachable, visited_states + [actual_state])
                        if subword is not None:
                            return subword + letter

    def have_empty_language(self):
        reachable=self.get_all_reachable_states()
        for state in reachable:
            if state in self.final_states:
                word = self.find_word_in_language(state, reachable, [])
                return False, word
        return True, ""

    #Checking if two automata are equal
    def is_equal_to(self, other):
        is_empty, word = self.take_intersection(other.take_complement()).have_empty_language()
        if not is_empty:
            return False, word
        is_empty, word = other.take_intersection(self.take_complement()).have_empty_language()
        if not is_empty:
            return False, word
        return True, ""
