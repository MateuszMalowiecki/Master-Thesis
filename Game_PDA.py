import numpy as np
from PDA import PDA
#TODO(backend):
#1. Dodac przejscia miedzy poziomami - do przemyslenia w fazie frontend'u 
#2. Poprawic sprawdzenie poprawnosci automatow - najprosciej https://stackoverflow.com/questions/54851609/given-two-dfas-how-can-i-check-that-the-language-generated-by-the-first-dfa-is 
class Game_PDA:
    def __init__(self, automata):
        print("Welcome to guess an automata game")
        self.automata=automata
        self.level_1()
    
    def try_guess_automata(self):
        try:
            n=int(input("Please tell how much states automata have: "))
            
            l=int(input("Please tell how much accepted final states automata have: "))
            finals=[]
            
            while len(finals) != l:
                state=int(input("Please give final state: "))
                if state not in range(n):
                    print("States must be integers within range(1, n)")
                    continue
                finals.append(state)
            m=int(input("Please tell how much symbols stack alphabet will have: "))
            stack_alphabet = []
            for _ in range(m):
                symbol = input("Please give stack symbol: ")
                stack_alphabet.append(symbol)
            initial_stack_symbol = input("Please give initial stack symbol: ")
            k = input("Please give number of transitions: ")
            transitions=[]
            print(f"Please give {k} transitions.")
            for _ in range(k):
                transition = input("Please give transition in form: old_state, \
                letter, stack_top, new_state, new_stack_symbols")
                transitions.append(transition)
            guessed_automata=PDA(self.automata.alphabet, range(n), stack_alphabet, 0, finals, initial_stack_symbol, transitions)
            return self.automata.is_equal_to(guessed_automata)
        except ValueError:
            print("All states, number of states and number of final states, should be integers.")
            return False
        
    def version_1(self):
        while(True):
            decision = input("Do you want now to guess the automata now?")
            if decision.lower() == "yes":
                guessed=self.try_guess_automata()
                if guessed:
                    print("Congratulations, you guessed automata")
                    return
                else:
                    print("Sorry, you passed the wrong automata")
            word=input("Please give the word and I will tell you if it is in language: ")
            res=self.automata.check_if_word_in_language(word)
            print(res)

    def version_2(self):
        while(True):
            decision = input("Do you want now to guess the automata now?")
            if decision.lower() == "yes":
                guessed=self.try_guess_automata()
                if guessed:
                    print("Congratulations, you guessed automata")
                    return
                else:
                    print("Sorry, you passed the wrong automata")
            word, state, stack_string=input("Please give the word, state and stack: ")
            stack=[w for w in stack_string]
            (states, stacks)=self.automata.give_states_and_stacks_when_starting_from_given_configuration(state, stack, word)
            print(f"Possible states: {states}, possible stacks: {stacks}")
    
    def version_3(self):
        while(True):
            decision = input("Do you want now to guess the automata now?")
            if decision.lower() == "yes":
                guessed=self.try_guess_automata()
                if guessed:
                    print("Congratulations, you guessed automata")
                    return
                else:
                    print("Sorry, you passed the wrong automata")
            word, state, stack_string=input("Please give the word, state and stack: ")
            stack=[w for w in stack_string]
            (states, _)=self.automata.give_states_and_stacks_when_starting_from_given_configuration(state, stack, word)
            print(f"Possible states: {states}")    
    
    def version_4(self):
        while(True):
            decision = input("Do you want now to guess the automata now?")
            if decision.lower() == "yes":
                guessed=self.try_guess_automata()
                if guessed:
                    print("Congratulations, you guessed automata")
                    return
                else:
                    print("Sorry, you passed the wrong automata")
            word, state, stack_string=input("Please give the word, state and stack: ")
            stack=[w for w in stack_string]
            (_, stacks)=self.automata.give_states_and_stacks_when_starting_from_given_configuration(state, stack, word)
            print(f"Ppossible stacks: {stacks}")