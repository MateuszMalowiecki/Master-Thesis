#With help of: https://github.com/theodoregold/pushdown-automata/blob/3ce36cdfdd1f4e260121fb43dea988b96288fed0/main.py#L36
from inspect import stack
from typing_extensions import final
from itertools import chain, combinations

from urllib3 import Retry

class DVPA:
    def __init__(self, calls_alphabet, return_alphabet, internal_alpahbet, states, stack_alphabet, initial_state, final_states, initial_stack_symbol, transitions):
        assert initial_state in states, f"invalid initial state number: {initial_state}"
        for state in final_states:
            assert state in states, f"invalid final state number: {state}"
        assert initial_stack_symbol in stack_alphabet, f"invalid initial stack symbol: {initial_stack_symbol}"
        self.calls_alphabet = calls_alphabet
        self.return_alphabet = return_alphabet
        self.internal_alpahbet = internal_alpahbet
        self.states=states
        self.stack_alphabet=stack_alphabet
        self.initial_state = initial_state
        self.final_states = final_states
        self.initial_stack_symbol= initial_stack_symbol
        self.transitions = transitions
        for key, value in transitions.items():
            if len(key) == 2 and key[1] in calls_alphabet:
                assert len(value) == 2, f"invalid transtion: {key} -> {value}"
                (old_state, _) = key
                (new_state, new_stack_letter) = value
                assert old_state in states, f"invalid old state number: {old_state} in call transition"
                assert new_state in states, f"invalid new state number: {new_state} in call transition"
                assert new_stack_letter in stack_alphabet, f"invalid new stack letter: {new_stack_letter} in call transition"
                assert new_stack_letter != initial_stack_symbol, f"initial stack symbol should not be pushed into stack"
            elif len(key) == 2 and key[1] in internal_alpahbet:
                (old_state, _) = key
                new_state=value
                assert old_state in states, f"invalid old state number: {old_state} in internal transition" 
                assert new_state in states, f"invalid new state number: {new_state} in internal transition"
            elif len(key) == 3 and key[1] in return_alphabet:
                (old_state, _, old_stack_top) = key
                new_state=value
                assert old_state in states, f"invalid old state number: {old_state} in return transition" 
                assert new_state in states, f"invalid new state number: {new_state} in return transition"
                assert old_stack_top in stack_alphabet, f"invalid old stack top: {old_stack_top} in return transition"
            else:
                if key[1] not in calls_alphabet and key[1] not in return_alphabet and key[1] not in internal_alpahbet:
                    assert False, f"letter {key[1]} does not belong to any alphabet"
                assert False, f"invalid transtion: {key} -> {value}"
    
    def check_if_word_in_language(self, word):
        actual_state=self.initial_state
        actual_stack=[self.initial_stack_symbol]
        for w in word:
            try:
                new_state=actual_state
                new_stack=actual_stack
                if w in self.internal_alpahbet:
                    new_state=self.transitions[(actual_state, w)]
                elif w in self.calls_alphabet:
                    new_state, new_stack_top=self.transitions[(actual_state, w)]
                    new_stack = [new_stack_top] + actual_stack
                else:
                    actual_stack_top = actual_stack[0]
                    if actual_stack_top != self.initial_stack_symbol:
                        new_stack = new_stack[1:]
                    new_state=self.transitions[(actual_state, w, actual_stack_top)]
                actual_state=new_state
                actual_stack=new_stack
            except:
                return False
        return actual_state in self.final_states

    #As above, but with duplicates removing
    def give_state_and_stack_when_starting_from_given_configuration(self, state, input, stack):
        actual_state = state
        actual_stack = stack
        for w in input:
            try:
                new_state=actual_state
                new_stack=actual_stack
                if w in self.internal_alpahbet:
                    new_state=self.transitions[(actual_state, w)]
                elif w in self.calls_alphabet:
                    new_state, new_stack_top=self.transitions[(actual_state, w)]
                    new_stack = [new_stack_top] + actual_stack
                else:
                    actual_stack_top = actual_stack[0]
                    if actual_stack_top != self.initial_stack_symbol:
                        new_stack = new_stack[1:]
                    new_state=self.transitions[(actual_state, w, actual_stack_top)]
                actual_state=new_state
                actual_stack=new_stack
            except:
                return None
        return actual_state, actual_stack

    # Changing dvpa to vpa
    def to_VPA(self):
        transitions=[]
        for key, value in self.transitions.items():
            if len(key) == 2 and isinstance(value, tuple):
                (old_state, old_letter) = key
                (new_state, new_stack_letter) = value
                transitions.append((old_state, old_letter, new_state, new_stack_letter))
            elif len(key) == 2:
                (old_state, old_letter) = key
                new_state=value
                transitions.append((old_state, old_letter, new_state, ""))
            elif len(key) == 3:
                (old_state, old_letter, old_stack_top) = key
                new_state=value
                transitions.append((old_state, old_letter, new_state, old_stack_top))
        return VPA(self.calls_alphabet, self.return_alphabet, self.internal_alpahbet, self.states, 
            self.stack_alphabet, [self.initial_state], self.final_states, 
            self.initial_stack_symbol, transitions)

    def take_complement(self):
        return DVPA(self.calls_alphabet, self.return_alphabet, self.internal_alpahbet, self.states, 
            self.stack_alphabet, self.initial_state, [state for state in self.states if state not in self.final_states], 
            self.initial_stack_symbol, self.transitions)

    def take_intersection(self, other):
        assert self.calls_alphabet == other.calls_alphabet, "Calls alphabets of intersected automata should be the same."
        assert self.return_alphabet == other.return_alphabet, "Return alphabets of intersected automata should be the same."
        assert self.internal_alpahbet == other.internal_alpahbet, "Internal alphabets of intersected automata should be the same."
        stack_alphabet=[]
        for our_stack_letter in self.stack_alphabet:
            for other_stack_letter in other.stack_alphabet:
                stack_alphabet.append((our_stack_letter, other_stack_letter))
        initial_stack_symbol = ((self.initial_stack_symbol, other.initial_stack_symbol))
        states = []
        initial_state=(self.initial_state, other.initial_state)
        finals=[]
        transitions={}
        for our_state in self.states:
            for other_state in other.states:
                states.append((our_state, other_state))
                if our_state in self.final_states and other_state in other.final_states:
                    finals.append((our_state, other_state))

                for letter in self.internal_alpahbet:
                    transitions[((our_state, other_state), letter)] = (self.transitions[(our_state, letter)], other.transitions[(other_state, letter)])

                for letter in self.calls_alphabet:
                    (our_new_state, our_new_letter) = self.transitions[(our_state, letter)]
                    (other_new_state, other_new_letter) = other.transitions[(other_state, letter)]
                    transitions[((our_state, other_state), letter)] = ((our_new_state, other_new_state), (our_new_letter, other_new_letter))
                
                for letter in self.return_alphabet:
                    for our_stack_letter, other_stack_letter in stack_alphabet:
                        our_new_state = self.transitions[(our_state, letter, our_stack_letter)]
                        other_new_state = other.transitions[(other_state, letter, other_stack_letter)]
                        transitions[((our_state, other_state), letter, (our_stack_letter, other_stack_letter))] = (our_new_state, other_new_state)
        return DVPA(self.calls_alphabet, self.return_alphabet, self.internal_alpahbet, 
            states, stack_alphabet, initial_state, finals, initial_stack_symbol, transitions)

    def get_all_reachable_states(self):
        reachable=[self.initial_state]
        for i in range(len(self.states)):
            for state in reachable:
                try:
                    for letter in self.internal_alpahbet:
                        new_state=self.transitions[(state,letter)]
                        if new_state not in reachable:
                            reachable.append(new_state)
                    for letter in self.calls_alphabet:
                        (new_state, _)=self.transitions[(state,letter)]
                        if new_state not in reachable:
                            reachable.append(new_state)
                    for letter in self.return_alphabet:
                        for stack_letter in self.stack_alphabet:
                            new_state=self.transitions[(state,letter, stack_letter)]
                            if new_state not in reachable:
                                reachable.append(new_state)
                except:
                    pass
        return reachable

    def find_word_in_language(self, actual_state, reachable, visited_states):
        if actual_state == self.initial_state:
            return ""
        for state in self.states:
            if state not in visited_states and state in reachable:
                for letter in self.internal_alpahbet:
                    if self.transitions[(state, letter)] == actual_state:
                        subword = self.find_word_in_language(state, reachable, visited_states + [actual_state]) 
                        if subword is not None:
                            return subword + letter
                for letter in self.calls_alphabet:
                    if self.transitions[(state, letter)][0] == actual_state:
                        subword = self.find_word_in_language(state, reachable, visited_states + [actual_state]) 
                        if subword is not None:
                            return subword + letter
                for letter in self.return_alphabet:
                    for stack_letter in self.stack_alphabet:
                        if self.transitions[(state, letter, stack_letter)] == actual_state:
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

    def is_equal_to(self, other):
        is_empty, word = self.take_intersection(other.take_complement()).have_empty_language()
        if not is_empty:
            return False, word
        is_empty, word = other.take_intersection(self.take_complement()).have_empty_language()
        if not is_empty:
            return False, word
        return True, ""

class VPA:
    def __init__(self, calls_alphabet, return_alphabet, internal_alpahbet, states, stack_alphabet, initial_states, final_states, initial_stack_symbol, transitions):
        for state in initial_states:
            assert state in states
        for state in final_states:
            assert state in states
        assert initial_stack_symbol in stack_alphabet
        self.calls_alphabet = calls_alphabet
        self.return_alphabet = return_alphabet
        self.internal_alpahbet = internal_alpahbet
        self.states=states
        self.stack_alphabet=stack_alphabet
        self.initial_states = initial_states
        self.final_states = final_states
        self.initial_stack_symbol= initial_stack_symbol
        self.transitions = {}
        for (old_state, letter, new_state, stack_symbol) in transitions:
            if not isinstance(old_state, tuple):
                old_state = int(old_state)
            if not isinstance(new_state, tuple):
                new_state = int(new_state)
            type=""
            assert old_state in states and new_state in states
            stack_symbols = []
            if letter in internal_alpahbet:
                type = "i"
            elif letter in calls_alphabet:
                type = "c"
                assert stack_symbol in stack_alphabet and stack_symbol != initial_stack_symbol
                stack_symbols=[stack_symbol]
            elif letter in return_alphabet:
                type = "r"
                assert stack_symbol in stack_alphabet
                stack_symbols=[stack_symbol]
            else:
                assert False
            if not old_state in self.transitions.keys():
                self.transitions[old_state] = []
            self.transitions[old_state].append((letter, type, stack_symbols, new_state))

    def get_transitions_from_state(self, state):
        return self.transitions[state] if state in self.transitions.keys() else []

    def create_internal_transitions(self, state_pairs, state):
        transitions={}
        for letter in self.internal_alpahbet:
            new_state=[]
            for q in state:
                transis=self.get_transitions_from_state(q)
                for trans in transis:
                    (new_letter, _, _, new_st)=trans
                    if new_st not in new_state and new_letter == letter:
                        new_state.append(new_st)
            new_state_pairs=[]
            for (q1, q2) in state_pairs:
                transis=self.get_transitions_from_state(q2)
                for trans in transis:
                    (new_letter, _, _, new_st)=trans
                    if (q1, new_st) not in new_state_pairs and new_letter == letter:
                        new_state_pairs.append((q1, new_st))
            transitions[((state_pairs, state), letter)] = (tuple(new_state_pairs), tuple(new_state))
        return transitions

    def create_calls_transitions(self, state_pairs, state):
        transitions={}
        for letter in self.calls_alphabet:
            new_state=[]
            for q in state:
                transis=self.get_transitions_from_state(q)
                for trans in transis:
                    (new_letter, _, _, new_st)=trans
                    if new_st not in new_state and new_letter == letter:
                        new_state.append(new_st)
            transitions[((state_pairs, state), letter)] = ((tuple([(q, q) for q in self.states]), tuple(new_state)), (state_pairs, state, letter))
        return transitions

    def create_update_pairs(self, state_pairs, a1, a2):
        res=[]
        for q in self.states:
            transis=self.get_transitions_from_state(q)
            for trans in transis:
                (new_letter, _, new_stack_symbols, new_state)=trans
                if new_letter != a2:
                    continue
                for (q1, q2) in state_pairs:
                    if new_state != q1:
                        continue
                    transis2=self.get_transitions_from_state(q2)
                    for trans2 in transis2:
                        (new_letter2, _, new_stack_symbols2, new_state2)=trans2
                        if new_stack_symbols == new_stack_symbols2 and new_letter2 == a1 \
                            and (q, new_state2) not in res:
                            res.append((q, new_state2))
        return res
    
    def create_return_initial_stack_symbol_transitions(self, state_pairs, state, letter):
        transitions={}
        new_state_for_initial=[]
        new_state_pairs_for_initial=[]
        for q in state:
            transis=self.get_transitions_from_state(q)
            for trans in transis:
                (new_letter, _, stack_symbols, new_st)=trans
                if new_st not in new_state_for_initial and new_letter == letter and stack_symbols[0] == self.initial_stack_symbol:
                    new_state_for_initial.append(new_st)
        for (q1, q2) in state_pairs:
            transis=self.get_transitions_from_state(q2)
            for trans in transis:
                (new_letter, _, stack_symbols, new_st)=trans
                if (q1, new_st) not in new_state_pairs_for_initial and new_letter == letter and stack_symbols[0] == self.initial_stack_symbol:
                    new_state_pairs_for_initial.append((q1, new_st))
        transitions[((state_pairs, state), letter, self.initial_stack_symbol)] = (tuple(new_state_pairs_for_initial), tuple(new_state_for_initial))
        return transitions

    def create_return_transitions(self, state_pairs, state, stack_alphabet):
        transitions={}
        for letter in self.return_alphabet:
            for stack_letter in stack_alphabet:
                if stack_letter == 'Z':
                    continue
                (S, R, a) = stack_letter
                update=self.create_update_pairs(state_pairs, letter, a)
                new_state=[]
                new_state_pairs=[]
                for (q, q3) in update:
                    for (q4, q5) in S:
                        if q == q5 and (q3, q4) not in new_state_pairs:
                            new_state_pairs.append((q4, q3))
                    if q in R and not q3 in new_state:
                        new_state.append(q3)
                transitions[((state_pairs, state), letter, stack_letter)] = (tuple(new_state_pairs), tuple(new_state))
            transitions.update(self.create_return_initial_stack_symbol_transitions(state_pairs, state, letter))
        return transitions    
    
    def create_transitions(self, states,stack_alphabet):
        transitions={}
        for (state_pairs, state) in states:
            transitions.update(self.create_internal_transitions(state_pairs, state))
            transitions.update(self.create_calls_transitions(state_pairs, state))
            transitions.update(self.create_return_transitions(state_pairs, state, stack_alphabet))
        return transitions

    def to_DVPA(self):
        states_pairs=[(q1, q2) for q1 in self.states for q2 in self.states]
        subsets_of_states=list(chain.from_iterable(combinations(self.states, r) for r in range(len(self.states)+1)))
        subsets_of_pair_of_states=list(chain.from_iterable(combinations(states_pairs, r) for r in range(len(states_pairs)+1)))
        states=[(q1, q2) for q1 in subsets_of_pair_of_states for q2 in subsets_of_states]
        stack_alphabet=[(S, R, a) for S in subsets_of_pair_of_states for R in subsets_of_states for a in self.calls_alphabet] + [self.initial_stack_symbol]
        initial=(tuple([(q, q) for q in self.states]), tuple(self.initial_states))
        finals=[(state_pairs, state) for (state_pairs, state) in states if any(st in self.final_states for st in state)]
        initial_stack_symbol = self.initial_stack_symbol
        transitions=self.create_transitions(states, stack_alphabet)
        return DVPA(self.calls_alphabet, self.return_alphabet, self.internal_alpahbet, states, stack_alphabet, initial, finals, initial_stack_symbol, transitions)

    def take_complement(self):
        dvpa_from_vpa = self.to_DVPA()
        return dvpa_from_vpa.take_complement().to_VPA()
        
    def take_intersection(self, other):
        assert self.calls_alphabet == other.calls_alphabet
        assert self.return_alphabet == other.return_alphabet
        assert self.internal_alpahbet == other.internal_alpahbet
        stack_alphabet=[]
        for our_stack_letter in self.stack_alphabet:
            for other_stack_letter in other.stack_alphabet:
                stack_alphabet.append((our_stack_letter, other_stack_letter))
        initial_stack_symbol = ((self.initial_stack_symbol, other.initial_stack_symbol))
        states = []
        initials=[]
        finals=[]
        transitions=[]
        for our_state in self.states:
            for other_state in other.states:
                states.append((our_state, other_state))
                if our_state in self.initial_states and other_state in other.initial_states:
                    initials.append((our_state, other_state))
                if our_state in self.final_states and other_state in other.final_states:
                    finals.append((our_state, other_state))
                our_transitions=self.transitions[our_state] if our_state in self.transitions.keys() else []
                other_transitions=other.transitions[other_state] if other_state in other.transitions.keys() else []
                for our_trans in our_transitions:
                    for other_trans in other_transitions:
                        (our_letter, our_type, our_stack_symbols, our_new_state) = our_trans
                        (other_letter, other_type, other_stack_symbols, other_new_state) = other_trans
                        if our_letter != other_letter or our_type != other_type:
                            continue
                        if our_type == "i":
                            transitions.append(((our_state, other_state), our_letter, (our_new_state, other_new_state), ""))
                        else:
                            transitions.append(((our_state, other_state), our_letter, (our_new_state, other_new_state), (our_stack_symbols[0], other_stack_symbols[0])))

        return VPA(self.calls_alphabet, self.return_alphabet, self.internal_alpahbet, states, stack_alphabet, initials, finals, initial_stack_symbol, transitions)
    
    def get_all_reachable_states(self):
        reachable=self.initial_states
        for i in range(len(self.states)):
            for state in reachable:
                transitions=self.transitions[state] if state in self.transitions.keys() else []
                for trans in transitions:
                    _, _,_, new_state=trans
                    if new_state not in reachable:
                        reachable.append(new_state)
        return reachable
    
    def have_empty_language(self):
        reachable=self.get_all_reachable_states()
        return len([state for state in self.final_states if state in reachable]) == 0
    
    def is_equal_to(self, other):
        return self.take_intersection(other.take_complement()).have_empty_language() and \
            other.take_intersection(self.take_complement()).have_empty_language()
    
    #Check if given trial is accepting
    def is_accepting(self, state, input):
        return len(input) == 0 and state in self.final_states

    #Get all possible moves from given configuration
    def get_possible_moves(self, state, input, stack):
        possible_transitions=self.transitions[state] if state in self.transitions.keys() else []
        possible_moves=[]
        if len(input) == 0:
            return possible_moves
        for transition in possible_transitions:
            (letter, type, stack_symbols, new_state) = transition
            state_after_transition = new_state
        
            if input[0] != letter:
                continue
            input_after_transition = input[1:]
            
            stack_after_transition=[]
            if type=="c":
                stack_after_transition = stack_symbols + stack
            elif type=="r" and stack[0] == stack_symbols[0]:
                if stack[0] == self.initial_stack_symbol:
                    stack_after_transition = stack
                else:
                    stack_after_transition = stack[1:]
            elif type=="i":
                stack_after_transition = stack
            else:
                continue

            possible_moves.append((state_after_transition, input_after_transition, stack_after_transition))
        return possible_moves

    #Count how many accepting configs we can have with given input and state
    def generate_all_accepting_configs(self, state, input, stack):
        total_num_of_accepting_configs=0
        if self.found_accepting_configs_in_subtrees:
            return 0
        if self.is_accepting(state, input):
            self.found_accepting_configs_in_subtrees=True
            return 1
        moves=self.get_possible_moves(state, input, stack)
        for move in moves:
            total_num_of_accepting_configs += self.generate_all_accepting_configs(move[0], move[1], move[2])
        return total_num_of_accepting_configs

    #Check if automaton accepts given word
    def check_if_word_in_language(self, word):
        self.found_accepting_configs_in_subtrees=False
        total=0
        for state in self.initial_states:
            total+=self.generate_all_accepting_configs(state, word, [self.initial_stack_symbol])
        return total > 0

    #generate all states in which automaton can finish from given state and input
    def generate_all_configs_from_given_configuration(self, state, input, stack):
        all_configs=[]

        if input == "":
            all_configs=[(state, stack)]
            return all_configs

        moves=self.get_possible_moves(state, input, stack)

        if len(moves) == 0:
            return all_configs
        
        for move in moves:
            all_configs += self.generate_all_configs_from_given_configuration(move[0], move[1], move[2])
        
        return all_configs
    
    #As above, but with duplicates removing
    def give_states_and_stacks_when_starting_from_given_configuration(self, state, input, stack):
        states_and_stacks=self.generate_all_configs_from_given_configuration(state, input, stack)
        states_and_string_stacks=[]
        for (state, stack) in states_and_stacks:
            if isinstance(stack[0], tuple):
                stack_tup=("", "")
                for tup in stack:
                    stack_tup = tuple(ele1 + ele2 for ele1, ele2 in zip(stack_tup, tup))
                states_and_string_stacks.append((state, stack_tup)) 
            else:
                states_and_string_stacks.append((state, "".join(stack)))
        return list(dict.fromkeys(states_and_string_stacks))
