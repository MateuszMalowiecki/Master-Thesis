#With help of: https://github.com/theodoregold/pushdown-automata/blob/3ce36cdfdd1f4e260121fb43dea988b96288fed0/main.py#L36
class PDA:
    def __init__(self, calls_alphabet, return_alphabet, internal_alpahbet, states, stack_alphabet, initial_states, final_states, initial_stack_symbol, transitions):
        for state in initial_states:
            assert state in states
        for state in final_states:
            assert state in states
        assert initial_stack_symbol in stack_alphabet
        self.calls_alphabet = calls_alphabet
        self.return_alphabet = return_alphabet
        self.internal_alpahbet = internal_alpahbet
        #self.alphabet = calls_alphabet + return_alphabet + internal_alpahbet
        self.initial_states = initial_states
        self.final_states = final_states
        self.initial_stack_symbol= initial_stack_symbol
        self.transitions = {}
        for (old_state, letter, new_state, stack_symbol) in transitions:
            old_state = int(old_state)
            new_state = int(new_state)
            type=""
            assert old_state in states and new_state in states
            if letter in internal_alpahbet:
                type = "i"
                stack_symbol = ""
            elif letter in calls_alphabet:
                type = "c"
                assert len(stack_symbol) == 1 and stack_symbol in stack_alphabet and stack_symbol != initial_stack_symbol
            elif letter in return_alphabet:
                type = "r"
                assert len(stack_symbol) == 1 and stack_symbol in stack_alphabet
            else:
                assert False
            if not old_state in self.transitions.keys():
                self.transitions[old_state] = []
            self.transitions[old_state].append((letter, type, stack_symbol, new_state))
    
    #Checking if two automatas are equal
    #Since checking if two PDA's are equivalent is undecidable, I make this check by 
    #comparing for all words with length shorter than 20 if they agree on it
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
            (letter, type, stack_symbol, new_state) = transition
            state_after_transition = new_state
        
            if input[0] != letter:
                continue
            input_after_transition = input[1:]
            
            stack_after_transition=""
            if type=="c":
                stack_after_transition = stack_symbol + stack
            elif type=="r" and stack[0] == stack_symbol:
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
            total+=self.generate_all_accepting_configs(state, word, self.initial_stack_symbol)
        return total > 0

    #generate all states in which automata can finish from given state and input
    def generate_all_configs_from_given_configuration(self, state, input, stack):
        all_configs=[]

        if input == "":
            all_configs=[(state, stack)]
            '''for old_state, transitions in self.transitions.items():
                if old_state == state: 
                    for transition in transitions:
                        if len(transition[0]) == 0:
                            if len(transition[1]) == 0:
                                all_configs.append((transition[2], transition[3] + stack))
                            elif len(stack) > 0 and stack[0] == transition[1]:
                                all_configs.append((transition[2], transition[3] + stack[1:]))'''
            return all_configs

        moves=self.get_possible_moves(state, input, stack)

        if len(moves) == 0:
            return all_configs
        
        for move in moves:
            all_configs += self.generate_all_configs_from_given_configuration(move[0], move[1], move[2])
        
        return all_configs
    
    #As above, but with duplicates removing
    def give_states_and_stacks_when_starting_from_given_configuration(self, state, input, stack):
        return list(dict.fromkeys(self.generate_all_configs_from_given_configuration(state, input, stack)))

pda=PDA(["a"], ["b"], ["c"], [0, 1, 2], ["A", "Z"], [0], [2], "Z", 
        [(0, "a", 0, "A"), (0, "c", 1, ""), (1, "b", 1, "A"), (1, "c", 2, "")])
second_pda=PDA(["a"], ["b"], ["c"], [0, 1, 2], ["A", "Z"], [0], [2], "Z", 
        [(0, "a", 0, "A"), (0, "c", 1, ""), (1, "b", 1, "A"), (1, "c", 2, "")])
print(pda.give_states_and_stacks_when_starting_from_given_configuration(0, "ac",""))
#print(pda.check_if_word_in_language("acbc"))
#print(pda.check_if_word_in_language("acbabc"))