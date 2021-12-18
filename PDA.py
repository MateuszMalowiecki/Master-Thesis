#With help of: https://github.com/theodoregold/pushdown-automata/blob/3ce36cdfdd1f4e260121fb43dea988b96288fed0/main.py#L36
class PDA:
    def __init__(self, alphabet, states, stack_alphabet, initial_state, final_states, initial_stack_symbol, transitions, accepting_condition):
        assert initial_state in states
        for state in final_states:
            assert state in states
        assert initial_stack_symbol in stack_alphabet
        self.alphabet = alphabet
        #self.states = states
        #self.stack_alphabet= stack_alphabet
        self.initial_state = initial_state
        self.final_states = final_states
        self.initial_stack_symbol= initial_stack_symbol
        self.transitions = {}
        print(f"Transitions: {transitions}")
        for (old_state, letter, stack_top, new_state, new_stack_symbols) in transitions:
            old_state = int(old_state)
            new_state = int(new_state)
            if letter == "eps":
                letter = ""
            if new_stack_symbols == "None":
                new_stack_symbols = ""
            assert old_state in states and new_state in states and (letter in alphabet or letter == "") and \
                stack_top in stack_alphabet and all([symbol in stack_alphabet for symbol in new_stack_symbols])
            if not old_state in self.transitions.keys():
                self.transitions[old_state] = []
            self.transitions[old_state].append((letter, stack_top, new_state, new_stack_symbols))
        assert accepting_condition.lower() in ["state", "stack"]
        self.accepting_condition = accepting_condition
    
    #Since checking if two PDA's are equivalent is undecidable, I make this check by 
    #comparing for all words with length shorter than 20 if they agree on it
    def is_equal_to(self, another):
        words=[""]
        limit=20
        while(len(words[0]) < limit):
            print(f"Words length: {len(words[0])}")
            for word in words:
                if self.check_if_word_in_language(word) != another.check_if_word_in_language(word):
                    print(f"Automatas don't match on word:{word}")
                    return False
            words=[letter + word for letter in self.alphabet for word in words]
        return True
    
    def is_accepting(self, state, input, stack):
        if len(input) > 0:
            return False
        if self.accepting_condition == "stack":
            return len(stack) < 2
        elif self.accepting_condition == "state":
            return state in self.final_states
        return False

    def get_possible_moves(self, state, input, stack):
        possible_transitions=self.transitions[state] if state in self.transitions.keys() else []
        possible_moves=[]
        for transition in possible_transitions:
            (letter, stack_top, new_state, new_stack_symbols) = transition
            state_after_transition = new_state
        
            input_after_transition = ""
            if len(letter) == 0:
               input_after_transition = input
            elif len(input) > 0 and input[0] == transition[0]:
                input_after_transition = input[1:]
            else:
                continue
            
            stack_after_transition=""
            if len(stack_top) == 0:
                stack_after_transition =  new_stack_symbols + stack
            elif len(stack) > 0 and stack[0] == stack_top:
                stack_after_transition =  new_stack_symbols + stack[1:]
            else:
                continue

            possible_moves.append((state_after_transition, input_after_transition, stack_after_transition))
        return possible_moves

    def generate_all_accepting_configs(self, state, input, stack):
        total_num_of_accepting_configs=0
        if self.found_accepting_configs_in_subtrees:
            return 0
        if self.is_accepting(state, input, stack):
            self.found_accepting_configs_in_subtrees=True
            return 1
        moves=self.get_possible_moves(state, input, stack)
        for move in moves:
            total_num_of_accepting_configs += self.generate_all_accepting_configs(move[0], move[1], move[2])
        return total_num_of_accepting_configs

    def check_if_word_in_language(self, word):
        self.found_accepting_configs_in_subtrees=False
        total=self.generate_all_accepting_configs(self.initial_state, word, self.initial_stack_symbol)
        return total > 0

    def generate_all_configs_from_given_configuration(self, state, input, stack):
        all_configs=[]

        if input == "":
            all_configs=[(state, stack)]
            for old_state, transitions in self.transitions.items():
                if old_state == state: 
                    for transition in transitions:
                        if len(transition[0]) == 0:
                            if len(transition[1]) == 0:
                                all_configs.append((transition[2], transition[3] + stack))
                            elif len(stack) > 0 and stack[0] == transition[1]:
                                all_configs.append((transition[2], transition[3] + stack[1:]))
            return all_configs

        moves=self.get_possible_moves(state, input, stack)
        
        if len(moves) == 0:
            return [(state, stack)]
        
        for move in moves:
            all_configs += self.generate_all_configs_from_given_configuration(move[0], move[1], move[2])
        
        return all_configs
    def give_states_and_stacks_when_starting_from_given_configuration(self, state, input, stack):
        return list(dict.fromkeys(self.generate_all_configs_from_given_configuration(state, input, stack)))
pda=PDA(["a", "b"], [0, 1, 2], ["A", "Z"], 0, [2], "Z", 
        [(0, "a", "Z", 0, "AZ"), (0, "a", "A", 0, "AA"), (0, "", "Z", 1, "Z"), 
            (0, "", "A", 1, "A"), (1, "b", "A", 1, ""), (1, "", "Z", 2, "Z")], "state")