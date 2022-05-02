from tokenize import String
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from DFA import DFA, NFA
from VPA import DVPA
from Weighted import DWFA
import copy

game_screens_ids={"game_dfa1": 4, "game_dfa1_lvl2": 5, "game_dfa2": 6, "game_dfa2_lvl2": 7, 
        "game_vpa1": 8, "game_vpa1_lvl2": 9, "game_vpa2": 10, "game_vpa2_lvl2": 11, 
        "game_vpa3": 12, "game_vpa3_lvl2": 13, "game_vpa4": 14, "game_vpa4_lvl2": 15,
        "game_wfa1": 16, "game_wfa1_lvl2": 17, "game_wfa2": 18, "game_wfa2_lvl2": 19}

win_level_pages_ids= {"win_lvl1_v1_dfa_page": 22, "win_lvl1_v2_dfa_page": 23, "win_lvl1_v1_vpa_page": 24, "win_lvl1_v2_vpa_page": 25, 
        "win_lvl1_v3_vpa_page": 26, "win_lvl1_v4_vpa_page": 27, "win_lvl1_v1_wfa_page": 28, "win_lvl1_v2_wfa_page": 29, "win_lvl2_page": 30}

guess_form_screens_ids={"dfa_guess_form_v1": 33, "dfa_guess_form_v1_lvl2": 34, "dfa_guess_form_v2": 35, "dfa_guess_form_v2_lvl2": 36, 
        "vpa_guess_form_v1": 38, "vpa_guess_form_v1_lvl2": 39, "vpa_guess_form_v2": 40, "vpa_guess_form_v2_lvl2": 41, 
        "vpa_guess_form_v3": 42, "vpa_guess_form_v3_lvl2": 43, "vpa_guess_form_v4": 44, "vpa_guess_form_v4": 45,
        "wfa_guess_form_v1": 47, "wfa_guess_form_v1_lvl2": 48, "wfa_guess_form_v2": 49, "wfa_guess_form_v2_lvl2": 50}
#TODO:
#1. Refactoring (for example define macros, get rid of unneccessary code etc.) + tests (write UTs for automatas)

class MainWindow(Screen):
    pass

class SecondWindow(Screen):
    pass

class DFAChooseVersionWindow(Screen):
    pass

class VPAChooseVersionWindow(Screen):
    pass

class WFAChooseVersionWindow(Screen):
    pass

class GameWindow(Screen):
    automata_text = StringProperty("")
    answer_text= StringProperty("")
    button_text = StringProperty("")
    input = ObjectProperty(None)
    name = StringProperty("")
    first_label_x = NumericProperty(0)
    first_label_y = NumericProperty(0)
    guess_form_name = StringProperty("")
    def clear_window(self):
        self.input.text = ""
        self.answer_text = ""

    def go_to_main_menu(self):
        self.manager.screens[guess_form_screens_ids[self.guess_form_name]].number_of_tries = 0
        self.clear_window()
        self.number_of_tips = 0
        self.parent.current = "second"

    def go_to_guess_form(self):
        self.clear_window()
        self.parent.current = self.guess_form_name

class GameDFAv1Window(GameWindow):
    dfa=DFA(["a", "b"], [0, 1, 2, 3], 0, [3], {(0, "a") : 1, (0, "b") : 1, (1, "a") : 2, (1, "b") : 2, 
        (2, "a") : 3, (2, "b") : 3, (3, "a") : 3, (3, "b") : 3})

    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = f"Please write a word in the input.\n Tip:\n Alphabet of automaton: {self.dfa.alphabet}\n States of automaton: {self.dfa.states},\n Initial state of automaton: {self.dfa.initial_state}"
        self.button_text = "Check if word is in language."

    def check_word(self):
        try:
            word = self.input.text
            for letter in word:
                assert letter >= 'a' and letter <= 'z', "Error: Only letters are allowed."
                assert letter in self.dfa.alphabet,  f"Error: Letter {letter} is not in the alpahbet."
            if self.dfa.check_if_word_in_language(word):
                self.answer_text = f"word {word} is in language"
            else:
                self.answer_text = f"word {word} is not in language"
            self.input.text=""
            self.number_of_tips += 1
        except AssertionError as e:
            self.answer_text = str(e)

class GameDFAv1WindowLevel2(GameWindow):
    dfa=DFA(["a", "b"], [0, 1, 2, 3], 0, [3], {(0, "a") : 1, (0, "b") : 2, (1, "a") : 0, (1, "b") : 3, 
        (2, "a") : 3, (2, "b") : 0, (3, "a") : 2, (3, "b") : 1})

    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = f"Please write a word in the input.\n Tip:\n Alphabet of automaton: {self.dfa.alphabet}\n States of automaton: {self.dfa.states},\n Initial state of automaton: {self.dfa.initial_state}"
        self.button_text = "Check if word is in language."

    def check_word(self):
        try:
            word = self.input.text
            for letter in word:
                assert letter >= 'a' and letter <= 'z', "Error: Only letters are allowed."
                assert letter in self.dfa.alphabet,  f"Error: Letter {letter} is not in the alpahbet."
            if self.dfa.check_if_word_in_language(word):
                self.answer_text = f"word {word} is in language"
            else:
                self.answer_text = f"word {word} is not in language"
            self.input.text=""
            self.number_of_tips += 1
        except AssertionError as e:
            self.answer_text = str(e)

class GameDFAv2Window(GameWindow):
    dfa=DFA(["a", "b"], [0, 1, 2, 3], 0, [3], {(0, "a") : 1, (0, "b") : 1, (1, "a") : 2, (1, "b") : 2, 
        (2, "a") : 3, (2, "b") : 3, (3, "a") : 3, (3, "b") : 3})

    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = f"Please write a word and a state in the input.\n Tip:\n Alphabet of automaton: {self.dfa.alphabet}\n States of automaton: {self.dfa.states},\n Initial state of automaton: {self.dfa.initial_state}"
        self.button_text = "Check in which state we finish."

    def check_word(self):
        try:
            input_content = self.input.text.split()
            assert len(input_content) == 2, "Error: You should give exactly 2 values separated by space."
            word, state = input_content[0], int(input_content[1])
            for letter in word:
                assert letter in self.dfa.alphabet, f"Error: letter {letter} is not in the alphabet."
            assert state in self.dfa.states, f"Error: state should be a number between 0 and {len(self.dfa.states) - 1}."
            end_state=self.dfa.give_state_when_starting_from_given_configuration(int(state), word)
            self.answer_text = f"We finished in state: {end_state}"
            self.input.text=""
            self.number_of_tips += 1
        except ValueError as e:
            invalid_state = str(e).split()[-1]
            self.answer_text = f"Error: States in automata are numbers, but you put {invalid_state} as state."
        except AssertionError as e:
            self.answer_text = str(e) 

class GameDFAv2WindowLevel2(GameWindow):
    dfa=DFA(["a", "b"], [0, 1, 2, 3], 0, [3], {(0, "a") : 1, (0, "b") : 2, (1, "a") : 0, (1, "b") : 3, 
        (2, "a") : 3, (2, "b") : 0, (3, "a") : 2, (3, "b") : 1})

    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = f"Please write a word and a state in the input.\n Tip:\n Alphabet of automaton: {self.dfa.alphabet}\n States of automaton: {self.dfa.states},\n Initial state of automaton: {self.dfa.initial_state}"
        self.button_text = "Check in which state we finish."

    def check_word(self):
        try:
            input_content = self.input.text.split()
            assert len(input_content) == 2, "Error: You should give exactly 2 values separated by space."
            word, state = input_content[0], int(input_content[1])
            for letter in word:
                assert letter in self.dfa.alphabet, f"Error: letter {letter} is not in the alphabet."
            assert state in self.dfa.states, f"Error: state should be a number between 0 and {len(self.dfa.states) - 1}."
            end_state=self.dfa.give_state_when_starting_from_given_configuration(int(state), word)
            self.answer_text = f"We finished in state: {end_state}"
            self.input.text=""
            self.number_of_tips += 1
        except ValueError as e:
            invalid_state = str(e).split()[-1]
            self.answer_text = f"Error: States in automata are numbers, but you put {invalid_state} as state."
        except AssertionError as e:
            self.answer_text = str(e) 

'''
class GameNFAv1Window(GameWindow):
    nfa = NFA(["a", "b"], [0, 1], 0, [1], 
        [(0, "a", 0), (0, "b", 0), (0, "b", 1)])

    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = "Please write a word in the input."
        self.button_text = "Check if this word is in language."
        self.tip_text= f"Tip: Alphabet is {self.nfa.alphabet} and automata has {len(self.nfa.states)} states"

    def check_word(self):
        try:
            word = self.input.text
            for letter in word:
                assert letter >= 'a' and letter <= 'z', "Error: Only letters are allowed."
                assert letter in self.nfa.alphabet,  f"Error: Letter {letter} is not in the alpahbet."
            if self.nfa.check_if_word_in_language(word):
                self.answer_text = f"word {word} is in language"
            else:
                self.answer_text = f"word {word} is not in language"
            self.input.text=""
        except AssertionError as e:
            self.answer_text = str(e)

class GameNFAv2Window(GameWindow):
    nfa = NFA(["a", "b"], [0, 1], 0, [1], 
        [(0, "a", 0), (0, "b", 0), (0, "b", 1)])
    
    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = "Please write a word and a state in the input."
        self.button_text = "Check in which states we will finish."
        self.tip_text= f"Tip: Alphabet is {self.nfa.alphabet} and automata has {len(self.nfa.states)} states"

    def check_word(self):
        try:
            input_content = self.input.text.split()
            assert len(input_content) == 2, "Error: You should give exactly 2 values separated by space."
            word, state = input_content[0], int(input_content[1])
            for letter in word:
                assert letter in self.nfa.alphabet, f"Error: letter {letter} is not in the alphabet."
            assert state in self.nfa.states, f"Error: state should be a number between 0 and {len(self.nfa.states) - 1}."
            end_states=self.nfa.give_states_when_starting_from_given_configuration(state, word)
            self.answer_text = f"We finished in states: {end_states}"
            self.input.text=""
        except ValueError as e:
            invalid_state = str(e).split()[-1]
            self.answer_text = f"Error: States in automata are numbers, but you put {invalid_state} as state."
        except AssertionError as e:
            self.answer_text = str(e) 
'''

class GameVPAv1Window(GameWindow):
    dvpa=DVPA(["a"], ["b"], ["c"], [0, 1], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 1, (0, "b", "Z"): 1, 
            (0, "c"): 1, (1, "a"): (0, "A"), (1, "b", "A"): 0, (1, "b", "Z"): 0, (1, "c"): 0})

    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = ("Please write a word in the input.\n"
            f"  Tip:\n Alphabets of automaton: {self.dvpa.calls_alphabet}, {self.dvpa.return_alphabet}, {self.dvpa.internal_alpahbet}\n"
            f" States of automaton: {self.dvpa.states}\n Initial state of automaton: {self.dvpa.initial_state}\n Stack alphabet: {self.dvpa.stack_alphabet}\n"
            f" Initial stack symbol: {self.dvpa.initial_stack_symbol}"
            )
        self.button_text = "Check if word is in language."

    def check_word(self):
        try:
            word = self.input.text
            for letter in word:
                assert letter >= 'a' and letter <= 'z', "Error: Only letters are allowed."
                assert (letter in self.dvpa.calls_alphabet) or (letter in self.dvpa.return_alphabet) or (letter in self.dvpa.internal_alpahbet), (
                    f"Error: Letter {letter} is not in any alpahbet.")
            if self.dvpa.check_if_word_in_language(word):
                self.answer_text = f"word {word} is in language"
            else:
                self.answer_text = f"word {word} is not in language"
            self.input.text=""
            self.number_of_tips += 1
        except AssertionError as e:
            self.answer_text = str(e)

class GameVPAv1WindowLevel2(GameWindow):
    dvpa=DVPA(["a"], ["b"], ["c"], [0, 1, 2, 3], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 2, (0, "b", "Z"): 2, (0, "c"): 0, 
            (1, "a"): (0, "A"), (1, "b", "A"): 3, (1, "b", "Z"): 3, (1, "c"): 1,
            (2, "a"): (3, "A"), (2, "b", "A"): 0, (2, "b", "Z"): 0, (2, "c"): 2, 
            (3, "a"): (2, "A"), (3, "b", "A"): 1, (3, "b", "Z"): 1, (3, "c"): 3})

    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = ("Please write a word in the input.\n"
            f"  Tip:\n Alphabets of automaton: {self.dvpa.calls_alphabet}, {self.dvpa.return_alphabet}, {self.dvpa.internal_alpahbet}\n"
            f" States of automaton: {self.dvpa.states}\n Initial state of automaton: {self.dvpa.initial_state}\n Stack alphabet: {self.dvpa.stack_alphabet}\n"
            f" Initial stack symbol: {self.dvpa.initial_stack_symbol}"
            )
        self.button_text = "Check if word is in language."

    def check_word(self):
        try:
            word = self.input.text
            for letter in word:
                assert letter >= 'a' and letter <= 'z', "Error: Only letters are allowed."
                assert (letter in self.dvpa.calls_alphabet) or (letter in self.dvpa.return_alphabet) or (letter in self.dvpa.internal_alpahbet), (
                    f"Error: Letter {letter} is not in any alpahbet.")
            if self.dvpa.check_if_word_in_language(word):
                self.answer_text = f"word {word} is in language"
            else:
                self.answer_text = f"word {word} is not in language"
            self.input.text=""
            self.number_of_tips += 1
        except AssertionError as e:
            self.answer_text = str(e)

class GameVPAv2Window(GameWindow):
    dvpa=DVPA(["a"], ["b"], ["c"], [0, 1], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 1, (0, "b", "Z"): 1, 
            (0, "c"): 1, (1, "a"): (0, "A"), (1, "b", "A"): 0, (1, "b", "Z"): 0, (1, "c"): 0})

    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = ("Please write a word, a state and a stack in the input.\n"
            f"  Tip:\n Alphabets of automaton: {self.dvpa.calls_alphabet}, {self.dvpa.return_alphabet}, {self.dvpa.internal_alpahbet}\n"
            f" States of automaton: {self.dvpa.states}\n Initial state of automaton: {self.dvpa.initial_state}\n Stack alphabet: {self.dvpa.stack_alphabet}\n"
            f" Initial stack symbol: {self.dvpa.initial_stack_symbol}"
            )
        self.button_text = "Check in which states and stacks we finish."

    def check_word(self):
        try:
            input_content = self.input.text.split()
            assert len(input_content) == 3, "Error: You should give exactly 3 values separated by space."
            word, state, stack_string = input_content[0], int(input_content[1]), input_content[2]
            for letter in word:
                assert (letter in self.dvpa.calls_alphabet) or (letter in self.dvpa.return_alphabet) or (letter in self.dvpa.internal_alpahbet), (
                    f"Error: Letter {letter} is not in any alpahbet.")
            assert state in self.dvpa.states, f"Error: state should be a number between 0 and {len(self.dvpa.states) - 1}."
            for symbol in stack_string:
                assert symbol in self.dvpa.stack_alphabet, f"Error: Symbol {symbol} is not a part of stack alphabet."
            end_states, end_stacks=self.dvpa.give_state_and_stack_when_starting_from_given_configuration(state, word, list(stack_string))
            self.answer_text = f"We finished in states: {end_states} and stacks: {end_stacks}"
            self.input.text=""
            self.number_of_tips += 1
        except ValueError as e:
            invalid_state = str(e).split()[-1]
            self.answer_text = f"Error: States in automata are numbers, but you put {invalid_state} as state."
        except AssertionError as e:
            self.answer_text = str(e)

class GameVPAv2WindowLevel2(GameWindow):
    dvpa=DVPA(["a"], ["b"], ["c"], [0, 1, 2, 3], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 2, (0, "b", "Z"): 2, (0, "c"): 0, 
            (1, "a"): (0, "A"), (1, "b", "A"): 3, (1, "b", "Z"): 3, (1, "c"): 1,
            (2, "a"): (3, "A"), (2, "b", "A"): 0, (2, "b", "Z"): 0, (2, "c"): 2, 
            (3, "a"): (2, "A"), (3, "b", "A"): 1, (3, "b", "Z"): 1, (3, "c"): 3})
    
    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = ("Please write a word, a state and a stack in the input.\n"
            f"  Tip:\n Alphabets of automaton: {self.dvpa.calls_alphabet}, {self.dvpa.return_alphabet}, {self.dvpa.internal_alpahbet}\n"
            f" States of automaton: {self.dvpa.states}\n Initial state of automaton: {self.dvpa.initial_state}\n Stack alphabet: {self.dvpa.stack_alphabet}\n"
            f" Initial stack symbol: {self.dvpa.initial_stack_symbol}"
            )        
        self.button_text = "Check in which states and stacks we finish."
    
    def check_word(self):
        try:
            input_content = self.input.text.split()
            assert len(input_content) == 3, "Error: You should give exactly 3 values separated by space."
            word, state, stack_string = input_content[0], int(input_content[1]), input_content[2]
            for letter in word:
                assert (letter in self.dvpa.calls_alphabet) or (letter in self.dvpa.return_alphabet) or (letter in self.dvpa.internal_alpahbet), (
                    f"Error: Letter {letter} is not in any alpahbet.")
            assert state in self.dvpa.states, f"Error: state should be a number between 0 and {len(self.dvpa.states) - 1}."
            for symbol in stack_string:
                assert symbol in self.dvpa.stack_alphabet, f"Error: Symbol {symbol} is not a part of stack alphabet."
            end_states, end_stacks=self.dvpa.give_state_and_stack_when_starting_from_given_configuration(state, word, list(stack_string))
            self.answer_text = f"We finished in states: {end_states} and stacks: {end_stacks}"
            self.input.text=""
            self.number_of_tips += 1
        except ValueError as e:
            invalid_state = str(e).split()[-1]
            self.answer_text = f"Error: States in automata are numbers, but you put {invalid_state} as state."
        except AssertionError as e:
            self.answer_text = str(e)

class GameVPAv3Window(GameWindow):
    dvpa=DVPA(["a"], ["b"], ["c"], [0, 1], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 1, (0, "b", "Z"): 1, 
            (0, "c"): 1, (1, "a"): (0, "A"), (1, "b", "A"): 0, (1, "b", "Z"): 0, (1, "c"): 0})
    
    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = ("Please write a word, a state and a stack in the input.\n"
            f"  Tip:\n Alphabets of automaton: {self.dvpa.calls_alphabet}, {self.dvpa.return_alphabet}, {self.dvpa.internal_alpahbet}\n"
            f" States of automaton: {self.dvpa.states}\n Initial state of automaton: {self.dvpa.initial_state}\n Stack alphabet: {self.dvpa.stack_alphabet}\n"
            f" Initial stack symbol: {self.dvpa.initial_stack_symbol}"
            )
        self.button_text = "Check in which states we finish."

    def check_word(self):
        try:
            input_content = self.input.text.split()
            assert len(input_content) == 3, "Error: You should give exactly 3 values separated by space."
            word, state, stack_string = input_content[0], int(input_content[1]), input_content[2]
            for letter in word:
                assert (letter in self.dvpa.calls_alphabet) or (letter in self.dvpa.return_alphabet) or (letter in self.dvpa.internal_alpahbet), (
                    f"Error: Letter {letter} is not in any alpahbet.")
            assert state in self.dvpa.states, f"Error: state should be a number between 0 and {len(self.dvpa.states) - 1}."
            for symbol in stack_string:
                assert symbol in self.dvpa.stack_alphabet, f"Error: Symbol {symbol} is not a part of stack alphabet."
            end_states, _=self.dvpa.give_state_and_stack_when_starting_from_given_configuration(state, word, list(stack_string))
            self.answer_text = f"We finished in states: {end_states}"
            self.input.text=""
            self.number_of_tips += 1
        except ValueError as e:
            invalid_state = str(e).split()[-1]
            self.answer_text = f"Error: States in automata are numbers, but you put {invalid_state} as state."
        except AssertionError as e:
            self.answer_text = str(e)

class GameVPAv3WindowLevel2(GameWindow):
    dvpa=DVPA(["a"], ["b"], ["c"], [0, 1, 2, 3], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 2, (0, "b", "Z"): 2, (0, "c"): 0, 
            (1, "a"): (0, "A"), (1, "b", "A"): 3, (1, "b", "Z"): 3, (1, "c"): 1,
            (2, "a"): (3, "A"), (2, "b", "A"): 0, (2, "b", "Z"): 0, (2, "c"): 2, 
            (3, "a"): (2, "A"), (3, "b", "A"): 1, (3, "b", "Z"): 1, (3, "c"): 3})
    
    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = ("Please write a word, a state and a stack in the input.\n"
            f"  Tip:\n Alphabets of automaton: {self.dvpa.calls_alphabet}, {self.dvpa.return_alphabet}, {self.dvpa.internal_alpahbet}\n"
            f" States of automaton: {self.dvpa.states}\n Initial state of automaton: {self.dvpa.initial_state}\n Stack alphabet: {self.dvpa.stack_alphabet}\n"
            f" Initial stack symbol: {self.dvpa.initial_stack_symbol}"
            )        
        self.button_text = "Check in which states we finish."

    def check_word(self):
        try:
            input_content = self.input.text.split()
            assert len(input_content) == 3, "Error: You should give exactly 3 values separated by space."
            word, state, stack_string = input_content[0], int(input_content[1]), input_content[2]
            for letter in word:
                assert (letter in self.dvpa.calls_alphabet) or (letter in self.dvpa.return_alphabet) or (letter in self.dvpa.internal_alpahbet), (
                    f"Error: Letter {letter} is not in any alpahbet.")
            assert state in self.dvpa.states, f"Error: state should be a number between 0 and {len(self.dvpa.states) - 1}."
            for symbol in stack_string:
                assert symbol in self.dvpa.stack_alphabet, f"Error: Symbol {symbol} is not a part of stack alphabet."
            end_states, _=self.dvpa.give_state_and_stack_when_starting_from_given_configuration(state, word, list(stack_string))
            self.answer_text = f"We finished in states: {end_states}"
            self.input.text=""
            self.number_of_tips += 1
        except ValueError as e:
            invalid_state = str(e).split()[-1]
            self.answer_text = f"Error: States in automata are numbers, but you put {invalid_state} as state."
        except AssertionError as e:
            self.answer_text = str(e)

class GameVPAv4Window(GameWindow):
    dvpa=DVPA(["a"], ["b"], ["c"], [0, 1], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 1, (0, "b", "Z"): 1, 
            (0, "c"): 1, (1, "a"): (0, "A"), (1, "b", "A"): 0, (1, "b", "Z"): 0, (1, "c"): 0})
    
    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = ("Please write a word, a state and a stack in the input.\n"
            f"  Tip:\n Alphabets of automaton: {self.dvpa.calls_alphabet}, {self.dvpa.return_alphabet}, {self.dvpa.internal_alpahbet}\n"
            f" States of automaton: {self.dvpa.states}\n Initial state of automaton: {self.dvpa.initial_state}\n Stack alphabet: {self.dvpa.stack_alphabet}\n"
            f" Initial stack symbol: {self.dvpa.initial_stack_symbol}"
            )
        self.button_text = "Check in which stacks we finish."

    def check_word(self):
        try:
            input_content = self.input.text.split()
            assert len(input_content) == 3, "Error: You should give exactly 3 values separated by space."
            word, state, stack_string = input_content[0], int(input_content[1]), input_content[2]
            for letter in word:
                assert (letter in self.dvpa.calls_alphabet) or (letter in self.dvpa.return_alphabet) or (letter in self.dvpa.internal_alpahbet), (
                    f"Error: Letter {letter} is not in any alpahbet.")
            assert state in self.dvpa.states, f"Error: state should be a number between 0 and {len(self.dvpa.states) - 1}."
            for symbol in stack_string:
                assert symbol in self.dvpa.stack_alphabet, f"Error: Symbol {symbol} is not a part of stack alphabet."
            _, end_stacks=self.dvpa.give_state_and_stack_when_starting_from_given_configuration(state, word, list(stack_string))
            self.answer_text = f"We finished in stacks: {end_stacks}"
            self.input.text=""
            self.number_of_tips += 1
        except ValueError as e:
            invalid_state = str(e).split()[-1]
            self.answer_text = f"Error: States in automata are numbers, but you put {invalid_state} as state."
        except AssertionError as e:
            self.answer_text = str(e)

class GameVPAv4WindowLevel2(GameWindow):
    dvpa=DVPA(["a"], ["b"], ["c"], [0, 1, 2, 3], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 2, (0, "b", "Z"): 2, (0, "c"): 0, 
            (1, "a"): (0, "A"), (1, "b", "A"): 3, (1, "b", "Z"): 3, (1, "c"): 1,
            (2, "a"): (3, "A"), (2, "b", "A"): 0, (2, "b", "Z"): 0, (2, "c"): 2, 
            (3, "a"): (2, "A"), (3, "b", "A"): 1, (3, "b", "Z"): 1, (3, "c"): 3})

    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = ("Please write a word, a state and a stack in the input.\n"
            f"  Tip:\n Alphabets of automaton: {self.dvpa.calls_alphabet}, {self.dvpa.return_alphabet}, {self.dvpa.internal_alpahbet}\n"
            f" States of automaton: {self.dvpa.states}\n Initial state of automaton: {self.dvpa.initial_state}\n Stack alphabet: {self.dvpa.stack_alphabet}\n"
            f" Initial stack symbol: {self.dvpa.initial_stack_symbol}"
            )
        self.button_text = "Check in which stacks we finish."

    def check_word(self):
        try:
            input_content = self.input.text.split()
            assert len(input_content) == 3, "Error: You should give exactly 3 values separated by space."
            word, state, stack_string = input_content[0], int(input_content[1]), input_content[2]
            for letter in word:
                assert (letter in self.dvpa.calls_alphabet) or (letter in self.dvpa.return_alphabet) or (letter in self.dvpa.internal_alpahbet), (
                    f"Error: Letter {letter} is not in any alpahbet.")
            assert state in self.dvpa.states, f"Error: state should be a number between 0 and {len(self.dvpa.states) - 1}."
            for symbol in stack_string:
                assert symbol in self.dvpa.stack_alphabet, f"Error: Symbol {symbol} is not a part of stack alphabet."
            _, end_stacks=self.dvpa.give_state_and_stack_when_starting_from_given_configuration(state, word, list(stack_string))
            self.answer_text = f"We finished in stacks: {end_stacks}"
            self.input.text=""
            self.number_of_tips += 1
        except ValueError as e:
            invalid_state = str(e).split()[-1]
            self.answer_text = f"Error: States in automata are numbers, but you put {invalid_state} as state."
        except AssertionError as e:
            self.answer_text = str(e)

class GameWFAv1Window(GameWindow):
    wfa = DWFA(["a", "b"], [0, 1, 2, 3], {0 : 4, 1 : 6, 2 : 1, 3: 2}, {0 : 11, 1 : 5, 2 : 3, 3 : 7},
        {(0, "a") : (2, 1), (0, "b") : (3, 1), (1, "a") : (7, 2), (1, "b") : (9, 2), 
            (2, "a") : (6, 3), (2, "b") : (11, 3), (3, "a") : (8, 0), (3, "b") : (5, 0)})

    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = f"Please write a word in the input.\n Tip:\n Alphabet of automaton: {self.wfa.alphabet}\n States of automaton: {self.wfa.states}"
        self.button_text = "Check weight of this word."

    def check_word(self):
        try:
            word = self.input.text
            for letter in word:
                assert letter in self.wfa.alphabet,  f"Error: Letter {letter} is not in the alpahbet."
            weight = self.wfa.weight_of_word(word)
            self.answer_text = f"Weight of word {word} is {weight}"
            self.input.text=""
            self.number_of_tips += 1
        except AssertionError as e:
            self.answer_text = str(e)

class GameWFAv1WindowLevel2(GameWindow):
    wfa = DWFA(["a", "b"], [0, 1, 2, 3], {0 : 3, 1 : 5, 2 : 7, 3: 11}, {0 : 2, 1 : 6, 2 : 4, 3 : 1},
        {(0, "a") : (7, 1), (0, "b") : (5, 2), (1, "a") : (8, 0), (1, "b") : (6, 3), 
            (2, "a") : (3, 3), (2, "b") : (2, 0), (3, "a") : (11, 2), (3, "b") : (9, 1)})

    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = f"Please write a word in the input.\n Tip:\n Alphabet of automaton: {self.wfa.alphabet}\n States of automaton: {self.wfa.states}"
        self.button_text = "Check weight of this word."

    def check_word(self):
        try:
            word = self.input.text
            for letter in word:
                assert letter in self.wfa.alphabet,  f"Error: Letter {letter} is not in the alpahbet."
            weight = self.wfa.weight_of_word(word)
            self.answer_text = f"Weight of word {word} is {weight}"
            self.input.text=""
            self.number_of_tips += 1
        except AssertionError as e:
            self.answer_text = str(e)

class GameWFAv2Window(GameWindow):
    wfa = DWFA(["a", "b"], [0, 1, 2, 3], {0 : 4, 1 : 6, 2 : 1, 3: 2}, {0 : 11, 1 : 5, 2 : 3, 3 : 7},
        {(0, "a") : (2, 1), (0, "b") : (3, 1), (1, "a") : (7, 2), (1, "b") : (9, 2), 
            (2, "a") : (6, 3), (2, "b") : (11, 3), (3, "a") : (8, 0), (3, "b") : (5, 0)})

    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = f"Please write a word and a state in the input.\n Tip:\n Alphabet of automaton: {self.wfa.alphabet}\n States of automaton: {self.wfa.states}"
        self.button_text = "Check in which state and weight we finish."

    def check_word(self):
        try:
            input_content = self.input.text.split()
            assert len(input_content) == 2, "Error: You should give exactly 2 values separated by space."
            word, state = input_content[0], int(input_content[1])
            for letter in word:
                assert letter in self.wfa.alphabet, f"Error: letter {letter} is not in the alphabet."
            assert state in self.wfa.states, f"Error: state should be a number between 0 and {len(self.wfa.states) - 1}."
            end_state, path_weight=self.wfa.give_state_and_weight_when_starting_from_given_configuration(int(state), word)
            self.answer_text = f"We finished in state: {end_state} and path weight is: {path_weight}"
            self.input.text=""
            self.number_of_tips += 1
        except ValueError as e:
            invalid_state = str(e).split()[-1]
            self.answer_text = f"Error: States in automata are numbers, but you put {invalid_state} as state."
        except AssertionError as e:
            self.answer_text = str(e) 

class GameWFAv2WindowLevel2(GameWindow):
    wfa = DWFA(["a", "b"], [0, 1, 2, 3], {0 : 3, 1 : 5, 2 : 7, 3: 11}, {0 : 2, 1 : 6, 2 : 4, 3 : 1},
        {(0, "a") : (7, 1), (0, "b") : (5, 2), (1, "a") : (8, 0), (1, "b") : (6, 3), 
            (2, "a") : (3, 3), (2, "b") : (2, 0), (3, "a") : (11, 2), (3, "b") : (9, 1)})

    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = f"Please write a word and a state in the input.\n Tip:\n Alphabet of automaton: {self.wfa.alphabet}\n States of automaton: {self.wfa.states}"
        self.button_text = "Check in which state and weight we finish."

    def check_word(self):
        try:
            input_content = self.input.text.split()
            assert len(input_content) == 2, "Error: You should give exactly 2 values separated by space."
            word, state = input_content[0], int(input_content[1])
            for letter in word:
                assert letter in self.wfa.alphabet, f"Error: letter {letter} is not in the alphabet."
            assert state in self.wfa.states, f"Error: state should be a number between 0 and {len(self.wfa.states) - 1}."
            end_state, path_weight=self.wfa.give_state_and_weight_when_starting_from_given_configuration(int(state), word)
            self.answer_text = f"We finished in state: {end_state} and path weight is: {path_weight}"
            self.input.text=""
            self.number_of_tips += 1
        except ValueError as e:
            invalid_state = str(e).split()[-1]
            self.answer_text = f"Error: States in automata are numbers, but you put {invalid_state} as state."
        except AssertionError as e:
            self.answer_text = str(e) 

class DFAGuessForm(Screen):
    dfa = None
    finals_input = ObjectProperty(None)
    transitions_input = ObjectProperty(None)
    automata_text = StringProperty("")
    guess_text=StringProperty("")

    def __init__(self, **kw):
        super().__init__(**kw)
        self.guess_text = ("Write final states and transitions of automata here.\n"
                "Note: Final states should be numbers separated by a comma on one line,\n and transitions should should have form: old_state, letter, new_state; each on a separate line."
                )

    def clear_window(self):
        self.finals_input.text = ""
        self.transitions_input.text = ""

    def check_automata(self, num_of_tries):
        self.manager.screens[win_level_pages_ids[self.win_level_page_name]].label_text=f"Congratulations, you won with {self.manager.screens[game_screens_ids[self.last_game_name]].number_of_tips} tips and {num_of_tries} failed guesses."
        self.manager.screens[game_screens_ids[self.last_game_name]].number_of_tips = 0
        self.guess_text = ("Write final states and transitions of automata here.\n"
                "Note: Final states should be numbers separated by a comma on one line,\n and transitions should should have form: old_state, letter, new_state; each on a separate line."
                )
        self.parent.current = self.win_level_page_name

    def go_to_tips_form(self):
        self.clear_window()
        self.guess_text = ("Write final states and transitions of automata here.\n"
                "Note: Final states should be numbers separated by a comma on one line,\n and transitions should should have form: old_state, letter, new_state; each on a separate line."
                )
        self.parent.current = self.last_game_name

    def check_automata_correctness(self):
        try:
            finals = [int(state) for state in self.finals_input.text.split(", ")]
            trans_strings=self.transitions_input.text.split("\n")
            transitions={}
            for s in trans_strings:
                old_state, letter, new_state = s.split(", ")
                transitions[(int(old_state), letter)] = int(new_state)
            guessed_automata=DFA(self.dfa.alphabet, self.dfa.states, 0, finals, transitions)
            self.clear_window()
            is_equal, word = self.dfa.is_equal_to(guessed_automata)
            if is_equal:
                return True
            self.guess_text = f"Your automata does not match on word:\n {word}"
            return False
        except AssertionError as e:
            self.clear_window()
            self.guess_text = f"Error: {str(e)}"
            return False
        except KeyError as e:
            self.clear_window()
            self.guess_text = f"Error: Not given transition for: {e}"
            return False
        except ValueError as e:
            self.clear_window()
            self.guess_text = "ParseError!!!\n Note: Final states should be numbers separated by a comma on one line,\n and transitions should should have form: old_state, letter, new_state; each on a separate line."
            return False

class DFAGuessFormv1(DFAGuessForm):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = f"Tip:\n Alphabet of automaton: {self.dfa.alphabet}\n States of automaton: {self.dfa.states},\n Initial state of automaton: {self.dfa.initial_state}"

    def check_automata(self):
        if self.check_automata_correctness():
            num_of_tries=copy.deepcopy(self.number_of_tries)
            self.number_of_tries = 0
            super().check_automata(num_of_tries)
        else:
            self.number_of_tries += 1

    dfa=DFA(["a", "b"], [0, 1, 2, 3], 0, [3], {(0, "a") : 1, (0, "b") : 1, (1, "a") : 2, (1, "b") : 2, 
        (2, "a") : 3, (2, "b") : 3, (3, "a") : 3, (3, "b") : 3})

class DFAGuessFormv1Level2(DFAGuessForm):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = f"Tip:\n Alphabet of automaton: {self.dfa.alphabet}\n States of automaton: {self.dfa.states},\n Initial state of automaton: {self.dfa.initial_state}"

    def check_automata(self):
        if self.check_automata_correctness():
            num_of_tries=copy.deepcopy(self.number_of_tries)
            self.number_of_tries = 0
            super().check_automata(num_of_tries)
        else:
            self.number_of_tries += 1

    dfa=DFA(["a", "b"], [0, 1, 2, 3], 0, [3], {(0, "a") : 1, (0, "b") : 2, (1, "a") : 0, (1, "b") : 3, 
        (2, "a") : 3, (2, "b") : 0, (3, "a") : 2, (3, "b") : 1})

class DFAGuessFormv2(DFAGuessForm):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = f"Tip:\n Alphabet of automaton: {self.dfa.alphabet}\n States of automaton: {self.dfa.states},\n Initial state of automaton: {self.dfa.initial_state}"

    def check_automata(self):
        if self.check_automata_correctness():
            num_of_tries=copy.deepcopy(self.number_of_tries)
            self.number_of_tries = 0
            super().check_automata(num_of_tries)
        else:
            self.number_of_tries += 1

    dfa=DFA(["a", "b"], [0, 1, 2, 3], 0, [3], {(0, "a") : 1, (0, "b") : 1, (1, "a") : 2, (1, "b") : 2, 
        (2, "a") : 3, (2, "b") : 3, (3, "a") : 3, (3, "b") : 3})

class DFAGuessFormv2Level2(DFAGuessForm):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = f"Tip:\n Alphabet of automaton: {self.dfa.alphabet}\n States of automaton: {self.dfa.states},\n Initial state of automaton: {self.dfa.initial_state}"

    def check_automata(self):
        if self.check_automata_correctness():
            num_of_tries=copy.deepcopy(self.number_of_tries)
            self.number_of_tries = 0
            super().check_automata(num_of_tries)
        else:
            self.number_of_tries += 1

    dfa=DFA(["a", "b"], [0, 1, 2, 3], 0, [3], {(0, "a") : 1, (0, "b") : 2, (1, "a") : 0, (1, "b") : 3, 
        (2, "a") : 3, (2, "b") : 0, (3, "a") : 2, (3, "b") : 1})


'''
class NFAGuessForm(Screen):
    nfa = NFA(["a", "b"], [0, 1], 0, [1], 
        [(0, "a", 0), (0, "b", 0), (0, "b", 1)])
    finals_input = ObjectProperty(None)
    transitions_input = ObjectProperty(None)
    guess_text=StringProperty("")

    def __init__(self, **kw):
        super().__init__(**kw)
        self.guess_text = "Write final states and transitions of automata here"

    def clear_window(self):
        self.finals_input.text = ""
        self.transitions_input.text = ""

    def check_automata(self):
        if self.check_automata_correctness():
            self.guess_text = "Write final states and transitions of automata here"
            self.parent.current = "win_page"

    def go_to_tips_form(self):
        self.clear_window()
        self.guess_text = "Write final states and transitions of automata here"
        self.parent.current = self.last_game_name

    def check_automata_correctness(self):
        try:
            finals = [int(state) for state in self.finals_input.text.split(", ")]
            trans_strings=self.transitions_input.text.split("\n")
            transitions=[]
            for s in trans_strings:
                old_state, letter, new_state = s.split(", ")
                transitions.append((int(old_state), letter, int(new_state)))
            guessed_automata=NFA(self.nfa.alphabet, self.nfa.states, 0, finals, transitions)
            self.clear_window()
            is_equal, word = self.nfa.is_equal_to(guessed_automata)
            if is_equal:
                return True
            self.guess_text = f"Your automata does not match on word:\n {word}"
            return False
        except AssertionError as e:
            self.clear_window()
            self.guess_text = f"Error: {str(e)}"
            return False
        except ValueError as e:
            self.clear_window()
            self.guess_text = f"ParseError: final states should be numbers between 0 and {len(self.nfa.states) - 1} separated by coma, and transitions should have form: old_state, letter, new_state"
            return False

class NFAGuessFormv1(NFAGuessForm):
    pass

class NFAGuessFormv2(NFAGuessForm):
    pass
'''

class VPAGuessForm(Screen):
    dvpa=None
    finals_input = ObjectProperty(None)
    transitions_input = ObjectProperty(None)
    automata_text = StringProperty("")
    guess_text=StringProperty("")

    def __init__(self, **kw):
        super().__init__(**kw)
        self.guess_text = ("Write final states and transitions of automata here.\n"
                "Note: Final states should be numbers separated by a comma on one line,\n and transitions should should have form: old_state, letter, new_state, stack_symbol; each on a separate line."
                )

    def clear_window(self):
        self.finals_input.text = ""
        self.transitions_input.text = ""

    def check_automata(self, num_of_tries):
        self.manager.screens[win_level_pages_ids[self.win_level_page_name]].label_text=f"Congratulations, you won with {self.manager.screens[game_screens_ids[self.last_game_name]].number_of_tips} tips and {num_of_tries} failed guesses."
        self.manager.screens[game_screens_ids[self.last_game_name]].number_of_tips = 0
        self.guess_text = ("Write final states and transitions of automata here.\n"
                "Note: Final states should be numbers separated by a comma on one line,\n and transitions should should have form: old_state, letter, new_state, stack_symbol; each on a separate line."
                )
        self.parent.current = self.win_level_page_name

    def go_to_tips_form(self):
        self.clear_window()
        self.guess_text = ("Write final states and transitions of automata here.\n"
                "Note: Final states should be numbers separated by a comma on one line,\n and transitions should should have form: old_state, letter, new_state, stack_symbol; each on a separate line."
                )
        self.parent.current = self.last_game_name

    def check_automata_correctness(self):
        try:
            finals = [int(state) for state in self.finals_input.text.split(", ")]
            trans_strings=self.transitions_input.text.split("\n")
            transitions={}
            for s in trans_strings:
                old_state, letter, new_state, stack_symbol = s.split(", ")
                if letter in self.dvpa.calls_alphabet:
                    transitions[(int(old_state), letter)] = (int(new_state), stack_symbol)
                elif letter in self.dvpa.return_alphabet:
                    transitions[(int(old_state), letter, stack_symbol)] = int(new_state)
                else:
                    transitions[(int(old_state), letter)] = int(new_state)
            guessed_automata=DVPA(self.dvpa.calls_alphabet, self.dvpa.return_alphabet, self.dvpa.internal_alpahbet, self.dvpa.states, self.dvpa.stack_alphabet, 0, finals, self.dvpa.initial_stack_symbol, transitions)
            self.clear_window()
            is_equal, word = self.dvpa.is_equal_to(guessed_automata)
            if is_equal:
                return True
            self.guess_text = f"Your automata does not match on word:\n {word}"
            return False
        except AssertionError as e:
            self.clear_window()
            self.guess_text = f"Error: {str(e)}"
            return False
        except KeyError as e:
            self.clear_window()
            self.guess_text = f"Error: Not given transition for: {e}"
            return False
        except ValueError as e:
            self.clear_window()
            self.guess_text = "ParseError!!!\n Note: Final states should be numbers separated by a comma on one line,\n and transitions should should have form: old_state, letter, new_state, stack_symbol; each on a separate line."
            return False


class VPAGuessFormv1(VPAGuessForm):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = (f"  Tip:\n Alphabets of automaton: {self.dvpa.calls_alphabet}, {self.dvpa.return_alphabet}, {self.dvpa.internal_alpahbet}\n"
            f" States of automaton: {self.dvpa.states}\n Initial state of automaton: {self.dvpa.initial_state}\n Stack alphabet: {self.dvpa.stack_alphabet}\n"
            f" Initial stack symbol: {self.dvpa.initial_stack_symbol}"
            )
    def check_automata(self):
        if self.check_automata_correctness():
            num_of_tries=copy.deepcopy(self.number_of_tries)
            self.number_of_tries = 0
            super().check_automata(num_of_tries)
        else:
            self.number_of_tries += 1

    dvpa=DVPA(["a"], ["b"], ["c"], [0, 1], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 1, (0, "b", "Z"): 1, 
            (0, "c"): 1, (1, "a"): (0, "A"), (1, "b", "A"): 0, (1, "b", "Z"): 0, (1, "c"): 0})

class VPAGuessFormv1Level2(VPAGuessForm):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = (f"  Tip:\n Alphabets of automaton: {self.dvpa.calls_alphabet}, {self.dvpa.return_alphabet}, {self.dvpa.internal_alpahbet}\n"
            f" States of automaton: {self.dvpa.states}\n Initial state of automaton: {self.dvpa.initial_state}\n Stack alphabet: {self.dvpa.stack_alphabet}\n"
            f" Initial stack symbol: {self.dvpa.initial_stack_symbol}"
            )

    def check_automata(self):
        if self.check_automata_correctness():
            num_of_tries=copy.deepcopy(self.number_of_tries)
            self.number_of_tries = 0
            super().check_automata(num_of_tries)
        else:
            self.number_of_tries += 1

    dvpa=DVPA(["a"], ["b"], ["c"], [0, 1, 2, 3], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 2, (0, "b", "Z"): 2, (0, "c"): 0, 
            (1, "a"): (0, "A"), (1, "b", "A"): 3, (1, "b", "Z"): 3, (1, "c"): 1,
            (2, "a"): (3, "A"), (2, "b", "A"): 0, (2, "b", "Z"): 0, (2, "c"): 2, 
            (3, "a"): (2, "A"), (3, "b", "A"): 1, (3, "b", "Z"): 1, (3, "c"): 3})

class VPAGuessFormv2(VPAGuessForm):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = (f"  Tip:\n Alphabets of automaton: {self.dvpa.calls_alphabet}, {self.dvpa.return_alphabet}, {self.dvpa.internal_alpahbet}\n"
            f" States of automaton: {self.dvpa.states}\n Initial state of automaton: {self.dvpa.initial_state}\n Stack alphabet: {self.dvpa.stack_alphabet}\n"
            f" Initial stack symbol: {self.dvpa.initial_stack_symbol}"
            )

    def check_automata(self):
        if self.check_automata_correctness():
            num_of_tries=copy.deepcopy(self.number_of_tries)
            self.number_of_tries = 0
            super().check_automata(num_of_tries)
        else:
            self.number_of_tries += 1

    dvpa=DVPA(["a"], ["b"], ["c"], [0, 1], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 1, (0, "b", "Z"): 1, 
            (0, "c"): 1, (1, "a"): (0, "A"), (1, "b", "A"): 0, (1, "b", "Z"): 0, (1, "c"): 0})

class VPAGuessFormv2Level2(VPAGuessForm):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = (f"  Tip:\n Alphabets of automaton: {self.dvpa.calls_alphabet}, {self.dvpa.return_alphabet}, {self.dvpa.internal_alpahbet}\n"
            f" States of automaton: {self.dvpa.states}\n Initial state of automaton: {self.dvpa.initial_state}\n Stack alphabet: {self.dvpa.stack_alphabet}\n"
            f" Initial stack symbol: {self.dvpa.initial_stack_symbol}"
            )

    def check_automata(self):
        if self.check_automata_correctness():
            num_of_tries=copy.deepcopy(self.number_of_tries)
            self.number_of_tries = 0
            super().check_automata(num_of_tries)
        else:
            self.number_of_tries += 1

    dvpa=DVPA(["a"], ["b"], ["c"], [0, 1, 2, 3], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 2, (0, "b", "Z"): 2, (0, "c"): 0, 
            (1, "a"): (0, "A"), (1, "b", "A"): 3, (1, "b", "Z"): 3, (1, "c"): 1,
            (2, "a"): (3, "A"), (2, "b", "A"): 0, (2, "b", "Z"): 0, (2, "c"): 2, 
            (3, "a"): (2, "A"), (3, "b", "A"): 1, (3, "b", "Z"): 1, (3, "c"): 3})

class VPAGuessFormv3(VPAGuessForm):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = (f"  Tip:\n Alphabets of automaton: {self.dvpa.calls_alphabet}, {self.dvpa.return_alphabet}, {self.dvpa.internal_alpahbet}\n"
            f" States of automaton: {self.dvpa.states}\n Initial state of automaton: {self.dvpa.initial_state}\n Stack alphabet: {self.dvpa.stack_alphabet}\n"
            f" Initial stack symbol: {self.dvpa.initial_stack_symbol}"
            )

    def check_automata(self):
        if self.check_automata_correctness():
            num_of_tries=copy.deepcopy(self.number_of_tries)
            self.number_of_tries = 0
            super().check_automata(num_of_tries)
        else:
            self.number_of_tries += 1

    dvpa=DVPA(["a"], ["b"], ["c"], [0, 1], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 1, (0, "b", "Z"): 1, 
            (0, "c"): 1, (1, "a"): (0, "A"), (1, "b", "A"): 0, (1, "b", "Z"): 0, (1, "c"): 0})

class VPAGuessFormv3Level2(VPAGuessForm):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = (f"  Tip:\n Alphabets of automaton: {self.dvpa.calls_alphabet}, {self.dvpa.return_alphabet}, {self.dvpa.internal_alpahbet}\n"
            f" States of automaton: {self.dvpa.states}\n Initial state of automaton: {self.dvpa.initial_state}\n Stack alphabet: {self.dvpa.stack_alphabet}\n"
            f" Initial stack symbol: {self.dvpa.initial_stack_symbol}"
            )

    def check_automata(self):
        if self.check_automata_correctness():
            num_of_tries=copy.deepcopy(self.number_of_tries)
            self.number_of_tries = 0
            super().check_automata(num_of_tries)
        else:
            self.number_of_tries += 1

    dvpa=DVPA(["a"], ["b"], ["c"], [0, 1, 2, 3], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 2, (0, "b", "Z"): 2, (0, "c"): 0, 
            (1, "a"): (0, "A"), (1, "b", "A"): 3, (1, "b", "Z"): 3, (1, "c"): 1,
            (2, "a"): (3, "A"), (2, "b", "A"): 0, (2, "b", "Z"): 0, (2, "c"): 2, 
            (3, "a"): (2, "A"), (3, "b", "A"): 1, (3, "b", "Z"): 1, (3, "c"): 3})

class VPAGuessFormv4(VPAGuessForm):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = (f"  Tip:\n Alphabets of automaton: {self.dvpa.calls_alphabet}, {self.dvpa.return_alphabet}, {self.dvpa.internal_alpahbet}\n"
            f" States of automaton: {self.dvpa.states}\n Initial state of automaton: {self.dvpa.initial_state}\n Stack alphabet: {self.dvpa.stack_alphabet}\n"
            f" Initial stack symbol: {self.dvpa.initial_stack_symbol}"
            )

    def check_automata(self):
        if self.check_automata_correctness():
            num_of_tries=copy.deepcopy(self.number_of_tries)
            self.number_of_tries = 0
            super().check_automata(num_of_tries)
        else:
            self.number_of_tries += 1

    dvpa=DVPA(["a"], ["b"], ["c"], [0, 1], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 1, (0, "b", "Z"): 1, 
            (0, "c"): 1, (1, "a"): (0, "A"), (1, "b", "A"): 0, (1, "b", "Z"): 0, (1, "c"): 0})

class VPAGuessFormv4Level2(VPAGuessForm):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = (f"  Tip:\n Alphabets of automaton: {self.dvpa.calls_alphabet}, {self.dvpa.return_alphabet}, {self.dvpa.internal_alpahbet}\n"
            f" States of automaton: {self.dvpa.states}\n Initial state of automaton: {self.dvpa.initial_state}\n Stack alphabet: {self.dvpa.stack_alphabet}\n"
            f" Initial stack symbol: {self.dvpa.initial_stack_symbol}"
            )

    def check_automata(self):
        if self.check_automata_correctness():
            num_of_tries=copy.deepcopy(self.number_of_tries)
            self.number_of_tries = 0
            super().check_automata(num_of_tries)
        else:
            self.number_of_tries += 1

    dvpa=DVPA(["a"], ["b"], ["c"], [0, 1, 2, 3], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 2, (0, "b", "Z"): 2, (0, "c"): 0, 
            (1, "a"): (0, "A"), (1, "b", "A"): 3, (1, "b", "Z"): 3, (1, "c"): 1,
            (2, "a"): (3, "A"), (2, "b", "A"): 0, (2, "b", "Z"): 0, (2, "c"): 2, 
            (3, "a"): (2, "A"), (3, "b", "A"): 1, (3, "b", "Z"): 1, (3, "c"): 3})

class WFAGuessForm(Screen):
    wfa = None
    initial_function_input = ObjectProperty(None)
    final_function_input = ObjectProperty(None)
    transitions_input = ObjectProperty(None)
    automata_text = StringProperty("")
    guess_text=StringProperty("")

    def __init__(self, **kw):
        super().__init__(**kw)
        self.guess_text = ("Write weight functions and transitions of automata here.\n"
                "Note: Weight functions should be in form: state, weight; each pair on a separate line\n and transitions should have form: old_state, letter, weight, new_state; each on a separate line."
                )

    def clear_window(self):
        self.initial_function_input.text = ""
        self.final_function_input.text = ""
        self.transitions_input.text = ""

    def check_automata(self, num_of_tries):
        self.manager.screens[win_level_pages_ids[self.win_level_page_name]].label_text=f"Congratulations, you won with {self.manager.screens[game_screens_ids[self.last_game_name]].number_of_tips} tips and {num_of_tries} failed guesses."
        self.manager.screens[game_screens_ids[self.last_game_name]].number_of_tips = 0
        self.guess_text = ("Write weight functions and transitions of automata here.\n"
                "Note: Weight functions should be in form: state, weight; each pair on a separate line\n and transitions should have form: old_state, letter, weight, new_state; each on a separate line."
                )
        self.parent.current = self.win_level_page_name

    def go_to_tips_form(self):
        self.clear_window()
        self.guess_text = ("Write weight functions and transitions of automata here.\n"
                "Note: Weight functions should be in form: state, weight; each pair on a separate line\n and transitions should have form: old_state, letter, weight, new_state; each on a separate line."
                )
        self.parent.current = self.last_game_name

    def check_automata_correctness(self):
        try:
            initial_function_strings = self.initial_function_input.text.split("\n")
            final_function_strings = self.final_function_input.text.split("\n")
            trans_strings=self.transitions_input.text.split("\n")
            initial_function={}
            for s in initial_function_strings:
                state, weight = s.split(", ")
                initial_function[int(state)] = int(weight)
            final_function={}
            for s in final_function_strings:
                state, weight = s.split(", ")
                final_function[int(state)] = int(weight)
            transitions={}
            for s in trans_strings:
                old_state, letter, weight, new_state = s.split(", ")
                transitions[(int(old_state), letter)] = (int(weight), int(new_state))
            guessed_automata=DWFA(self.wfa.alphabet, self.wfa.states, initial_function, final_function, transitions)
            self.clear_window()
            is_equal, word = self.wfa.is_equal_to(guessed_automata)
            if is_equal:
                return True
            self.guess_text = f"Your automata does not match on word:\n {word}"
            return False
        except AssertionError as e:
            self.clear_window()
            self.guess_text = f"Error: {str(e)}"
            return False
        except KeyError as e:
            self.clear_window()
            self.guess_text = f"Error: Not given transition for: {e}"
            return False
        except ValueError as e:
            self.clear_window()
            self.guess_text = f"ParseError!!!\n Note: Weight functions should be in form: state, weight; each pair on a separate line\n and transitions should have form: old_state, letter, weight, new_state; each on a separate line."
            return False

class WFAGuessFormv1(WFAGuessForm):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = f"Tip:\n Alphabet of automaton: {self.wfa.alphabet}\n States of automaton: {self.wfa.states}"

    def check_automata(self):
        if self.check_automata_correctness():
            num_of_tries=copy.deepcopy(self.number_of_tries)
            self.number_of_tries = 0
            super().check_automata(num_of_tries)
        else:
            self.number_of_tries += 1

    wfa = DWFA(["a", "b"], [0, 1, 2, 3], {0 : 4, 1 : 6, 2 : 1, 3: 2}, {0 : 11, 1 : 5, 2 : 3, 3 : 7},
        {(0, "a") : (2, 1), (0, "b") : (3, 1), (1, "a") : (7, 2), (1, "b") : (9, 2), 
            (2, "a") : (6, 3), (2, "b") : (11, 3), (3, "a") : (8, 0), (3, "b") : (5, 0)})

class WFAGuessFormv1Level2(WFAGuessForm):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = f"Tip:\n Alphabet of automaton: {self.wfa.alphabet}\n States of automaton: {self.wfa.states}"

    def check_automata(self):
        if self.check_automata_correctness():
            num_of_tries=copy.deepcopy(self.number_of_tries)
            self.number_of_tries = 0
            super().check_automata(num_of_tries)
        else:
            self.number_of_tries += 1

    wfa = DWFA(["a", "b"], [0, 1, 2, 3], {0 : 3, 1 : 5, 2 : 7, 3: 11}, {0 : 2, 1 : 6, 2 : 4, 3 : 1},
        {(0, "a") : (7, 1), (0, "b") : (5, 2), (1, "a") : (8, 0), (1, "b") : (6, 3), 
            (2, "a") : (3, 3), (2, "b") : (2, 0), (3, "a") : (11, 2), (3, "b") : (9, 1)})

class WFAGuessFormv2(WFAGuessForm):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = f"Tip:\n Alphabet of automaton: {self.wfa.alphabet}\n States of automaton: {self.wfa.states}"

    def check_automata(self):
        if self.check_automata_correctness():
            num_of_tries=copy.deepcopy(self.number_of_tries)
            self.number_of_tries = 0
            super().check_automata(num_of_tries)
        else:
            self.number_of_tries += 1

    wfa = DWFA(["a", "b"], [0, 1, 2, 3], {0 : 4, 1 : 6, 2 : 1, 3: 2}, {0 : 11, 1 : 5, 2 : 3, 3 : 7},
        {(0, "a") : (2, 1), (0, "b") : (3, 1), (1, "a") : (7, 2), (1, "b") : (9, 2), 
            (2, "a") : (6, 3), (2, "b") : (11, 3), (3, "a") : (8, 0), (3, "b") : (5, 0)})

class WFAGuessFormv2Level2(WFAGuessForm):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = f"Tip:\n Alphabet of automaton: {self.wfa.alphabet}\n States of automaton: {self.wfa.states}"

    def check_automata(self):
        if self.check_automata_correctness():
            num_of_tries=copy.deepcopy(self.number_of_tries)
            self.number_of_tries = 0
            super().check_automata(num_of_tries)
        else:
            self.number_of_tries += 1

    wfa = DWFA(["a", "b"], [0, 1, 2, 3], {0 : 3, 1 : 5, 2 : 7, 3: 11}, {0 : 2, 1 : 6, 2 : 4, 3 : 1},
        {(0, "a") : (7, 1), (0, "b") : (5, 2), (1, "a") : (8, 0), (1, "b") : (6, 3), 
            (2, "a") : (3, 3), (2, "b") : (2, 0), (3, "a") : (11, 2), (3, "b") : (9, 1)})

class WinLevelPage(Screen):
    next_page=StringProperty("")
    label_text=StringProperty("")
    button_text=StringProperty("")

class WinLevel1Page(WinLevelPage):
    pass

class WinLevel1v1DFAPage(WinLevel1Page):
    pass

class WinLevel1v2DFAPage(WinLevel1Page):
    pass

class WinLevel1v1VPAPage(WinLevel1Page):
    pass

class WinLevel1v2VPAPage(WinLevel1Page):
    pass

class WinLevel1v3VPAPage(WinLevel1Page):
    pass

class WinLevel1v4VPAPage(WinLevel1Page):
    pass

class WinLevel1v1WFAPage(WinLevel1Page):
    pass

class WinLevel1v2WFAPage(WinLevel1Page):
    pass

class WinLevel2Page(WinLevelPage):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("Game.kv")

class GameApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    GameApp().run()
