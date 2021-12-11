#With help of: https://github.com/theodoregold/pushdown-automata/blob/3ce36cdfdd1f4e260121fb43dea988b96288fed0/main.py#L36
class PDA:
    def __init__(self, alphabet, states, stack_alphabet, initial_state, final_states, initial_stack_symbol, transitions):
        assert initial_state in states
        for state in final_states:
            assert state in states
        assert initial_stack_symbol in stack_alphabet
        #self.alphabet = alphabet
        #self.states = states
        #self.stack_alphabet= stack_alphabet
        self.initial_state = initial_state
        #self.final_states = final_states
        self.initial_stack_symbol= initial_stack_symbol
        self.transitions = {}
        for (old_state, letter, stack_top, new_state, new_stack_symbols) in transitions:
            #print(old_state, letter, stack_top, new_state, new_stack_symbols)
            assert old_state in states and new_state in states and (letter in alphabet or letter == "") and \
                stack_top in stack_alphabet and all([symbol in stack_alphabet for symbol in new_stack_symbols])
            if not old_state in self.transitions.keys():
                self.transitions[old_state] = []
            self.transitions[old_state].append((letter, stack_top, new_state, new_stack_symbols))
    
    #TODO: Checking if two PDA's are equivalent is basically undecidable
    #Talk with JMi about it.
    def is_equal_to(self, another):
        for letter in self.alphabet:
            if self.check_if_word_in_language(letter) != another.check_if_word_in_language(letter):
                return False
        return True
    
    def is_accepting(self, state, input, stack):
        return len(input) == 0 and len(stack) < 2

    def get_possible_moves(self, state, input, stack):
        possible_transitions=self.transitions[state] if state in self.transitions.keys() else []
        possible_moves=[]
        for transition in possible_transitions:
            state_after_transition = transition[2]
        
            input_after_transition = ""
            if len(transition[0]) == 0:
               input_after_transition = input
            elif len(input) > 0 and input[0] == transition[0]:
                input_after_transition = input[1:]
            else:
                continue
            
            stack_after_transition=""
            if len(transition[1]) == 0:
                stack_after_transition =  transition[3] + stack
            elif len(stack) > 0 and stack[0] == transition[1]:
                stack_after_transition =  transition[3] + stack[1:]
            else:
                continue

            possible_moves.append((state_after_transition, input_after_transition, stack_after_transition))
        return possible_moves

    def generate_all_accepting_configs(self, state, input, stack):
        total_num_of_accepting_configs=0
        if self.found_accepting_configs_in_subtrees:
            return 0
        if self.is_accepting(state, input, stack):
            #print("Got in there")
            self.found_accepting_configs_in_subtrees=True
            return 1
        moves=self.get_possible_moves(state, input, stack)
        for move in moves:
            total_num_of_accepting_configs += self.generate_all_accepting_configs(move[0], move[1], move[2])
        print(f"total_num_of_accepting_configs: {total_num_of_accepting_configs}")
        return total_num_of_accepting_configs

    #PDA accpets with empty stack
    def check_if_word_in_language(self, word):
        self.found_accepting_configs_in_subtrees=False
        total=self.generate_all_accepting_configs(self.initial_state, word, self.initial_stack_symbol)
        return total > 0

    def generate_all_configs_from_given_configuration(self, state, input, stack):
        all_configs=[]

        if input == "":
            #all_configs.append((state, stack))
            for old_state, transitions in self.transitions.items():
                if old_state == state: 
                    print(f"Transitions for: {old_state}")
                    for transition in transitions:
                        print(f"transition : {transition}")
                        if len(transition[0]) == 0:
                            print(f"2. transition : {transition}")
                            if len(transition[1]) == 0:
                                all_configs.append((transition[2], transition[3] + stack))
                            elif len(stack) > 0 and stack[0] == transition[1]:
                                all_configs.append((transition[2], transition[3] + stack[1:]))
            print(f"1. all_configs:{all_configs}")
            return all_configs

        moves=self.get_possible_moves(state, input, stack)
        
        if len(moves) == 0:
            return [(state, stack)]
        
        for move in moves:
            all_configs += self.generate_all_configs_from_given_configuration(move[0], move[1], move[2])
        
        #print(f"2. all_configs:{all_configs}")
        return all_configs
    #TODO: Think if these can't be paired
    def give_states_and_stacks_when_starting_from_given_configuration(self, state, input, stack):
        states_and_stacks = list(dict.fromkeys(self.generate_all_configs_from_given_configuration(state, input, stack)))
        #print(states_and_stacks)
        return[[state for state, _ in states_and_stacks],
                [stack for _, stack in states_and_stacks]]
pda=PDA(["a", "b"], [0, 1, 2], ["A", "Z"], 0, [2], "Z", 
        [(0, "a", "Z", 0, "AZ"), (0, "a", "A", 0, "AA"), (0, "", "Z", 1, "Z"), 
            (0, "", "A", 1, "A"), (1, "b", "A", 1, ""), (1, "", "Z", 2, "Z")])
print(pda.give_states_and_stacks_when_starting_from_given_configuration(0, "aabb", "Z"))