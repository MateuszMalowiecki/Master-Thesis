import numpy as np
from DFA import DFA
#TODO(backend):
#1. Dodac przejscia miedzy poziomami - do przemyslenia w fazie frontend'u 
class Game_DFA:
    def __init__(self, automata):
        print("Welcome to guess an automata game")
        self.automata=automata

    def try_guess_automata(self):
        try:
            n = int(input("Please tell how much states automata have: "))
            l=int(input("Please tell how much accepted final states automata have: "))
            finals=[]
            for i in range(l):
                state=int(input("Please give final state: "))
                finals.append(state)
            k = n * len(self.automata.alphabet)
            transitions={}
            print(f"Please give {k} transitions: ")
            for old_state in range(n):
                for letter in self.automata.alphabet:
                    new_state=int(input(f"Please give transition for {old_state}, {letter}: "))
                    transitions[(old_state, letter)] = new_state
            guessed_automata=DFA(self.automata.alphabet, range(n), 0, finals, transitions)
            return self.automata.is_equal_to(guessed_automata)
        except ValueError:
            print("All states, number of states and number of final states, should be integers.")
            return False
        except AssertionError:
            print("Either you put wrong initial/final state,  wrong transition or wrong acceptance condition")
            return False
        
    def version_1(self):
        print(f"Alphabet is {self.automata.alphabet}")
        while(True):
            decision = input("Do you want now to guess the automata now? ")
            if decision.lower() == "yes":
                guessed=self.try_guess_automata()
                if guessed:
                    print("Congratulations, you guessed automata")
                    return
                else:
                    print("Sorry, you passed the wrong automata")
                    continue
            word=input("Please give the word and I will tell you if it is in language: ")
            res=self.automata.check_if_word_in_language(word)
            print(res)

    def version_2(self):
        print(f"Alphabet is {self.automata.alphabet}")
        while(True):
            decision = input("Do you want to guess the automata now? ")
            if decision.lower() == "yes":
                guessed=self.try_guess_automata()
                if guessed:
                    print("Congratulations, you guessed automata")
                    return
                else:
                    print("Sorry, you passed the wrong automata")
                    continue
            word, state=tuple(input("Please give the word and state: ").split())
            state=self.automata.give_state_when_starting_from_given_configuration(int(state), word)
            print(f"We finish in state: {state}")

dfa=DFA(["a", "b"], [0, 1, 2, 3], 0, [3], {(0, "a") : 1, (0, "b") : 1, (1, "a") : 2, (1, "b") : 2, 
        (2, "a") : 3, (2, "b") : 3, (3, "a") : 3, (3, "b") : 3})
game_DFA = Game_DFA(dfa)
game_DFA.version_2()