class DFA:
    def __init__(self, alphabet, states, initial_state, final_states, transitions):
        assert initial_state in states
        for state in final_states:
            assert state in states
        for (old_state, letter) in transitions:
            assert old_state in states and transitions[(old_state, letter)] in states and letter in alphabet
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.final_states = final_states
        self.transitions = transitions

    #Checking if two automatas are equal
    def is_equal_to(self, another):
        words=[""]
        limit=20
        while(len(words[0]) <= limit):
            print(f"Words length: {len(words[0])}")
            for word in words:
                if self.check_if_word_in_language(word) != another.check_if_word_in_language(word):
                    print(f"Automatas don't match on word:{word}")
                    return False
            words=[letter + word for letter in self.alphabet for word in words]
        return True

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
