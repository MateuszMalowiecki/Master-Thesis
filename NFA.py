from itertools import chain, combinations
import DFA

class NFA:
    def __init__(self, alphabet, states, initial_state, final_states, transitions):
        assert initial_state in states
        for state in final_states:
            assert state in states
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.final_states = final_states
        self.transitions = {}
        for (old_state, letter, new_state) in transitions:
            old_state = int(old_state)
            new_state = int(new_state)
            if letter == "eps":
                letter = ""
            assert old_state in states and new_state in states and letter in alphabet
            if not old_state in self.transitions.keys():
                self.transitions[old_state] = []
            self.transitions[old_state].append((letter, new_state))
    def to_DFA(self):
        states=list(chain.from_iterable(combinations(self.states, r) for r in range(len(self.states)+1)))
        initial=[(self.initial_state,)]
        final_states=[state for state in states if any(st in self.final_states for st in state)]
        transitions={}
        for state in states:
            for letter in self.alphabet:
                new_state=[]
                for st in states:
                    for trans in self.transitions[st]:
                        (_, new_st)=trans
                        if new_st not in new_state:
                            new_state.append(new_st)
                transitions[(state, letter)] = tuple(new_state)
        return DFA(self.alphabet, states, initial, final_states, transitions)

    def take_complement(self):
        dfa_from_nfa = self.to_DFA()
        return dfa_from_nfa.take_complement.toNFA()

    def take_intersection(self, other):
        assert self.alphabet == other.alphabet
        states = []
        initial_state=(self.initial_state, other.initial_state)
        finals=[]
        transitions=[]
        for our_state in self.states:
            for other_state in other.states:
                states.append((our_state, other_state))
                if our_state in self.final_states and other_state in other.final_states:
                    finals.append((our_state, other_state))
                our_transitions=self.transitions[our_state] if our_state in self.transitions.keys() else []
                other_transitions=other.transitions[other_state] if other_state in other.transitions.keys() else []
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
                transitions=self.transitions[state] if state in self.transitions.keys() else []
                for trans in transitions:
                    _, new_state=trans
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

    #Check if given trial is accepting
    def is_accepting(self, state, input):
        return len(input) == 0 and state in self.final_states

    #Get all possible moves from given configuration
    def get_possible_moves(self, state, input):
        possible_transitions=self.transitions[state] if state in self.transitions.keys() else []
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

s=(1,2,3)
print(any(e <= 1 for e in s))
#print(list(chain.from_iterable(combinations(s, r) for r in range(len(s)+1))))