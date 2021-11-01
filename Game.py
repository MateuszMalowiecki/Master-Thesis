import random
from DFA import DFA
from NFA import NFA
class Game_DFA_v1:
    def __init__(self, automata):
        self.automata=automata
    def try_guess_language(self):
        language=[]
        while True:
            word=input("Write word in language or END if language is complete")
            if word == "END":
                break
            language.append(word)
        for word in language:
            if not self.automata.check_if_word_in_language(word):
                return False
        return True
        
    def level_1(self):
        print(f"automata has {len(self.automata.states)} states")
        for transition in self.automata.transitions:
            print(f"Automata has transition {transition}")
        for final in self.automata.finals:
            print(f"Automata has final state {final}")
        is_guessed=self.try_guess_language()
        if is_guessed:
            print("You passed the level")
            return
        print("You failed the level")

    def level_2(self):
        print(f"automata has {len(self.automata.states)} states")
        for final in self.automata.finals:
            print(f"Automata has final state {final}")
        for i in range(3):
            old_state, letter= input("Please give some some state and a a letter")
            new_state=self.automata.transtions[(old_state, letter)]
            print(f"{old_state} - {letter} > {new_state}")
        is_guessed=self.try_guess_language()
        if is_guessed:
            print("You passed the level")
            return
        print("You failed the level")
    

class Game_DFA_v2:
    def __init__(self, language, alpahabet):
        self.alphabet=alpahabet
        self.language=language
    def write_n_words(self, n):
        for i in range(n):
            print(self.language[random.randint(0, len(self.language))])
    
    def try_guess_automata(self):
        n=input("Please tell how much states automata have: ")
        k= n * len(self.alphabet)
        transitions=[]
        for i in range(int(k)):
            old_state, letter, new_state=input("Please give transition: ")
            transitions.append(((old_state, letter), new_state))
        l=input("Please tell how much accepted final states automata have: ")
        finals=[]
        for i in range(l):
            state=input("Please give final state: ")
            finals.append(state)
        guessed_automata=DFA(self.alphabet, range(n), 0, finals, transitions)
        for word in self.language:
            if not guessed_automata.check_if_word_in_language(word):
                return False
        return True
    def level_1(self):
        print("Here are the words, your language contains:")
        for word in self.language:
            print(word)
        is_guessed=self.try_guess_automata()
        if is_guessed:
            print("You passed the level")
            return
        print("You failed the level")
    
    def level_2(self):
        n=input("Please choose how many words from language you want to know:")
        self.write_n_words(n)
        is_guessed=self.try_guess_automata()
        if is_guessed:
            print("You passed the level")
            return
        print("You failed the level")

    def level_3(self):
        word1, word2, word3 = input("Give three words")
        print(f"Word1: {word1 in self.language}")
        print(f"Word2: {word2 in self.language}")
        print(f"Word3: {word3 in self.language}")
        is_guessed=self.try_guess_automata()
        if is_guessed:
            print("You passed the level")
            return
        print("You failed the level")
        
    def level_4(self):
        print("Here are three words in language")
        self.write_n_words(3)
        is_guessed=self.try_guess_automata()
        if is_guessed:
            print("You passed the level")
            return
        print("You failed the level")

#gdfa=Game_DFA_v2(["a", "b", "ab", "aa", "bb", "ba"], ["a", "b"])
#gdfa.level_1()