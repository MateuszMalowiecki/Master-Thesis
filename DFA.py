import NFA

class DFA:
    def __init__(self, alphabet, states, initial_state, final_states, transitions):
        assert initial_state in states
        for state in final_states:
            assert state in states
        for (old_state, letter) in transitions:
            assert old_state in states and transitions[(old_state, letter)] in states and letter in alphabet
        self.alphabet = alphabet
        self.states=states
        self.initial_state = initial_state
        self.final_states = final_states
        self.transitions = transitions

    #Check if automata accepts given word
    def check_if_word_in_language(self, word):
        actual=self.initial_state
        for w in word:
            actual=self.transitions[(actual, w)]
        return actual in self.final_states

    #Give state in which automata will finish from given state and input
    def give_state_when_starting_from_given_configuration(self, state, word):
        actual = state
        for w in word:
            actual=self.transitions[(actual, w)]
        return actual
    
    def take_complement(self):
        return DFA(self.alphabet, self.states, self.initial_state, 
            [state for state in self.states if state not in self.final_states], self.transitions)
    
    def take_intersection(self, other):
        assert self.alphabet == other.alphabet, "Alphabets of intersected automatas should be the same."
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
        for i in range(len(self.states)):
            for state in reachable:
                for letter in self.alphabet:
                    new_state=self.transitions[(state,letter)]
                    if new_state not in reachable:
                        reachable.append(new_state)
        return reachable
    def have_empty_language(self):
        reachable=self.get_all_reachable_states()
        return len([state for state in self.final_states if state in reachable]) == 0
    #Checking if two automatas are equal
    def is_equal_to(self, other):
        return self.take_intersection(other.take_complement()).have_empty_language() and \
            other.take_intersection(self.take_complement()).have_empty_language()
    def to_NFA(self):
        transitions=[]
        for key, new_state in self.transitions.items():
            (old_state, letter) = key
            transitions.append((old_state, letter, new_state))
        return NFA(self.alphabet, self.states, self.initial_state, self.final_states, transitions)

dfa=DFA(["a", "b"], [0, 1, 2, 3], 0, [3], {(0, "a") : 1, (0, "b") : 1, (1, "a") : 2, (1, "b") : 2, 
        (2, "a") : 3, (2, "b") : 3, (3, "a") : 3, (3, "b") : 3})
second_dfa=DFA(["a", "b"], [0, 1, 2, 3], 3, [0], {(3, "a") : 2, (3, "b") : 2, (2, "a") : 1, (2, "b") : 1, 
        (1, "a") : 0, (1, "b") : 0, (0, "a") : 0, (0, "b") : 0})
#print(dfa.take_intersection(second_dfa).states)
#print(dfa.take_intersection(second_dfa).)
#print(dfa.take_intersection(second_dfa).final_states)
print(dfa.is_equal_to(second_dfa))