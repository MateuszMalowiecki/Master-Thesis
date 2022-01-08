#With help of: https://github.com/theodoregold/pushdown-automata/blob/3ce36cdfdd1f4e260121fb43dea988b96288fed0/main.py#L36
from typing_extensions import final


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
    
    #def take_complement(self):
        #TODO: Make it after creation of DVPAs
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

vpa=VPA(["a"], ["b"], ["c"], [0, 1, 2], ["A", "Z"], [0], [2], "Z", 
        [(0, "a", 0, "A"), (0, "c", 1, ""), (1, "b", 1, "A"), (1, "c", 2, "")])
second_vpa=VPA(["a"], ["b"], ["c"], [0, 1, 2], ["A", "Z"], [0], [2], "Z", 
        [(0, "a", 0, "A"), (0, "c", 1, ""), (1, "b", 1, "A"), (1, "c", 2, "")])
print(vpa.check_if_word_in_language("acbc"))
print(vpa.check_if_word_in_language("acb"))
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
#print(vpa.check_if_word_in_language("acbabc"))