import numpy as np
from VPA import DVPA
class Game_DVPA:
    def __init__(self, automata):
        print("Welcome to guess an automata game")
        self.automata=automata
    
    #Method for passing user's automata and checking its correctness
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
            transitions={}
            for old_state in range(n):
                for letter in self.automata.calls_alphabet:
                    new_state, new_stack_letter=tuple(input(f"Please give transition for {old_state}, {letter} in form new_state new_stack_symbol: ").split())
                    transitions[(old_state, letter)] = (int(new_state), new_stack_letter)
                for letter in self.automata.return_alphabet:
                    for stack_letter in stack_alphabet:
                        new_state=int(input(f"Please give transition for {old_state}, {letter}, {stack_letter}: "))
                        transitions[(old_state, letter, stack_letter)] = new_state
                for letter in self.automata.internal_alpahbet:
                    new_state=int(input(f"Please give transition for {old_state}, {letter}: "))
                    transitions[(old_state, letter)] = new_state
            guessed_automata=DVPA(self.automata.calls_alphabet, self.automata.return_alphabet, self.automata.internal_alpahbet, range(n), stack_alphabet, 0, finals, initial_stack_symbol, transitions)
            return self.automata.is_equal_to(guessed_automata)
        except ValueError as e:
            print(e)
            print("All states, number of states and number of final states, should be integers.")
            return False
        except AssertionError as e:
            print("Either you put wrong initial/final state, wrong initial stack symbol, wrong transition or wrong acceptance condition")
            return False

    #Some versions of our game:    
    def version_1(self):
        print(f"Alphabet of calls is {self.automata.calls_alphabet}")
        print(f"Alphabet of returns is {self.automata.return_alphabet}")
        print(f"Alphabet of internals is {self.automata.internal_alpahbet}")
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
            word=input("Please give the word and I will tell you if it is in language: ")
            res=self.automata.check_if_word_in_language(word)
            print(res)

    def version_2(self):
        print(f"Alphabet of calls is {self.automata.calls_alphabet}")
        print(f"Alphabet of returns is {self.automata.return_alphabet}")
        print(f"Alphabet of internals is {self.automata.internal_alpahbet}")
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
            new_state, stack=self.automata.give_state_and_stack_when_starting_from_given_configuration(int(state), word, list(stack_string))
            print(f"We finish in state: {new_state}, stack: {stack}")
    
    def version_3(self):
        print(f"Alphabet of calls is {self.automata.calls_alphabet}")
        print(f"Alphabet of returns is {self.automata.return_alphabet}")
        print(f"Alphabet of internals is {self.automata.internal_alpahbet}")
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
            new_state, _ = self.automata.give_state_and_stack_when_starting_from_given_configuration(int(state), word, list(stack_string))
            print(f"We finish in state: {new_state}")
    
    def version_4(self):
        print(f"Alphabet of calls is {self.automata.calls_alphabet}")
        print(f"Alphabet of returns is {self.automata.return_alphabet}")
        print(f"Alphabet of internals is {self.automata.internal_alpahbet}")
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
            _, new_stack = self.automata.give_state_and_stack_when_starting_from_given_configuration(int(state), word, list(stack_string))
            print(f"We finish in stack: {new_stack}")

dvpa=DVPA(["a"], ["b"], ["c"], [0, 1], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 1, (0, "b", "Z"): 1, 
            (0, "c"): 1, (1, "a"): (0, "A"), (1, "b", "A"): 0, (1, "b", "Z"): 0, (1, "c"): 0})

game_DVPA = Game_DVPA(dvpa)
game_DVPA.version_4()
