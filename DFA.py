from itertools import chain, combinations
from turtle import st

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

    def find_word_in_language(self, actual_state, reachable, visited_states):
        if actual_state == self.initial_state:
            return ""
        for state in self.states:
            if state not in visited_states and state in reachable:
                for letter in self.alphabet:
                    if self.transitions[(state, letter)] == actual_state:
                        return self.find_word_in_language(state, reachable, visited_states + [actual_state]) + letter

    def have_empty_language(self):
        reachable=self.get_all_reachable_states()
        for state in reachable:
            if state in self.final_states:
                word = self.find_word_in_language(state, reachable, [])
                return False, word
        return True, ""

    #Checking if two automatas are equal
    def is_equal_to(self, other):
        is_empty, word = self.take_intersection(other.take_complement()).have_empty_language()
        if not is_empty:
            return False, word
        is_empty, word = other.take_intersection(self.take_complement()).have_empty_language()
        if not is_empty:
            return False, word
        return True, ""

    def to_NFA(self):
        transitions=[]
        for key, new_state in self.transitions.items():
            (old_state, letter) = key
            transitions.append((old_state, letter, new_state))
        return NFA(self.alphabet, self.states, self.initial_state, self.final_states, transitions)

class NFA:
    def __init__(self, alphabet, states, initial_state, final_states, transitions):
        assert initial_state in states,  f"invalid initial state number: {initial_state}"
        for state in final_states:
            assert state in states, f"invalid final state number: {state}"
        self.states=states
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.final_states = final_states
        self.transitions = {}
        for (old_state, letter, new_state) in transitions:
            old_state = int(old_state) if isinstance(old_state, str) else old_state
            new_state = int(new_state) if isinstance(new_state, str) else new_state
            if letter == "eps":
                letter = ""
            assert old_state in states, f"invalid old state number: {old_state} in transition"
            assert new_state in states, f"invalid new state number: {new_state} in transition"
            assert letter in alphabet, f"invalid letter: {letter} in transition"
            if not old_state in self.transitions.keys():
                self.transitions[old_state] = []
            self.transitions[old_state].append((letter, new_state))

    def get_transitions_from_state(self, state):
        return self.transitions[state] if state in self.transitions.keys() else []

    def create_transitions(self, states):
        transitions={}
        for state in states:
            for letter in self.alphabet:
                new_state=[]
                for st in state:
                    transis=self.get_transitions_from_state(st)
                    for trans in transis:
                        (new_letter, new_st)=trans
                        if new_st not in new_state and new_letter == letter:
                            new_state.append(new_st)
                transitions[(state, letter)] = tuple(new_state)
        return transitions

    def to_DFA(self):
        states=list(chain.from_iterable(combinations(self.states, r) for r in range(len(self.states)+1)))
        initial=(self.initial_state,)
        final_states=[state for state in states if any(st in self.final_states for st in state)]
        transitions=self.create_transitions(states)
        return DFA(self.alphabet, states, initial, final_states, transitions)

    def take_complement(self):
        dfa_from_nfa = self.to_DFA()
        return dfa_from_nfa.take_complement().to_NFA()

    def take_intersection(self, other):
        assert self.alphabet == other.alphabet, "Alphabets of intersected automatas should be the same."
        states = []
        initial_state=(self.initial_state, other.initial_state)
        finals=[]
        transitions=[]
        for our_state in self.states:
            for other_state in other.states:
                states.append((our_state, other_state))
                if our_state in self.final_states and other_state in other.final_states:
                    finals.append((our_state, other_state))
                our_transitions=self.get_transitions_from_state(our_state)
                other_transitions=other.get_transitions_from_state(other_state)
                for our_trans in our_transitions:
                    for other_trans in other_transitions:
                        (our_letter, our_new_state) = our_trans
                        (other_letter, other_new_state) = other_trans
                        if our_letter != other_letter:
                            continue
                        transitions.append(((our_state, other_state), our_letter, (our_new_state, other_new_state)))
        return NFA(self.alphabet, states, initial_state, finals, transitions)

    def get_all_reachable_states(self):
        reachable=[self.initial_state]
        for _ in range(len(self.states)):
            for state in reachable:
                transitions=self.get_transitions_from_state(state)
                for trans in transitions:
                    _, new_state=trans
                    if new_state not in reachable:
                        reachable.append(new_state)
        return reachable

    def find_word_in_language(self, actual_state, reachable, visited_states):
        if actual_state == self.initial_state:
            return ""
        for state in self.states:
            if state not in visited_states and state in reachable:
                for letter in self.alphabet:
                    if (letter, actual_state) in self.transitions[state]:
                        return self.find_word_in_language(state, reachable, visited_states + [actual_state]) + letter

    def have_empty_language(self):
        reachable=self.get_all_reachable_states()
        for state in reachable:
            if state in self.final_states:
                word = self.find_word_in_language(state, reachable, [])
                return False, word
        return True, ""
    
    #Checking if two automatas are equal
    def is_equal_to(self, other):
        is_empty, word = self.take_intersection(other.take_complement()).have_empty_language()
        if not is_empty:
            return False, word
        is_empty, word = other.take_intersection(self.take_complement()).have_empty_language()
        if not is_empty:
            return False, word
        return True, ""

    #Check if given trial is accepting
    def is_accepting(self, state, input):
        return len(input) == 0 and state in self.final_states

    #Get all possible moves from given configuration
    def get_possible_moves(self, state, input):
        possible_transitions=self.get_transitions_from_state(state)
        possible_moves=[]
        for transition in possible_transitions:
            (letter, new_state) = transition
            state_after_transition = new_state
        
            input_after_transition = ""
            if len(letter) == 0:
               input_after_transition = input
            elif len(input) > 0 and input[0] == letter:
                input_after_transition = input[1:]
            else:
                continue

            possible_moves.append((state_after_transition, input_after_transition))
        return possible_moves

    #Count how many accepting configs we can have with given input and state
    def generate_all_accepting_configs(self, state, input):
        total_num_of_accepting_configs=0
        if self.found_accepting_configs_in_subtrees:
            return 0
        if self.is_accepting(state, input):
            self.found_accepting_configs_in_subtrees=True
            return 1
        moves=self.get_possible_moves(state, input)
        for move in moves:
            total_num_of_accepting_configs += self.generate_all_accepting_configs(move[0], move[1])
        return total_num_of_accepting_configs
    
    #Check if automata accepts given word
    def check_if_word_in_language(self, word):
        self.found_accepting_configs_in_subtrees=False
        total=self.generate_all_accepting_configs(self.initial_state, word)
        return total > 0

    #Generate all states in which automata can finish from given state and input
    def generate_all_configs_from_given_configuration(self, state, input):
        all_configs=[]

        if input == "":
            all_configs=[state]
            for old_state, transitions in self.transitions.items():
                if old_state == state: 
                    for transition in transitions:
                        if len(transition[0]) == 0:
                            all_configs.append(transition[1])
            return all_configs

        moves=self.get_possible_moves(state, input)
        if len(moves) == 0:
            return [state] if len(input) == 0 else []
        
        for move in moves:
            all_configs += self.generate_all_configs_from_given_configuration(move[0], move[1])  
        return all_configs
    
    #As above, but with duplicates removing
    def give_states_when_starting_from_given_configuration(self, state, input):
        return list(dict.fromkeys(self.generate_all_configs_from_given_configuration(state, input)))
