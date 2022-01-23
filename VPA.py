#With help of: https://github.com/theodoregold/pushdown-automata/blob/3ce36cdfdd1f4e260121fb43dea988b96288fed0/main.py#L36
from typing_extensions import final
from itertools import chain, combinations

from urllib3 import Retry

#TODO: Test functionalities
class DVPA:
    def __init__(self, calls_alphabet, return_alphabet, internal_alpahbet, states, stack_alphabet, initial_state, final_states, initial_stack_symbol, transitions):
        assert initial_state in states
        for state in final_states:
            assert state in states
        assert initial_stack_symbol in stack_alphabet
        self.calls_alphabet = calls_alphabet
        self.return_alphabet = return_alphabet
        self.internal_alpahbet = internal_alpahbet
        self.states=states
        self.stack_alphabet=stack_alphabet
        self.initial_state = initial_state
        self.final_states = final_states
        self.initial_stack_symbol= initial_stack_symbol
        self.transitions = transitions
    
    #Changing dvpa to vpa
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
        assert self.calls_alphabet == other.calls_alphabet
        assert self.return_alphabet == other.return_alphabet
        assert self.internal_alpahbet == other.internal_alpahbet
        stack_alphabet=[]
        for our_stack_letter in self.stack_alphabet:
            for other_stack_letter in other.stack_alphabet:
                stack_alphabet.append((our_stack_letter, other_stack_letter))
        initial_stack_symbol = ((self.initial_stack_symbol, other.initial_stack_symbol))
        states = []
        initial_state=(self.initial_state, other.initial_state)
        finals=[]
        transitions=[]
        for our_state in self.states:
            for other_state in other.states:
                states.append((our_state, other_state))
                if our_state in self.final_states and other_state in other.final_states:
                    finals.append((our_state, other_state))

                for letter in self.internal_alpahbet:
                    transitions[((our_state, other_state), letter)] = (self.transitions[(our_state, letter)], other.transitions[(other_state, letter)])

                for letter in self.calls_alphabet:
                    (our_new_state, our_new_letter) = self.transitions[(our_state, letter)]
                    (other_new_state, other_new_letter) = self.transitions[(other_state, letter)]
                    transitions[((our_state, other_state), letter)] = ((our_new_state, other_new_state), (our_new_letter, other_new_letter))
                
                for letter in self.return_alphabet:
                    for stack_letter in self.stack_alphabet:
                        our_new_state = self.transitions[(our_state, letter, stack_letter)]
                        other_new_state = self.transitions[(other_state, letter, stack_letter)]
                        transitions[((our_state, other_state), letter, stack_letter)] = (our_new_state, other_new_state)

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
    def have_empty_language(self):
        reachable=self.get_all_reachable_states()
        return len([state for state in self.final_states if state in reachable]) == 0

    def is_equal_to(self, other):
        return self.take_intersection(other.take_complement()).have_empty_language() and \
            other.take_intersection(self.take_complement()).have_empty_language()
    
    def check_if_word_in_language(self, word):
        actual_state=self.initial_state
        actual_stack=[self.initial_stack_symbol]
        for w in word:
            #print(f"actual_stack: {actual_stack}")
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
                    new_stack = actual_stack.insert(0, new_stack_top)
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
        print(transitions)
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

    def create_internal_transitions(self, state_pairs, state):
        transitions={}
        for letter in self.internal_alpahbet:
            new_state=[]
            for q in state:
                transis=self.get_transitions_from_state(q)
                #print(f"transis, {transis}")
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
                        new_state.append((q1, new_st))
            transitions[(state, letter)] = (tuple(new_state_pairs), tuple(new_state))
        return transitions

    def create_calls_transitions(self, state_pairs, state):
        transitions={}
        for letter in self.calls_alphabet:
            new_state=[]
            for q in state:
                transis=self.get_transitions_from_state(q)
                #print(f"transis, {transis}")
                for trans in transis:
                    (new_letter, _, _, new_st)=trans
                    if new_st not in new_state and new_letter == letter:
                        new_state.append(new_st)
            transitions[(state, letter)] = (([(q, q) for q in self.states], tuple(new_state)), (state, state_pairs, letter))
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
                    transis2=self.get_transitions_from_state(q)
                    for trans2 in transis2:
                        (new_letter2, _, new_stack_symbols2, new_state2)=trans2
                        if new_stack_symbols == new_stack_symbols2 and new_letter2 == a1:
                            res.append((q, new_state2))
        return res
    
    def create_return_initial_stack_symbol_transitions(self, state, state_pairs, letter):
        transitions={}
        new_state_for_initial=[]
        new_state_pairs_for_initial=[]
        for q in state:
            transis=self.get_transitions_from_state(q)
            for trans in transis:
                (new_letter, _, stack_symbols, new_st)=trans
                if new_st not in new_state_for_initial and new_letter == letter and stack_symbols == self.initial_stack_symbol:
                    new_state_for_initial.append(new_st)
        for (q1, q2) in state_pairs:
            transis=self.get_transitions_from_state(q2)
            #print(f"transis, {transis}")
            for trans in transis:
                (new_letter, _, stack_symbols, new_st)=trans
                if (q1, new_st) not in new_state_pairs_for_initial and new_letter == letter and stack_symbols == self.initial_stack_symbol:
                    new_state_pairs_for_initial.append((q1, new_st))
        transitions[(state, letter, self.initial_stack_symbol)] = (tuple(new_state_pairs_for_initial), tuple(new_state_for_initial))
        return transitions

    def create_return_transitions(self, state_pairs, state, stack_alphabet):
        transitions={}
        for letter in self.return_alphabet:
            for (S, R, a) in stack_alphabet:
                update=self.create_update_pairs(state_pairs, letter, a)
                new_state=[]
                new_state_pairs=[]
                for (q, q3) in update:
                    for (q4, q5) in S:
                        if q3 == q4:
                            new_state_pairs.append((q, q5))
                    if q in R:
                        new_state.append(q3)
            transitions.update(self.create_return_initial_stack_symbol_transitions(state, state_pairs, letter))
        return transitions    
    
    def create_transitions(self, states,stack_alphabet):
        transitions={}
        for (state_pairs, state) in states:
            transitions.update(self.create_internal_transitions(state_pairs, state))
            transitions.update(self.create_calls_transitions(state_pairs, state))
            transitions.update(self.create_return_transitions(state_pairs, state))
        return transitions
    
    def to_DVPA(self):
        states_pairs=[(q1, q2) for q1 in self.states for q2 in self.states]
        subsets_of_states=list(chain.from_iterable(combinations(self.states, r) for r in range(len(self.states)+1)))
        subsets_of_pair_of_states=list(chain.from_iterable(combinations(states_pairs, r) for r in range(len(states_pairs)+1)))
        states=[(q1, q2) for q1 in subsets_of_pair_of_states for q2 in subsets_of_states]
        stack_alphabet=[(S, R, a) for S in subsets_of_pair_of_states for R in subsets_of_states for a in self.calls_alphabet] + [self.initial_stack_symbol]
        initial=([(q, q) for q in self.states], self.initial_states)
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
    
    #Checking if two automatas are equal
    def is_equal_to(self, another):
        words=[""]
        limit=15
        alphabet = self.calls_alphabet + self.return_alphabet + self.internal_alpahbet
        while(len(words[0]) <= limit):
            print(f"Words length: {len(words[0])}")
            for word in words:
                if self.check_if_word_in_language(word) != another.check_if_word_in_language(word):
                    print(f"Automatas don't match on word:{word}")
                    return False
            words=[letter + word for letter in alphabet for word in words]
        return True
    
    '''def is_equal_to(self, other):
        return self.take_intersection(other.take_complement()).have_empty_language() and \
            other.take_intersection(self.take_complement()).have_empty_language()
    '''
    
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

    #Check if automata accepts given word
    def check_if_word_in_language(self, word):
        self.found_accepting_configs_in_subtrees=False
        total=0
        for state in self.initial_states:
            total+=self.generate_all_accepting_configs(state, word, [self.initial_stack_symbol])
        return total > 0

    #generate all states in which automata can finish from given state and input
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

dvpa=DVPA(["a"], ["b"], ["c"], [0, 1, 2], ["A", "Z"], 0, [2], "Z", 
        {(0, "a"): (0, "A"), (0, "c"): 1, (1, "b", "A"): 1, (1, "c"): 2})
print(dvpa.check_if_word_in_language("acbc"))
print(dvpa.check_if_word_in_language("acb"))
print(dvpa.check_if_word_in_language("bacbc"))
print(dvpa.have_empty_language())
print(dvpa.give_state_and_stack_when_starting_from_given_configuration(0, "acb",[]))
vpa=VPA(["a"], ["b"], ["c"], [0, 1, 2], ["A", "Z"], [0], [2], "Z", 
        [(0, "a", 0, "A"), (0, "c", 1, ""), (1, "b", 1, "A"), (1, "c", 2, "")])
second_vpa=VPA(["a"], ["b"], ["c"], [0, 1, 2], ["A", "Z"], [0], [2], "Z", 
        [(0, "a", 0, "A"), (0, "c", 1, ""), (1, "b", 1, "A"), (1, "c", 2, "")])
print(vpa.check_if_word_in_language("bacbc"))
'''print(vpa.check_if_word_in_language("acb"))
print(vpa.check_if_word_in_language("bac"))
print(vpa.give_states_and_stacks_when_starting_from_given_configuration(0, "aaacb",[]))
print(vpa.have_empty_language())
print(second_vpa.have_empty_language())
vpa_inter=vpa.take_intersection(second_vpa)
print(vpa_inter.check_if_word_in_language("acbc"))
print(vpa_inter.check_if_word_in_language("aaacbbbc"))
print(vpa_inter.check_if_word_in_language("acb"))
print(vpa_inter.check_if_word_in_language("bac"))
print(vpa_inter.give_states_and_stacks_when_starting_from_given_configuration((0, 0), "aaacb",[("Z", "Z")]))
print(vpa_inter.have_empty_language())
#print(vpa.check_if_word_in_language("acbc"))
#print(vpa.check_if_word_in_language("acbabc"))'''