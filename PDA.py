class PDA:
    def __init__(self, alphabet, states, stack_alphabet, initial_state, final_state, initial_stack_symbol, transitions):
        assert initial_state in states
        for state in final_state:
            assert state in states
        assert initial_stack_symbol in stack_alphabet
        for (old_state, letter, stack_top, new_state, new_stack_symbols) in transitions:
            assert old_state in states and new_state in states and letter in alphabet and \
                stack_top in stack_alphabet and all([symbol in stack_alphabet for symbol in new_stack_symbols]) 
        self.alphabet = alphabet
        self.states = states
        self.stack_alphabet= stack_alphabet
        self.initial_state = initial_state
        self.final_state = final_state
        self.initial_stack_symbol= initial_stack_symbol
        self.transitions = transitions
    def is_equal_to(another):
        return False
    #TODO
    '''def check_if_word_in_language(self, word):
        actual_states=[self.initial_state]
        actual_stacks=[[self.initial_stack_symbol]]
        for w in word:
            actual_states_before_iteration = actual_states
            actual_stacks_before_iteration = actual_stacks
            for state in actual_states_before_iteration:
                actual_states.remove(state)
                for stack in actual_stacks_before_iteration:
                    actual_stack_top = stack[0]
                    actual_stack =  actual_stack[1:]
                    for (old_state, letter, stack_top, new_state, new_stack_symbols) in self.transitions:
                            if stack_top == symbol and old_state == state and letter == w:
                                actual_states.append(new_state)
                
        return actual in self.final_state '''
    def give_states_and_stacks_when_starting_from_given_configuration(state, stack, word):
        #TODO