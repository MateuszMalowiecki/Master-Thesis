#With help of: https://github.com/theodoregold/pushdown-automata/blob/3ce36cdfdd1f4e260121fb43dea988b96288fed0/main.py#L36
from itertools import chain, combinations

class DVPA:
    def __init__(self, calls_alphabet, return_alphabet, internal_alpahbet, states, stack_alphabet, initial_state, final_states, initial_stack_symbol, transitions):
        assert initial_state in states, f"invalid initial state number: {initial_state}"
        for state in final_states:
            assert state in states, f"invalid final state number: {state}"
        assert initial_stack_symbol in stack_alphabet, f"invalid initial stack symbol: {initial_stack_symbol}"
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
                assert len(key) >= 2, f"invalid transtion: {key} -> {value}"    
                assert key[1] in calls_alphabet or key[1] in return_alphabet or key[1] in internal_alpahbet, f"letter {key[1]} does not belong to any alphabet"
                assert False, f"invalid transtion: {key} -> {value}"
        self.calls_alphabet = calls_alphabet
        self.return_alphabet = return_alphabet
        self.internal_alpahbet = internal_alpahbet
        self.states = states
        self.stack_alphabet = stack_alphabet
        self.initial_state = initial_state
        self.final_states = final_states
        self.initial_stack_symbol = initial_stack_symbol
        self.transitions = transitions

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
