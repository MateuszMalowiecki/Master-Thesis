import random, numpy as np
from DFA import DFA
from NFA import NFA
#TODO(backend):
#1. Dodac przejscia miedzy poziomami - do przemyslenia w fazie frontend'u 
#2. Poprawic sprawdzenie poprawnosci automatow - najprosciej https://stackoverflow.com/questions/54851609/given-two-dfas-how-can-i-check-that-the-language-generated-by-the-first-dfa-is 
#3. poprawic sprawdzanie poprawnosci inputow
class Game_DFA_v1:
    def __init__(self, automata):
        print("Welcome to guess an automata game")
        self.automata=automata
        self.level_1()
    def try_guess_language(self):
        language=[]
        while True:
            word=input("Write word in language or END if language is complete: ")
            if word == "END":
                break
            for letter in word:
                if letter not in self.automata.alphabet:
                    print(f"This word contains letter {letter}, which is not part of alphabet")
                    continue
            language.append(word)
        for word in language:
            if not self.automata.check_if_word_in_language(word):
                return False
        return True
        
    def level_1(self):
        print("Welcome to level 1: ")
        print(f"automata has {len(self.automata.states)} states")
        for transition in self.automata.transitions:
            print(f"Automata has transition {transition}")
        for final in self.automata.finals:
            print(f"Automata has final state {final}")
        is_guessed=self.try_guess_language()
        if is_guessed:
            print("You passed the level 1")
            self.level_2()
            return
        print("You failed the level 1")

    def level_2(self):
        try:
            print("Welcome to level 2")
            print(f"automata has {len(self.automata.states)} states")
            for final in self.automata.finals:
                print(f"Automata has final state {final}")
            for i in range(3):
                old_state, letter= tuple( x for x in input("Please give some some state and a letter: ").split())
                new_state=self.automata.transitions[(int(old_state), letter)]
                print(f"{old_state} - {letter} > {new_state}")
            is_guessed=self.try_guess_language()
            if is_guessed:
                print("You passed the level 2")
                return
        except ValueError:
            print("You should give pair: state letter")
        finally:
            print("You failed the level 2")

class Game_DFA_v2:
    def __init__(self, language, alpahabet):
        print("Welcome to guess an automata game")
        self.alphabet=alpahabet
        self.language=language
        self.level_1()
    def write_n_words(self, n):
        indices=np.random.choice(len(self.language), min(n, len(self.language)), False)
        for i in indices:
            print(self.language[i])
    
    def try_guess_automata(self):
        try:
            n=int(input("Please tell how much states automata have: "))
            print(n * len(self.alphabet))
            k= n * len(self.alphabet)
            transitions={}
            print(f"Please give {k} transitions.")
            for old_state in range(n):
                for letter in self.alphabet:
                    new_state=int(input(f"Please give transition for {old_state}, {letter}: "))
                    transitions[(old_state, letter)] = new_state
            l=int(input("Please tell how much accepted final states automata have: "))
            finals=[]
            for i in range(l):
                state=int(input("Please give final state: "))
                finals.append(state)
            guessed_automata=DFA(self.alphabet, range(n), 0, finals, transitions)
            for word in self.language:
                if not guessed_automata.check_if_word_in_language(word):
                    return False
            return True
        except ValueError:
            print("All states, number of states and number of final states, should be integers.")
            return False
    def level_1(self):
        print("Welcome to level 1")
        print("Here are the words, your language contains:")
        for word in self.language:
            print(word)
        is_guessed=self.try_guess_automata()
        if is_guessed:
            print("You passed the level 1")
            self.level_2()
            return
        print("You failed the level 1")
    
    def level_2(self):
        try:
            print("Welcome to level 2")
            n=int(input("Please choose how many words from language you want to know: "))
            self.write_n_words(n)
            is_guessed=self.try_guess_automata()
            if is_guessed:
                print("You passed the level 2")
                self.level_3()
                return
        except ValueError:
            print("Number of words you want to know should be an integer")
        finally:
            print("You failed the level 2")

    def level_3(self):
        try: 
            print("Welcome to level 3")
            word1, word2, word3 = tuple(x for x in input("Give three words: ").split())
            print(f"Word1: {word1 in self.language}")
            print(f"Word2: {word2 in self.language}")
            print(f"Word3: {word3 in self.language}")
            is_guessed=self.try_guess_automata()
            if is_guessed:
                print("You passed the level 3")
                self.level_4()
                return
        except ValueError:
            print("You should give three words")
        finally:
            print("You failed the level 3")
        
    def level_4(self):
        print("Welcome to level 4")
        print("Here are three words in language")
        self.write_n_words(3)
        is_guessed=self.try_guess_automata()
        if is_guessed:
            print("You passed the level 4")
            return
        print("You failed the level 4")

gdfa=Game_DFA_v2(["a", "b", "aa", "ab", "ba", "bb"], ["a", "b"])
#gdfa=Game_DFA_v1(DFA(["a", "b"], [0, 1, 2, 3], 0, [1, 2], {(0, "a") : 1, (0, "b") : 1, (1, "a") : 2, (1, "b") : 2, 
        #(2, "a") : 3, (2, "b") : 3, (3, "a") : 3, (3, "b") : 3}))
#gdfa.level_2()