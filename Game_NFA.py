import numpy as np
from NFA import NFA
#TODO(backend):
#1. Dodac przejscia miedzy poziomami - do przemyslenia w fazie frontend'u 
#2. Poprawic sprawdzenie poprawnosci automatow - najprosciej https://stackoverflow.com/questions/54851609/given-two-dfas-how-can-i-check-that-the-language-generated-by-the-first-dfa-is 
class Game_NFA:
    def __init__(self, automata):
        print("Welcome to guess an automata game")
        self.automata=automata
    def try_guess_automata(self):
        try:
            n=int(input("Please tell how much states automata have: "))
            l=int(input("Please tell how much accepted final states automata have: "))
            finals=[]
            for i in range(l):
                state=int(input("Please give final state: "))
                finals.append(state)
            k = int(input("Please give number of transitions: "))
            transitions=[]
            print(f"Please give {k} transitions.")
            for _ in range(k):
                transition = tuple(input("Please give transition in form: old_state, letter, new_state: ").split())
                transitions.append(transition)
            guessed_automata=NFA(self.automata.alphabet, range(n), 0, finals, transitions)
            return self.automata.is_equal_to(guessed_automata)
        except ValueError:
            print("All states, number of states and number of final states, should be integers.")
            return False
        except AssertionError as e:
            print(e)
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
            states=self.automata.give_states_and_when_starting_from_given_configuration(int(state), word)
            print("We finish in states: ")
            for state in states:
                print(state)

nfa=NFA(["a", "b"], [0, 1], 0, [1], 
        [(0, "a", 0), (0, "b", 0), (0, "b", 1), (1, "a", 0), (1, "b", 0)])
game_NFA = Game_NFA(nfa)
game_NFA.version_2()