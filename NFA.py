#transitions is set
class NFA:
    def __init__(self, alphabet, states, initial_state, final_states, transitions):
        assert initial_state in states
        for state in final_states:
            assert state in states
        self.alphabet = alphabet
        self.states = states
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

    def is_accepting(self, state, input):
        return len(input) == 0 and state in self.final_states

    def get_possible_moves(self, state, input):
        possible_transitions=self.transitions[state] if state in self.transitions.keys() else []
        possible_moves=[]
        for transition in possible_transitions:
            (letter, new_state) = transition
            state_after_transition = new_state
        
            input_after_transition = ""
            if len(letter) == 0:
               input_after_transition = input
            elif len(input) > 0 and input[0] == transition[0]:
                input_after_transition = input[1:]
            else:
                continue

            possible_moves.append((state_after_transition, input_after_transition))
        return possible_moves

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

    def check_if_word_in_language(self, word):
        self.found_accepting_configs_in_subtrees=False
        total=self.generate_all_accepting_configs(self.initial_state, word)
        return total > 0

    def generate_all_configs_from_given_configuration(self, state, input):
        all_configs=[]

        if input == "":
            all_configs=[state]
            for old_state, transitions in self.transitions.items():
                if old_state == state: 
                    for transition in transitions:
                        if len(transition[0]) == 0:
                            all_configs.append(transition[2])
            return all_configs

        moves=self.get_possible_moves(state, input)
        
        if len(moves) == 0:
            return [state]
        
        for move in moves:
            all_configs += self.generate_all_configs_from_given_configuration(move[0], move[1])
        
        return all_configs
    #TODO: Zastanowic sie jak ogarnac brak przejsc z danego stanu
    def give_states_and_when_starting_from_given_configuration(self, state, input):
        return list(dict.fromkeys(self.generate_all_configs_from_given_configuration(state, input)))
nfa=NFA(["a", "b"], [0, 1], 0, [1], 
        [(0, "a", 0), (0, "b", 0), (0, "b", 1), (1, "a", 0), (1, "b", 0)])
print(nfa.check_if_word_in_language("abab"))