import numpy as np
from PDA import PDA
#TODO(backend):
#1. Dodac przejscia miedzy poziomami - do przemyslenia w fazie frontend'u 
class Game_PDA:
    def __init__(self, automata):
        print("Welcome to guess an automata game")
        self.automata=automata
    
    def try_guess_automata(self):
        try:
            n=int(input("Please tell how much states automata have: "))
            
            l=int(input("Please tell how much accepted final states automata have: "))
            finals=[]
            
            while len(finals) != l:
                state=int(input("Please give final state: "))
                if state not in range(n):
                    print("States must be integers within range(0, n-1)")
                    continue
                finals.append(state)

            m=int(input("Please tell how much symbols stack alphabet will have: "))
            stack_alphabet = []
            for _ in range(m):
                symbol = input("Please give stack symbol: ")
                stack_alphabet.append(symbol)
            initial_stack_symbol = input("Please give initial stack symbol: ")
            k = int(input("Please give number of transitions: "))
            transitions=[]
            print(f"Please give {k} transitions.")
            for _ in range(k):
                transition = tuple(input("Please give transition in form: old_state, letter, stack_top, new_state, new_stack_symbols: ").split())
                transitions.append(transition)
            accepting_condition = input(f"Please tell PDA accepting condition (state or stack): ")
            guessed_automata=PDA(self.automata.alphabet, range(n), stack_alphabet, 0, finals, initial_stack_symbol, transitions, accepting_condition)
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
            decision = input("Do you want now to guess the automata now? ")
            if decision.lower() == "yes":
                guessed=self.try_guess_automata()
                if guessed:
                    print("Congratulations, you guessed automata")
                    return
                else:
                    print("Sorry, you passed the wrong automata")
                    continue
            word, state, stack_string=tuple(input("Please give the word, state and stack: ").split())
            states_and_stacks=self.automata.give_states_and_stacks_when_starting_from_given_configuration(int(state), word, stack_string)
            print(f"Possible states and stacks: {states_and_stacks}")
            for new_state, new_stack in states_and_stacks:
                print(f"{new_state}, {new_stack}")
    
    def version_3(self):
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
            word, state, stack_string=tuple(input("Please give the word, state and stack: ").split())
            states_and_stacks=self.automata.give_states_and_stacks_when_starting_from_given_configuration(int(state), word, stack_string)
            print("Possible states:")
            for new_state, _ in states_and_stacks:
                print(new_state)
    
    def version_4(self):
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
            word, state, stack_string=tuple(input("Please give the word, state and stack: ").split())
            states_and_stacks=self.automata.give_states_and_stacks_when_starting_from_given_configuration(int(state), word, stack_string)
            print(f"Possible stacks:")
            for _, new_stack in states_and_stacks:
                print(new_stack)
pda=PDA(["a", "b"], [0, 1, 2], ["A", "Z"], 0, [2], "Z", 
        [(0, "a", "Z", 0, "AZ"), (0, "a", "A", 0, "AA"), (0, "", "Z", 1, "Z"), 
            (0, "", "A", 1, "A"), (1, "b", "A", 1, ""), (1, "", "Z", 2, "Z")], "state")
game_PDA = Game_PDA(pda)
game_PDA.version_1()
