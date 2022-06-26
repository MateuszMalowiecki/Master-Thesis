from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from numpy.core.arrayprint import printoptions
from DFA import DFA
from VPA import DVPA
from Weighted import DWFA
from Automata_generator import Automata_generator
import copy
from matplotlib import pyplot as plt
from kivy.core.window import Window

from kivy.garden.matplotlib import FigureCanvasKivyAgg

import networkx as nx
import random
from kivy.app import App
  
# importing kivy builder
from kivy.lang import Builder


game_screens_ids={"game_dfa1_lvl1": 4, "game_dfa1_lvl2": 5, "game_dfa1_lvl3": 6, "game_dfa1_lvl4": 7,
        "game_dfa1_lvl5": 8, "game_dfa2_lvl1": 9, "game_dfa2_lvl2": 10, "game_dfa2_lvl3": 11, 
        "game_dfa2_lvl4": 12, "game_dfa2_lvl5": 13, "game_vpa1_lvl1": 14, "game_vpa1_lvl2": 15,
        "game_vpa1_lvl3": 16, "game_vpa1_lvl4": 17,"game_vpa1_lvl5": 18, "game_vpa2_lvl1": 19, 
        "game_vpa2_lvl2": 20, "game_vpa2_lvl3": 21, "game_vpa2_lvl4": 22, "game_vpa2_lvl5": 23,
        "game_wfa1_lvl1": 24, "game_wfa1_lvl2": 25, "game_wfa1_lvl3": 26, "game_wfa1_lvl4": 27,
        "game_wfa1_lvl5": 28, "game_wfa2_lvl1": 29, "game_wfa2_lvl2": 30, "game_wfa2_lvl3": 31, 
        "game_wfa2_lvl4": 32, "game_wfa2_lvl5": 33}

win_level_pages_ids= {"win_lvl1_v1_dfa_page": 40, "win_lvl2_v1_dfa_page": 41, "win_lvl3_v1_dfa_page": 42, "win_lvl4_v1_dfa_page": 43,
        "win_lvl1_v2_dfa_page": 44, "win_lvl2_v2_dfa_page": 45, "win_lvl3_v2_dfa_page": 46, "win_lvl4_v2_dfa_page": 47,
        "win_lvl1_v1_vpa_page": 48, "win_lvl2_v1_vpa_page": 49, "win_lvl3_v1_vpa_page": 50, "win_lvl4_v1_vpa_page": 51,
        "win_lvl1_v2_vpa_page": 52, "win_lvl2_v2_vpa_page": 53, "win_lvl3_v2_vpa_page": 54, "win_lvl4_v2_vpa_page": 55,
        "win_lvl1_v1_wfa_page": 56, "win_lvl2_v1_wfa_page": 57, "win_lvl3_v1_wfa_page": 58, "win_lvl4_v1_wfa_page": 59,
        "win_lvl1_v2_wfa_page": 60, "win_lvl2_v2_wfa_page": 61, "win_lvl3_v2_wfa_page": 62, "win_lvl4_v2_wfa_page": 63,
        "win_lvl5_page": 39}

guess_form_screens_ids={"dfa_guess_form_v1": 66, "dfa_guess_form_v1_lvl2": 67, "dfa_guess_form_v1_lvl3": 68, "dfa_guess_form_v1_lvl4": 69,
        "dfa_guess_form_v1_lvl5": 70, "dfa_guess_form_v2": 71, "dfa_guess_form_v2_lvl2": 72, "dfa_guess_form_v2_lvl3": 73, 
        "dfa_guess_form_v2_lvl4": 74, "dfa_guess_form_v2_lvl5": 75, "vpa_guess_form_v1": 77, "vpa_guess_form_v1_lvl2": 78, 
        "vpa_guess_form_v1_lvl3": 79, "vpa_guess_form_v1_lvl4": 80, "vpa_guess_form_v1_lvl5": 81, "vpa_guess_form_v2": 82,
        "vpa_guess_form_v2_lvl2": 83, "vpa_guess_form_v2_lvl3": 84, "vpa_guess_form_v2_lvl4": 85, "vpa_guess_form_v2_lvl5": 86, 
        "wfa_guess_form_v1": 88, "wfa_guess_form_v1_lvl2": 89, "wfa_guess_form_v1_lvl3": 90, "wfa_guess_form_v1_lvl4": 91,
        "wfa_guess_form_v1_lvl5": 92, "wfa_guess_form_v2": 93, "wfa_guess_form_v2_lvl2": 94, "wfa_guess_form_v2_lvl3": 95,
        "wfa_guess_form_v2_lvl4": 96, "wfa_guess_form_v2_lvl5": 97}

class MainWindow(Screen):
    pass

class SecondWindow(Screen):
    pass

class DFAChooseVersionWindow(Screen):
    def go_to_new_game(self, game_name):
        self.manager.dfa = self.manager.generator.generate_random_dfa(["a", "b"], 1, 2)
        if game_name == "game_dfa1_lvl1":
            self.manager.screens[game_screens_ids[game_name]].automaton_text = f"Please write a word in the input.\n Note, if you want to write empty word, please type epsilon.\n Tip:\n Alphabet of automaton: {self.manager.dfa.alphabet}\n States of automaton: {self.manager.dfa.states},\n Initial state of automaton: {self.manager.dfa.initial_state}"
            self.manager.screens[game_screens_ids[game_name]].answer_text = ""
        elif game_name == "game_dfa2_lvl1":
            self.manager.screens[game_screens_ids[game_name]].automaton_text = f"Please write a word and a state in the input.\n Note, if you want to write empty word, please type epsilon.\n Tip:\n Alphabet of automaton: {self.manager.dfa.alphabet}\n States of automaton: {self.manager.dfa.states},\n Initial state of automaton: {self.manager.dfa.initial_state}"
            self.manager.screens[game_screens_ids[game_name]].answer_text = ""
        self.manager.transition.direction = "right"
        self.parent.current = game_name

class VPAChooseVersionWindow(Screen):
    def go_to_new_game(self, game_name):
        self.manager.dvpa = self.manager.generator.generate_random_dvpa(["a"], ["b"], ["c"], ["Z", "A"], 1, 2)
        if game_name == "game_vpa1_lvl1":
            self.manager.screens[game_screens_ids[game_name]].automaton_text = ("Please write a word in the input.\n Note, if you want to write empty word, please type epsilon.\n"
                f"  Tip:\n Alphabets of automaton (in order calls, return, internal): {self.manager.dvpa.calls_alphabet}, {self.manager.dvpa.return_alphabet}, {self.manager.dvpa.internal_alpahbet}\n"
                f" States of automaton: {self.manager.dvpa.states}\n Initial state of automaton: {self.manager.dvpa.initial_state}\n Stack alphabet: {self.manager.dvpa.stack_alphabet}\n"
                f" Initial stack symbol: {self.manager.dvpa.initial_stack_symbol}")
            self.manager.screens[game_screens_ids[game_name]].answer_text = ""
        else:
            self.manager.screens[game_screens_ids[game_name]].automaton_text = ("Please write a word, a state and a stack in the input.\n Note, if you want to write empty word, please type epsilon.\n"
                f"  Tip:\n Alphabets of automaton (in order calls, return, internal): {self.manager.dvpa.calls_alphabet}, {self.manager.dvpa.return_alphabet}, {self.manager.dvpa.internal_alpahbet}\n"
                f" States of automaton: {self.manager.dvpa.states}\n Initial state of automaton: {self.manager.dvpa.initial_state}\n Stack alphabet: {self.manager.dvpa.stack_alphabet}\n"
                f" Initial stack symbol: {self.manager.dvpa.initial_stack_symbol}")
            self.manager.screens[game_screens_ids[game_name]].answer_text = ""
        self.manager.transition.direction = "right"
        self.parent.current = game_name

class WFAChooseVersionWindow(Screen):
    def go_to_new_game(self, game_name):
        self.manager.wfa = self.manager.generator.generate_random_dwfa(["a", "b"], 2, 1, 2)
        if game_name == "game_wfa1_lvl1":
            self.manager.screens[game_screens_ids[game_name]].automaton_text = f"Please write a word in the input.\n Note, if you want to write empty word, please type epsilon.\n Tip:\n Alphabet of automaton: {self.manager.wfa.alphabet}\n States of automaton: {self.manager.wfa.states}\n Maximal weight of automaton: 2"
            self.manager.screens[game_screens_ids[game_name]].answer_text = ""
        elif game_name == "game_wfa2_lvl1":
            self.manager.screens[game_screens_ids[game_name]].automaton_text = f"Please write a word and a state in the input.\n Note, if you want to write empty word, please type epsilon.\n Tip:\n Alphabet of automaton: {self.manager.wfa.alphabet}\n States of automaton: {self.manager.wfa.states}\n Maximal weight of automaton: 2"
            self.manager.screens[game_screens_ids[game_name]].answer_text = ""
        self.manager.transition.direction = "right"
        self.parent.current = game_name

class GameWindow(Screen):
    automaton_text = StringProperty("")
    answer_text= StringProperty("")
    button_text = StringProperty("")
    input = ObjectProperty(None)
    name = StringProperty("")
    first_label_x = NumericProperty(0)
    first_label_y = NumericProperty(0)
    guess_form_name = StringProperty("")

    def go_to_main_menu(self):
        self.manager.screens[guess_form_screens_ids[self.guess_form_name]].number_of_tries = 0
        self.input.text = ""
        self.answer_text = ""
        self.number_of_tips = 0
        self.parent.current = "second"

    def go_to_guess_form(self):
        self.input.text = ""
        self.parent.current = self.guess_form_name

class GameDFAWindow(GameWindow):
    def go_to_guess_form(self):
        self.manager.screens[guess_form_screens_ids[self.guess_form_name]].automaton_text = f"Tip:\n Alphabet of automaton: {self.manager.dfa.alphabet}\n States of automaton: {self.manager.dfa.states},\n Initial state of automaton: {self.manager.dfa.initial_state}"
        for state in self.manager.dfa.states:
            self.manager.screens[guess_form_screens_ids[self.guess_form_name]].G.add_node(state)
        super().go_to_guess_form()

class GameDFAv1Window(GameDFAWindow):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.button_text = "Check if word is in language."

    def check_word(self):
        try:
            words = self.input.text.replace(" ", "").split("\n")
            for word in words:
                print(word)
                if word == "epsilon":
                    word = ""
                for letter in word:
                    assert letter >= 'a' and letter <= 'z', f"\nError for word {word}: Only small letters are allowed."
                    assert letter in self.manager.dfa.alphabet,  f"\nError for word {word}: Letter {letter} is not in the alpahbet."
                error_idx=self.answer_text.find("Error")
                if error_idx != -1:
                    self.answer_text = self.answer_text[:error_idx-1]
                word_to_write = word if len(word) > 0 else "empty word"
                if self.manager.dfa.check_if_word_in_language(word):
                    self.answer_text += f"\nword {word_to_write} is in language"
                else:
                    self.answer_text += f"\nword {word_to_write} is not in language"
                self.input.text=""
                self.number_of_tips += 1
        except AssertionError as e:
            self.answer_text += str(e)

class GameDFAv1WindowLevel1(GameDFAv1Window):
    pass

class GameDFAv1WindowLevel2(GameDFAv1Window):
    pass

class GameDFAv1WindowLevel3(GameDFAv1Window):
    pass

class GameDFAv1WindowLevel4(GameDFAv1Window):
    pass

class GameDFAv1WindowLevel5(GameDFAv1Window):
    pass

class GameDFAv2Window(GameDFAWindow):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.button_text = "Check in which state we finish."

    def check_word(self):
        try:
            input_contents = self.input.text.split("\n")
            for input_content_string in input_contents:
                input_content = input_content_string.split()
                assert len(input_content) == 2, "\nError: You should give exactly 2 values separated by space."
                word, state = input_content[0], int(input_content[1])
                if word == "epsilon":
                    word = ""
                for letter in word:
                    assert letter in self.manager.dfa.alphabet, f"\nError for word {word}: letter {letter} is not in the alphabet."
                assert state in self.manager.dfa.states, f"\nError for state {state}: state should be a number between 0 and {len(self.manager.dfa.states) - 1}."
                end_state=self.manager.dfa.give_state_when_starting_from_given_configuration(int(state), word)
                error_idx=self.answer_text.find("Error")
                if error_idx != -1:
                    self.answer_text = self.answer_text[:error_idx-1]
                word_to_write = word if len(word) > 0 else "empty word"
                self.answer_text += f"\nWith word {word_to_write}, and state {state} we finished in state: {end_state}"
                self.input.text=""
                self.number_of_tips += 1
        except ValueError as e:
            invalid_state = str(e).split()[-1]
            self.answer_text += f"\nError: States in automaton are numbers, but you put {invalid_state} as state."
        except AssertionError as e:
            self.answer_text += str(e) 

class GameDFAv2WindowLevel1(GameDFAv2Window):
    pass

class GameDFAv2WindowLevel2(GameDFAv2Window):
    pass

class GameDFAv2WindowLevel3(GameDFAv2Window):
    pass

class GameDFAv2WindowLevel4(GameDFAv2Window):
    pass

class GameDFAv2WindowLevel5(GameDFAv2Window):
    pass

class GameVPAWindow(GameWindow):
    def go_to_guess_form(self):
        self.manager.screens[guess_form_screens_ids[self.guess_form_name]].automaton_text = (f"  Tip:\n Alphabets of automaton (in order calls, return, internal): {self.manager.dvpa.calls_alphabet}, {self.manager.dvpa.return_alphabet}, {self.manager.dvpa.internal_alpahbet}\n"
            f" States of automaton: {self.manager.dvpa.states}\n Initial state of automaton: {self.manager.dvpa.initial_state}\n Stack alphabet: {self.manager.dvpa.stack_alphabet}\n"
            f" Initial stack symbol: {self.manager.dvpa.initial_stack_symbol}"
            )
        for state in self.manager.dvpa.states:
            self.manager.screens[guess_form_screens_ids[self.guess_form_name]].G.add_node(state)
        super().go_to_guess_form()

class GameVPAv1Window(GameVPAWindow):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.button_text = "Check if word is in language."

    def check_word(self):
        try:
            words = self.input.text.replace(" ", "").split("\n")
            for word in words:
                if word == "epsilon":
                    word = ""
                for letter in word:
                    assert letter >= 'a' and letter <= 'z', f"\nError for word {word}: Only small letters are allowed."
                    assert (letter in self.manager.dvpa.calls_alphabet) or (letter in self.manager.dvpa.return_alphabet) or (letter in self.manager.dvpa.internal_alpahbet), (
                        f"\nError for word {word}: Letter {letter} is not in any alpahbet.")
                error_idx=self.answer_text.find("Error")
                if error_idx != -1:
                    self.answer_text = self.answer_text[:error_idx-1]
                word_to_write = word if len(word) > 0 else "empty word"
                if self.manager.dvpa.check_if_word_in_language(word):
                    self.answer_text += f"\nword {word_to_write} is in language"
                else:
                    self.answer_text += f"\nword {word_to_write} is not in language"
                self.input.text=""
                self.number_of_tips += 1
        except AssertionError as e:
            self.answer_text += str(e)

class GameVPAv1WindowLevel1(GameVPAv1Window):
    pass

class GameVPAv1WindowLevel2(GameVPAv1Window):
    pass

class GameVPAv1WindowLevel3(GameVPAv1Window):
    pass

class GameVPAv1WindowLevel4(GameVPAv1Window):
    pass

class GameVPAv1WindowLevel5(GameVPAv1Window):
    pass

class GameVPAv2Window(GameVPAWindow):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.button_text = "Check in which states and stacks we finish."

    def check_word(self):
        try:
            input_contents = self.input.text.split("\n")
            for input_content_string in input_contents:
                input_content = input_content_string.split()
                assert len(input_content) == 3, "\nError: You should give exactly 3 values separated by space."
                word, state, stack_string = input_content[0], int(input_content[1]), input_content[2]
                if word == "epsilon":
                    word = ""
                for letter in word:
                    assert (letter in self.manager.dvpa.calls_alphabet) or (letter in self.manager.dvpa.return_alphabet) or (letter in self.manager.dvpa.internal_alpahbet), (
                        f"\nError for word {word}: Letter {letter} is not in any alpahbet.")
                assert state in self.manager.dvpa.states, f"\nError for state {state}: state should be a number between 0 and {len(self.manager.dvpa.states) - 1}."
                for symbol in stack_string:
                    assert symbol in self.manager.dvpa.stack_alphabet, f"\nError for stack {stack_string}: Symbol {symbol} is not a part of stack alphabet."
                end_states, end_stacks=self.manager.dvpa.give_state_and_stack_when_starting_from_given_configuration(state, word, list(stack_string))
                error_idx=self.answer_text.find("Error")
                if error_idx != -1:
                    self.answer_text = self.answer_text[:error_idx-1]
                word_to_write = word if len(word) > 0 else "empty word"
                self.answer_text += f"\nWith word: {word_to_write}, state: {state}, and stack: {stack_string}, we finished in states: {end_states} and stacks: {''.join(end_stacks)}"
                self.input.text=""
                self.number_of_tips += 1
        except ValueError as e:
            invalid_state = str(e).split()[-1]
            self.answer_text += f"\nError: States in automaton are numbers, but you put {invalid_state} as state."
        except AssertionError as e:
            self.answer_text += str(e)

class GameVPAv2WindowLevel1(GameVPAv2Window):
    pass

class GameVPAv2WindowLevel2(GameVPAv2Window):
    pass

class GameVPAv2WindowLevel3(GameVPAv2Window):
    pass

class GameVPAv2WindowLevel4(GameVPAv2Window):
    pass

class GameVPAv2WindowLevel5(GameVPAv2Window):
    pass

class GameWFAWindow(GameWindow):
    max_automaton_weight=NumericProperty(0)
    def go_to_guess_form(self):
        self.manager.screens[guess_form_screens_ids[self.guess_form_name]].automaton_text = f" Tip:\n Alphabet of automaton: {self.manager.wfa.alphabet}\n States of automaton: {self.manager.wfa.states}\n Maximal weight of automaton: {self.max_automaton_weight}"
        for state in self.manager.wfa.states:
            self.manager.screens[guess_form_screens_ids[self.guess_form_name]].G.add_node(state)
        super().go_to_guess_form()

class GameWFAv1Window(GameWFAWindow):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.button_text = "Check weight of this word."

    def check_word(self):
        try:
            words = self.input.text.replace(" ", "").split("\n")
            for word in words:
                if word == "epsilon":
                    word = ""
                for letter in word:
                    assert letter in self.manager.wfa.alphabet,  f"\nError for word {word}: Letter {letter} is not in the alpahbet."
                weight = self.manager.wfa.weight_of_word(word)
                error_idx = self.answer_text.find("Error")
                if error_idx != -1:
                    self.answer_text = self.answer_text[:error_idx-1]
                word_to_write = word if len(word) > 0 else "empty word"
                self.answer_text += f"\nWeight of word {word_to_write} is {weight}"
                self.input.text=""
                self.number_of_tips += 1
        except AssertionError as e:
            self.answer_text += str(e)

class GameWFAv1WindowLevel1(GameWFAv1Window):
    pass

class GameWFAv1WindowLevel2(GameWFAv1Window):
    pass

class GameWFAv1WindowLevel3(GameWFAv1Window):
    pass

class GameWFAv1WindowLevel4(GameWFAv1Window):
    pass

class GameWFAv1WindowLevel5(GameWFAv1Window):
    pass

class GameWFAv2Window(GameWFAWindow):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.button_text = "Check in which state and weight we finish."

    def check_word(self):
        try:
            input_contents = self.input.text.split("\n")
            for input_content_string in input_contents:
                input_content = input_content_string.split()
                assert len(input_content) == 2, "\nError: You should give exactly 2 values separated by space."
                word, state = input_content[0], int(input_content[1])
                if word == "epsilon":
                    word = ""
                for letter in word:
                    assert letter in self.manager.wfa.alphabet, f"\nError for word {word}: letter {letter} is not in the alphabet."
                assert state in self.manager.wfa.states, f"\nError for state {state}: state should be a number between 0 and {len(self.manager.wfa.states) - 1}."
                end_state, path_weight=self.manager.wfa.give_state_and_weight_when_starting_from_given_configuration(int(state), word)
                error_idx = self.answer_text.find("Error")
                if error_idx != -1:
                    self.answer_text = self.answer_text[:error_idx-1]
                word_to_write = word if len(word) > 0 else "empty word"
                self.answer_text += f"\nWith word {word_to_write}, and state {state} we finished in state: {end_state} and path weight is: {path_weight}"
                self.input.text = ""
                self.number_of_tips += 1
        except ValueError as e:
            invalid_state = str(e).split()[-1]
            self.answer_text += f"\nError: States in automaton are numbers, but you put {invalid_state} as state."
        except AssertionError as e:
            self.answer_text += str(e)

class GameWFAv2WindowLevel1(GameWFAv2Window):
    pass

class GameWFAv2WindowLevel2(GameWFAv2Window):
    pass

class GameWFAv2WindowLevel3(GameWFAv2Window):
    pass

class GameWFAv2WindowLevel4(GameWFAv2Window):
    pass

class GameWFAv2WindowLevel5(GameWFAv2Window):
    pass

class DFAGuessForm(Screen):
    dfa = None
    finals_input = ObjectProperty(None)
    transitions_input = ObjectProperty(None)
    answer_text=StringProperty("")
    automaton_text = StringProperty("")
    guess_text=StringProperty("")

    def __init__(self, **kw):
        super().__init__(**kw)
        self.guess_text = ("Write final states and transitions of automaton here.\n"
                "Note: Final states should be numbers separated by a comma on one line,\n and transitions should have form: old_state, letter, new_state; each on a separate line."
                )
        self.answer_text = ""
        self.G = nx.DiGraph()

    def clear_window(self):
        self.finals_input.text = ""
        self.transitions_input.text = ""

    def check_automaton(self):
        is_correct=self.check_automaton_correctness()
        if is_correct:
            num_of_tries=copy.deepcopy(self.number_of_tries)
            self.number_of_tries = 0
            self.manager.screens[win_level_pages_ids[self.win_level_page_name]].label_text=f"Congratulations, you won with {self.manager.screens[game_screens_ids[self.last_game_name]].number_of_tips} tips and {num_of_tries} failed guesses."
            self.manager.screens[game_screens_ids[self.last_game_name]].number_of_tips = 0
            self.answer_text = ""
            self.parent.current = self.win_level_page_name
        elif is_correct is not None:
            self.number_of_tries += 1

    def go_to_tips_form(self):
        self.clear_window()
        self.answer_text = ""
        self.parent.current = self.last_game_name

    def remove_graph_from_box_layout(self):
        box_layout=self.children[0].children[-1]
        if len(box_layout.children) > 0:
            for elem in box_layout.children:
                box_layout.remove_widget(elem)

    def add_graph_to_box_layout(self):
        box_layout=self.children[0].children[-1]
        box_layout.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def read_inputs(self):
        finals_text = self.finals_input.text.replace(" ", "")
        if finals_text == "":
            finals=[]
        else:
            finals = [int(state) for state in finals_text.split(",")]
        trans_strings=self.transitions_input.text.replace(" ", "").split("\n")
        transitions={}
        for s in trans_strings:
            old_state, letter, new_state = s.split(",")
            transitions[(int(old_state), letter)] = int(new_state)
        return finals, transitions
    
    def get_edges_and_final_states_from_input(self):
        try:
            finals_text = self.finals_input.text.replace(" ", "")
            if finals_text == "":
                finals=[]
            else:
                finals = [int(state) for state in finals_text.split(",")]
            trans_strings=self.transitions_input.text.replace(" ", "").split("\n")
            edges_with_labels={}
            for s in trans_strings:
                old_state, letter, new_state = s.split(",")
                if ((int(old_state), int(new_state)) not in edges_with_labels.keys()):
                    edges_with_labels[(int(old_state), int(new_state))] = []
                edges_with_labels[(int(old_state), int(new_state))].append(letter)
            return edges_with_labels, finals, False
        except ValueError as e:
            self.answer_text = "ParseError!!!\n Note: Transitions should have form: old_state, letter, new_state; each on a separate line."
            return {}, [], True

    def draw_graph(self):
        self.answer_text = ""
        self.remove_graph_from_box_layout()
        edges_with_labels, finals, is_exception = self.get_edges_and_final_states_from_input()
        if is_exception:
            return

        for edge in edges_with_labels:
            letters = edges_with_labels[edge]
            edges_with_labels[edge] = ', '.join(letters)

        plt.clf()
        self.G.remove_edges_from(list(self.G.edges))
        for u, v in edges_with_labels.keys():
            self.G.add_edge(u, v)
        pos = nx.spring_layout(self.G)
        colours_map={}
        for final in finals:
            colours_map[final]='blue'
        values = [colours_map.get(node, 'pink') for node in self.G.nodes()]
        nx.draw(
            self.G, pos, edge_color='black', width=1, linewidths=1,
            node_size=500, node_color=values, alpha=0.9,
            labels={node: node for node in self.G.nodes()}
        )
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edges_with_labels, font_color='red')
        self.add_graph_to_box_layout()

    def check_automaton_correctness(self):
        try:
            finals, transitions = self.read_inputs()
            guessed_automaton=DFA(self.manager.dfa.alphabet, self.manager.dfa.states, 0, finals, transitions)
            is_equal, word = self.manager.dfa.is_equal_to(guessed_automaton)
            if is_equal:
                self.clear_window()
                return True
            word = word if len(word) > 0 else "empty word"
            self.answer_text = f"Your automaton does not match on word:\n {word}"
            return False
        except AssertionError as e:
            self.answer_text = f"Error: {str(e)}"
        except KeyError as e:
            self.answer_text = f"Error: Not given transition for: {e}"
        except ValueError as e:
            self.answer_text = "ParseError!!!\n Note: Final states should be numbers separated by a comma on one line,\n and transitions should have form: old_state, letter, new_state; each on a separate line."

class DFAGuessFormv1(DFAGuessForm):
    pass

class DFAGuessFormv1Level2(DFAGuessForm):
    pass

class DFAGuessFormv1Level3(DFAGuessForm):
    pass

class DFAGuessFormv1Level4(DFAGuessForm):
    pass

class DFAGuessFormv1Level5(DFAGuessForm):
    pass

class DFAGuessFormv2(DFAGuessForm):
    pass

class DFAGuessFormv2Level2(DFAGuessForm):
    pass

class DFAGuessFormv2Level3(DFAGuessForm):
    pass

class DFAGuessFormv2Level4(DFAGuessForm):
    pass

class DFAGuessFormv2Level5(DFAGuessForm):
    pass

class VPAGuessForm(Screen):
    dvpa=None
    finals_input = ObjectProperty(None)
    transitions_input = ObjectProperty(None)
    automaton_text = StringProperty("")
    answer_text = StringProperty("")
    guess_text=StringProperty("")

    def __init__(self, **kw):
        super().__init__(**kw)
        self.guess_text = ("Write final states and transitions of automaton here.\n"
                "Note: Final states should be numbers separated by a comma on one line,\n and transitions should have form: old_state, letter, new_state, stack_symbol; each on a separate line."
                )
        self.answer_text = ""
        self.G = nx.DiGraph()

    def clear_window(self):
        self.finals_input.text = ""
        self.transitions_input.text = ""

    def check_automaton(self):
        is_correct=self.check_automaton_correctness()
        if is_correct:
            num_of_tries=copy.deepcopy(self.number_of_tries)
            self.number_of_tries = 0
            self.manager.screens[win_level_pages_ids[self.win_level_page_name]].label_text=f"Congratulations, you won with {self.manager.screens[game_screens_ids[self.last_game_name]].number_of_tips} tips and {num_of_tries} failed guesses."
            self.manager.screens[game_screens_ids[self.last_game_name]].number_of_tips = 0
            self.answer_text = ""
            self.parent.current = self.win_level_page_name
        elif is_correct is not None:
            self.number_of_tries += 1

    def go_to_tips_form(self):
        self.clear_window()
        self.answer_text = ""
        self.parent.current = self.last_game_name
    
    def remove_graph_from_box_layout(self):
        box_layout=self.children[0].children[-1]
        if len(box_layout.children) > 0:
            for elem in box_layout.children:
                box_layout.remove_widget(elem)
    
    def add_graph_to_box_layout(self):
        box_layout=self.children[0].children[-1]
        box_layout.add_widget(FigureCanvasKivyAgg(plt.gcf()))
    
    def read_inputs(self):
        finals_text = self.finals_input.text.replace(" ", "")
        if finals_text == "":
            finals=[]
        else:
            finals = [int(state) for state in finals_text.split(",")]
        trans_strings=self.transitions_input.text.replace(" ", "").split("\n")
        transitions={}
        for s in trans_strings:
            old_state, letter, new_state, stack_symbol = s.split(",")
            if letter in self.manager.dvpa.calls_alphabet:
                transitions[(int(old_state), letter)] = (int(new_state), stack_symbol)
            elif letter in self.manager.dvpa.return_alphabet:
                transitions[(int(old_state), letter, stack_symbol)] = int(new_state)
            else:
                transitions[(int(old_state), letter)] = int(new_state)
        return finals, transitions

    def get_edges_and_final_states_from_input(self):
        try:
            finals_text = self.finals_input.text.replace(" ", "")
            if finals_text == "":
                finals=[]
            else:
                finals = [int(state) for state in finals_text.split(",")]
            trans_strings=self.transitions_input.text.replace(" ", "").split("\n")
            edges_with_labels={}
            for s in trans_strings:
                old_state, letter, new_state, stack_symbol = s.split(",")
                if ((int(old_state), int(new_state)) not in edges_with_labels.keys()):
                    edges_with_labels[(int(old_state), int(new_state))] = []
                edges_with_labels[(int(old_state), int(new_state))].append((letter, stack_symbol))
            return edges_with_labels, finals, False
        except ValueError as e:
            self.answer_text = "ParseError!!!\n Note: Transitions should have form: old_state, letter, new_state, stack_symbol; each on a separate line."
            return {}, [], True

    def draw_graph(self):
        self.answer_text = ""
        self.remove_graph_from_box_layout()
        edges_with_labels, finals, is_exception = self.get_edges_and_final_states_from_input()
        if is_exception:
            return
        for edge in edges_with_labels:
            letters = edges_with_labels[edge]
            edges_with_labels[edge] = ', '.join([str(letter) for letter in letters])

        plt.clf()
        self.G.remove_edges_from(list(self.G.edges))
        for u, v in edges_with_labels.keys():
            self.G.add_edge(u, v)
        pos = nx.spring_layout(self.G)
        colours_map={}
        for final in finals:
            colours_map[final]='blue'
        values = [colours_map.get(node, 'pink') for node in self.G.nodes()]
        nx.draw(
            self.G, pos, edge_color='black', width=1, linewidths=1,
            node_size=500, node_color=values, alpha=0.9,
            labels={node: node for node in self.G.nodes()}
        )
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edges_with_labels, font_color='red')
        self.add_graph_to_box_layout()

    def check_automaton_correctness(self):
        try:
            finals, transitions = self.read_inputs()
            guessed_automaton=DVPA(self.manager.dvpa.calls_alphabet, self.manager.dvpa.return_alphabet, self.manager.dvpa.internal_alpahbet, self.manager.dvpa.states, self.manager.dvpa.stack_alphabet, 0, finals, self.manager.dvpa.initial_stack_symbol, transitions)
            is_equal, word = self.manager.dvpa.is_equal_to(guessed_automaton)
            if is_equal:
                self.clear_window()
                return True
            word = word if len(word) > 0 else "empty word"
            self.answer_text = f"Your automaton does not match on word:\n {word}"
            return False
        except AssertionError as e:
            self.answer_text = f"Error: {str(e)}"
        except KeyError as e:
            self.answer_text = f"Error: Not given transition for: {e}"
        except ValueError as e:
            self.answer_text = "ParseError!!!\n Note: Final states should be numbers separated by a comma on one line,\n and transitions should have form: old_state, letter, new_state, stack_symbol; each on a separate line."

class VPAGuessFormv1(VPAGuessForm):
    pass

class VPAGuessFormv1Level2(VPAGuessForm):
    pass

class VPAGuessFormv1Level3(VPAGuessForm):
    pass

class VPAGuessFormv1Level4(VPAGuessForm):
    pass

class VPAGuessFormv1Level5(VPAGuessForm):
    pass

class VPAGuessFormv2(VPAGuessForm):
    pass
        
class VPAGuessFormv2Level2(VPAGuessForm):
    pass

class VPAGuessFormv2Level3(VPAGuessForm):
    pass
        
class VPAGuessFormv2Level4(VPAGuessForm):
    pass

class VPAGuessFormv2Level5(VPAGuessForm):
    pass

class WFAGuessForm(Screen):
    wfa = None
    initial_function_input = ObjectProperty(None)
    final_function_input = ObjectProperty(None)
    transitions_input = ObjectProperty(None)
    automaton_text = StringProperty("")
    answer_text = StringProperty("")
    guess_text = StringProperty("")

    def __init__(self, **kw):
        super().__init__(**kw)
        self.guess_text = ("Write weight functions and transitions of automaton here.\n"
                "Note: Weight functions should be in form: state, weight; each pair on a separate line\n and transitions should have form: old_state, letter, weight, new_state; each on a separate line."
                )
        self.answer_text = ""
        self.G = nx.DiGraph()

    def clear_window(self):
        self.initial_function_input.text = ""
        self.final_function_input.text = ""
        self.transitions_input.text = ""

    def check_automaton(self):
        is_correct = self.check_automaton_correctness()
        if is_correct:
            num_of_tries=copy.deepcopy(self.number_of_tries)
            self.number_of_tries = 0
            self.manager.screens[win_level_pages_ids[self.win_level_page_name]].label_text=f"Congratulations, you won with {self.manager.screens[game_screens_ids[self.last_game_name]].number_of_tips} tips and {num_of_tries} failed guesses."
            self.manager.screens[game_screens_ids[self.last_game_name]].number_of_tips = 0
            self.answer_text =""
            self.parent.current = self.win_level_page_name
        elif is_correct is not None:
            self.number_of_tries += 1

    def go_to_tips_form(self):
        self.clear_window()
        self.answer_text = ""
        self.parent.current = self.last_game_name
    
    def remove_graph_from_box_layout(self):
        box_layout=self.children[0].children[-1]
        if len(box_layout.children) > 0:
            for elem in box_layout.children:
                box_layout.remove_widget(elem)

    def add_graph_to_box_layout(self):
        box_layout=self.children[0].children[-1]
        box_layout.add_widget(FigureCanvasKivyAgg(plt.gcf()))
    
    def read_inputs(self):
        initial_function_strings = self.initial_function_input.text.replace(" ", "").split("\n")
        final_function_strings = self.final_function_input.text.replace(" ", "").split("\n")
        trans_strings=self.transitions_input.text.replace(" ", "").split("\n")
        initial_function={}
        for s in initial_function_strings:
            state, weight = s.split(",")
            initial_function[int(state)] = int(weight)
        final_function={}
        for s in final_function_strings:
            state, weight = s.split(",")
            final_function[int(state)] = int(weight)
        transitions={}
        for s in trans_strings:
            old_state, letter, weight, new_state = s.split(",")
            transitions[(int(old_state), letter)] = (int(weight), int(new_state))
        return initial_function, final_function, transitions

    def get_edges_from_input(self):
        try:
            trans_strings=self.transitions_input.text.replace(" ", "").split("\n")
            edges_with_labels={}
            for s in trans_strings:
                old_state, letter, weight, new_state = s.split(",")
                if ((int(old_state), int(new_state)) not in edges_with_labels.keys()):
                    edges_with_labels[(int(old_state), int(new_state))] = []
                edges_with_labels[(int(old_state), int(new_state))].append((letter, weight))
            return edges_with_labels, False
        except ValueError as e:
            self.answer_text = "ParseError!!!\n Note: Transitions should have form: old_state, letter, weight, new_state; each on a separate line."
            return {}, True

    def draw_graph(self):
        self.answer_text = ""
        self.remove_graph_from_box_layout()
        edges_with_labels, is_exception = self.get_edges_from_input()
        if is_exception:
            return
        for edge in edges_with_labels:
            letters = edges_with_labels[edge]
            edges_with_labels[edge] = ', '.join([str(letter) for letter in letters])

        plt.clf()
        self.G.remove_edges_from(list(self.G.edges))
        for u, v in edges_with_labels.keys():
            self.G.add_edge(u, v)
        pos = nx.spring_layout(self.G)
        nx.draw(
            self.G, pos, edge_color='black', width=1, linewidths=1,
            node_size=500, node_color='pink', alpha=0.9,
            labels={node: node for node in self.G.nodes()}
        )
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edges_with_labels, font_color='red')
        self.add_graph_to_box_layout()

    def check_automaton_correctness(self):
        try:
            initial_function, final_function, transitions = self.read_inputs()
            guessed_automaton=DWFA(self.manager.wfa.alphabet, self.manager.wfa.states, initial_function, final_function, transitions)
            is_equal, word = self.manager.wfa.is_equal_to(guessed_automaton)
            if is_equal:
                self.clear_window()
                return True
            word = word if len(word) > 0 else "empty word"
            self.answer_text = f"Your automaton does not match on word:\n {word}"
            return False
        except AssertionError as e:
            self.answer_text = f"Error: {str(e)}"
        except KeyError as e:
            self.answer_text = f"Error: Not given transition for: {e}"
        except ValueError as e:
            self.answer_text = f"ParseError!!!\n Note: Weight functions should be in form: state, weight; each pair on a separate line\n and transitions should have form: old_state, letter, weight, new_state; each on a separate line."

class WFAGuessFormv1(WFAGuessForm):
    pass

class WFAGuessFormv1Level2(WFAGuessForm):
    pass

class WFAGuessFormv1Level3(WFAGuessForm):
    pass

class WFAGuessFormv1Level4(WFAGuessForm):
    pass

class WFAGuessFormv1Level5(WFAGuessForm):
    pass

class WFAGuessFormv2(WFAGuessForm):
    pass

class WFAGuessFormv2Level2(WFAGuessForm):
    pass

class WFAGuessFormv2Level3(WFAGuessForm):
    pass

class WFAGuessFormv2Level4(WFAGuessForm):
    pass

class WFAGuessFormv2Level5(WFAGuessForm):
    pass

class WinLevelPage(Screen):
    next_page=StringProperty("")
    label_text=StringProperty("")
    button_text=StringProperty("")
    def go_to_next_level(self):
        self.parent.current = self.next_page
        self.manager.transition.direction = "left"

class WinLevel1Page(WinLevelPage):
    pass

class WinLevel2Page(WinLevelPage):
    pass

class WinLevel3Page(WinLevelPage):
    pass

class WinLevel4Page(WinLevelPage):
    pass

class WinLevel5Page(WinLevelPage):
    pass

class WinLevel1v1DFAPage(WinLevel1Page):
    def go_to_next_level(self):
        self.manager.dfa = self.manager.generator.generate_random_dfa(["a", "b"], 2, 4)
        self.manager.screens[game_screens_ids[self.next_page]].automaton_text = f"Please write a word in the input.\n Note, if you want to write empty word, please type epsilon.\nTip:\n Alphabet of automaton: {self.manager.dfa.alphabet}\n States of automaton: {self.manager.dfa.states},\n Initial state of automaton: {self.manager.dfa.initial_state}"
        self.manager.screens[game_screens_ids[self.next_page]].answer_text = ""
        super().go_to_next_level()

class WinLevel2v1DFAPage(WinLevel2Page):
    def go_to_next_level(self):
        self.manager.dfa = self.manager.generator.generate_random_dfa(["a", "b"], 4, 6)
        self.manager.screens[game_screens_ids[self.next_page]].automaton_text = f"Please write a word in the input.\n Note, if you want to write empty word, please type epsilon.\nTip:\n Alphabet of automaton: {self.manager.dfa.alphabet}\n States of automaton: {self.manager.dfa.states},\n Initial state of automaton: {self.manager.dfa.initial_state}"
        self.manager.screens[game_screens_ids[self.next_page]].answer_text = ""
        super().go_to_next_level()

class WinLevel3v1DFAPage(WinLevel3Page):
    def go_to_next_level(self):
        self.manager.dfa = self.manager.generator.generate_random_dfa(["a", "b"], 6, 8)
        self.manager.screens[game_screens_ids[self.next_page]].automaton_text = f"Please write a word in the input.\n Note, if you want to write empty word, please type epsilon.\nTip:\n Alphabet of automaton: {self.manager.dfa.alphabet}\n States of automaton: {self.manager.dfa.states},\n Initial state of automaton: {self.manager.dfa.initial_state}"
        self.manager.screens[game_screens_ids[self.next_page]].answer_text = ""
        super().go_to_next_level()

class WinLevel4v1DFAPage(WinLevel4Page):
    def go_to_next_level(self):
        self.manager.dfa = self.manager.generator.generate_random_dfa(["a", "b"], 8, 10)
        self.manager.screens[game_screens_ids[self.next_page]].automaton_text = f"Please write a word in the input.\n Note, if you want to write empty word, please type epsilon.\n Tip:\n Alphabet of automaton: {self.manager.dfa.alphabet}\n States of automaton: {self.manager.dfa.states},\n Initial state of automaton: {self.manager.dfa.initial_state}"
        self.manager.screens[game_screens_ids[self.next_page]].answer_text = ""
        super().go_to_next_level()

class WinLevel1v2DFAPage(WinLevel1Page):
    def go_to_next_level(self):
        self.manager.dfa = self.manager.generator.generate_random_dfa(["a", "b"], 2, 4)
        self.manager.screens[game_screens_ids[self.next_page]].automaton_text = f"Please write a word and a state in the input.\n Note, if you want to write empty word, please type epsilon.\n Tip:\n Alphabet of automaton: {self.manager.dfa.alphabet}\n States of automaton: {self.manager.dfa.states},\n Initial state of automaton: {self.manager.dfa.initial_state}"
        self.manager.screens[game_screens_ids[self.next_page]].answer_text = ""
        super().go_to_next_level()

class WinLevel2v2DFAPage(WinLevel2Page):
    def go_to_next_level(self):
        self.manager.dfa = self.manager.generator.generate_random_dfa(["a", "b"], 4, 6)
        self.manager.screens[game_screens_ids[self.next_page]].automaton_text = f"Please write a word and a state in the input.\n Note, if you want to write empty word, please type epsilon.\n Tip:\n Alphabet of automaton: {self.manager.dfa.alphabet}\n States of automaton: {self.manager.dfa.states},\n Initial state of automaton: {self.manager.dfa.initial_state}"
        self.manager.screens[game_screens_ids[self.next_page]].answer_text = ""
        super().go_to_next_level()

class WinLevel3v2DFAPage(WinLevel3Page):
    def go_to_next_level(self):
        self.manager.dfa = self.manager.generator.generate_random_dfa(["a", "b"], 6, 8)
        self.manager.screens[game_screens_ids[self.next_page]].automaton_text = f"Please write a word and a state in the input.\n Note, if you want to write empty word, please type epsilon.\n Tip:\n Alphabet of automaton: {self.manager.dfa.alphabet}\n States of automaton: {self.manager.dfa.states},\n Initial state of automaton: {self.manager.dfa.initial_state}"
        self.manager.screens[game_screens_ids[self.next_page]].answer_text = ""
        super().go_to_next_level()

class WinLevel4v2DFAPage(WinLevel4Page):
    def go_to_next_level(self):
        self.manager.dfa = self.manager.generator.generate_random_dfa(["a", "b"], 8, 10)
        self.manager.screens[game_screens_ids[self.next_page]].automaton_text = f"Please write a word and a state in the input.\n Note, if you want to write empty word, please type epsilon.\n Tip:\n Alphabet of automaton: {self.manager.dfa.alphabet}\n States of automaton: {self.manager.dfa.states},\n Initial state of automaton: {self.manager.dfa.initial_state}"
        self.manager.screens[game_screens_ids[self.next_page]].answer_text = ""
        super().go_to_next_level()

class WinLevel1v1VPAPage(WinLevel1Page):
    def go_to_next_level(self):
        self.manager.dvpa = self.manager.generator.generate_random_dvpa(["a"], ["b"], ["c"], ["Z", "A"], 2, 4)
        self.manager.screens[game_screens_ids[self.next_page]].automaton_text =  ("Please write a word in the input.\n Note, if you want to write empty word, please type epsilon.\n"
            f"  Tip:\n Alphabets of automaton (in order calls, return, internal): {self.manager.dvpa.calls_alphabet}, {self.manager.dvpa.return_alphabet}, {self.manager.dvpa.internal_alpahbet}\n"
            f" States of automaton: {self.manager.dvpa.states}\n Initial state of automaton: {self.manager.dvpa.initial_state}\n Stack alphabet: {self.manager.dvpa.stack_alphabet}\n"
            f" Initial stack symbol: {self.manager.dvpa.initial_stack_symbol}")
        self.manager.screens[game_screens_ids[self.next_page]].answer_text = ""
        super().go_to_next_level()

class WinLevel2v1VPAPage(WinLevel2Page):
    def go_to_next_level(self):
        self.manager.dvpa = self.manager.generator.generate_random_dvpa(["a"], ["b"], ["c"], ["Z", "A"], 4, 6)
        self.manager.screens[game_screens_ids[self.next_page]].automaton_text =  ("Please write a word in the input.\n Note, if you want to write empty word, please type epsilon.\n"
            f"  Tip:\n Alphabets of automaton (in order calls, return, internal): {self.manager.dvpa.calls_alphabet}, {self.manager.dvpa.return_alphabet}, {self.manager.dvpa.internal_alpahbet}\n"
            f" States of automaton: {self.manager.dvpa.states}\n Initial state of automaton: {self.manager.dvpa.initial_state}\n Stack alphabet: {self.manager.dvpa.stack_alphabet}\n"
            f" Initial stack symbol: {self.manager.dvpa.initial_stack_symbol}")
        self.manager.screens[game_screens_ids[self.next_page]].answer_text = ""
        super().go_to_next_level()

class WinLevel3v1VPAPage(WinLevel3Page):
    def go_to_next_level(self):
        self.manager.dvpa = self.manager.generator.generate_random_dvpa(["a"], ["b"], ["c"], ["Z", "A"], 6, 8)
        self.manager.screens[game_screens_ids[self.next_page]].automaton_text =  ("Please write a word in the input.\n Note, if you want to write empty word, please type epsilon.\n"
            f"  Tip:\n Alphabets of automaton (in order calls, return, internal): {self.manager.dvpa.calls_alphabet}, {self.manager.dvpa.return_alphabet}, {self.manager.dvpa.internal_alpahbet}\n"
            f" States of automaton: {self.manager.dvpa.states}\n Initial state of automaton: {self.manager.dvpa.initial_state}\n Stack alphabet: {self.manager.dvpa.stack_alphabet}\n"
            f" Initial stack symbol: {self.manager.dvpa.initial_stack_symbol}")
        self.manager.screens[game_screens_ids[self.next_page]].answer_text = ""
        super().go_to_next_level()

class WinLevel4v1VPAPage(WinLevel4Page):
    def go_to_next_level(self):
        self.manager.dvpa = self.manager.generator.generate_random_dvpa(["a"], ["b"], ["c"], ["Z", "A"], 8, 10)
        self.manager.screens[game_screens_ids[self.next_page]].automaton_text =  ("Please write a word in the input.\n Note, if you want to write empty word, please type epsilon.\n"
            f"  Tip:\n Alphabets of automaton (in order calls, return, internal): {self.manager.dvpa.calls_alphabet}, {self.manager.dvpa.return_alphabet}, {self.manager.dvpa.internal_alpahbet}\n"
            f" States of automaton: {self.manager.dvpa.states}\n Initial state of automaton: {self.manager.dvpa.initial_state}\n Stack alphabet: {self.manager.dvpa.stack_alphabet}\n"
            f" Initial stack symbol: {self.manager.dvpa.initial_stack_symbol}")
        self.manager.screens[game_screens_ids[self.next_page]].answer_text = ""
        super().go_to_next_level()

class WinLevel1v2VPAPage(WinLevel1Page):
    def go_to_next_level(self):
        self.manager.dvpa = self.manager.generator.generate_random_dvpa(["a"], ["b"], ["c"], ["Z", "A"], 2, 4)
        self.manager.screens[game_screens_ids[self.next_page]].automaton_text = ("Please write a word, a state and a stack in the input.\n Note, if you want to write empty word, please type epsilon.\n"
            f"  Tip:\n Alphabets of automaton (in order calls, return, internal): {self.manager.dvpa.calls_alphabet}, {self.manager.dvpa.return_alphabet}, {self.manager.dvpa.internal_alpahbet}\n"
            f" States of automaton: {self.manager.dvpa.states}\n Initial state of automaton: {self.manager.dvpa.initial_state}\n Stack alphabet: {self.manager.dvpa.stack_alphabet}\n"
            f" Initial stack symbol: {self.manager.dvpa.initial_stack_symbol}")
        self.manager.screens[game_screens_ids[self.next_page]].answer_text = ""
        super().go_to_next_level()

class WinLevel2v2VPAPage(WinLevel2Page):
    def go_to_next_level(self):
        self.manager.dvpa = self.manager.generator.generate_random_dvpa(["a"], ["b"], ["c"], ["Z", "A"], 4, 6)
        self.manager.screens[game_screens_ids[self.next_page]].automaton_text = ("Please write a word, a state and a stack in the input.\n Note, if you want to write empty word, please type epsilon.\n"
            f"  Tip:\n Alphabets of automaton (in order calls, return, internal): {self.manager.dvpa.calls_alphabet}, {self.manager.dvpa.return_alphabet}, {self.manager.dvpa.internal_alpahbet}\n"
            f" States of automaton: {self.manager.dvpa.states}\n Initial state of automaton: {self.manager.dvpa.initial_state}\n Stack alphabet: {self.manager.dvpa.stack_alphabet}\n"
            f" Initial stack symbol: {self.manager.dvpa.initial_stack_symbol}")
        self.manager.screens[game_screens_ids[self.next_page]].answer_text = ""
        super().go_to_next_level()

class WinLevel3v2VPAPage(WinLevel3Page):
    def go_to_next_level(self):
        self.manager.dvpa = self.manager.generator.generate_random_dvpa(["a"], ["b"], ["c"], ["Z", "A"], 6, 8)
        self.manager.screens[game_screens_ids[self.next_page]].automaton_text = ("Please write a word, a state and a stack in the input.\n Note, if you want to write empty word, please type epsilon.\n"
            f"  Tip:\n Alphabets of automaton (in order calls, return, internal): {self.manager.dvpa.calls_alphabet}, {self.manager.dvpa.return_alphabet}, {self.manager.dvpa.internal_alpahbet}\n"
            f" States of automaton: {self.manager.dvpa.states}\n Initial state of automaton: {self.manager.dvpa.initial_state}\n Stack alphabet: {self.manager.dvpa.stack_alphabet}\n"
            f" Initial stack symbol: {self.manager.dvpa.initial_stack_symbol}")
        self.manager.screens[game_screens_ids[self.next_page]].answer_text = ""
        super().go_to_next_level()

class WinLevel4v2VPAPage(WinLevel4Page):
    def go_to_next_level(self):
        self.manager.dvpa = self.manager.generator.generate_random_dvpa(["a"], ["b"], ["c"], ["Z", "A"], 8, 10)
        self.manager.screens[game_screens_ids[self.next_page]].automaton_text = ("Please write a word, a state and a stack in the input.\n Note, if you want to write empty word, please type epsilon.\n"
            f"  Tip:\n Alphabets of automaton (in order calls, return, internal): {self.manager.dvpa.calls_alphabet}, {self.manager.dvpa.return_alphabet}, {self.manager.dvpa.internal_alpahbet}\n"
            f" States of automaton: {self.manager.dvpa.states}\n Initial state of automaton: {self.manager.dvpa.initial_state}\n Stack alphabet: {self.manager.dvpa.stack_alphabet}\n"
            f" Initial stack symbol: {self.manager.dvpa.initial_stack_symbol}")
        self.manager.screens[game_screens_ids[self.next_page]].answer_text = ""
        super().go_to_next_level()

class WinLevel1v1WFAPage(WinLevel1Page):
    def go_to_next_level(self):
        self.manager.wfa = self.manager.generator.generate_random_dwfa(["a", "b"], 5, 2, 4)
        self.manager.screens[game_screens_ids[self.next_page]].automaton_text = f"Please write a word in the input.\n Note, if you want to write empty word, please type epsilon.\n Tip:\n Alphabet of automaton: {self.manager.wfa.alphabet}\n States of automaton: {self.manager.wfa.states}\n Maximal weight of automaton: 5"
        self.manager.screens[game_screens_ids[self.next_page]].answer_text = ""
        super().go_to_next_level()

class WinLevel2v1WFAPage(WinLevel2Page):
    def go_to_next_level(self):
        self.manager.wfa = self.manager.generator.generate_random_dwfa(["a", "b"], 10, 4, 6)
        self.manager.screens[game_screens_ids[self.next_page]].automaton_text = f"Please write a word in the input.\n Note, if you want to write empty word, please type epsilon.\n Tip:\n Alphabet of automaton: {self.manager.wfa.alphabet}\n States of automaton: {self.manager.wfa.states}\n Maximal weight of automaton: 10"
        self.manager.screens[game_screens_ids[self.next_page]].answer_text = ""
        super().go_to_next_level()

class WinLevel3v1WFAPage(WinLevel3Page):
    def go_to_next_level(self):
        self.manager.wfa = self.manager.generator.generate_random_dwfa(["a", "b"], 15, 6, 8)
        self.manager.screens[game_screens_ids[self.next_page]].automaton_text = f"Please write a word in the input.\n Note, if you want to write empty word, please type epsilon.\n Tip:\n Alphabet of automaton: {self.manager.wfa.alphabet}\n States of automaton: {self.manager.wfa.states}\n Maximal weight of automaton: 15"
        self.manager.screens[game_screens_ids[self.next_page]].answer_text = ""
        super().go_to_next_level()

class WinLevel4v1WFAPage(WinLevel4Page):
    def go_to_next_level(self):
        self.manager.wfa = self.manager.generator.generate_random_dwfa(["a", "b"], 20, 8, 10)
        self.manager.screens[game_screens_ids[self.next_page]].automaton_text = f"Please write a word in the input.\n Note, if you want to write empty word, please type epsilon.\n Tip:\n Alphabet of automaton: {self.manager.wfa.alphabet}\n States of automaton: {self.manager.wfa.states}\n Maximal weight of automaton: 20"
        self.manager.screens[game_screens_ids[self.next_page]].answer_text = ""
        super().go_to_next_level()

class WinLevel1v2WFAPage(WinLevel1Page):
    def go_to_next_level(self):
        self.manager.wfa = self.manager.generator.generate_random_dwfa(["a", "b"], 5, 2, 4)
        self.manager.screens[game_screens_ids[self.next_page]].automaton_text = f"Please write a word and a state in the input.\n Note, if you want to write empty word, please type epsilon.\n Tip:\n Alphabet of automaton: {self.manager.wfa.alphabet}\n States of automaton: {self.manager.wfa.states}\n Maximal weight of automaton: 5"
        self.manager.screens[game_screens_ids[self.next_page]].answer_text = ""
        super().go_to_next_level()

class WinLevel2v2WFAPage(WinLevel2Page):
    def go_to_next_level(self):
        self.manager.wfa = self.manager.generator.generate_random_dwfa(["a", "b"], 10, 4, 6)
        self.manager.screens[game_screens_ids[self.next_page]].automaton_text = f"Please write a word and a state in the input.\n Note, if you want to write empty word, please type epsilon.\n Tip:\n Alphabet of automaton: {self.manager.wfa.alphabet}\n States of automaton: {self.manager.wfa.states}\n Maximal weight of automaton: 10"
        self.manager.screens[game_screens_ids[self.next_page]].answer_text = ""
        super().go_to_next_level()

class WinLevel3v2WFAPage(WinLevel3Page):
    def go_to_next_level(self):
        self.manager.wfa = self.manager.generator.generate_random_dwfa(["a", "b"], 15, 6, 8)
        self.manager.screens[game_screens_ids[self.next_page]].automaton_text = f"Please write a word and a state in the input.\n Note, if you want to write empty word, please type epsilon.\n Tip:\n Alphabet of automaton: {self.manager.wfa.alphabet}\n States of automaton: {self.manager.wfa.states}\n Maximal weight of automaton: 15"
        self.manager.screens[game_screens_ids[self.next_page]].answer_text = ""
        super().go_to_next_level()

class WinLevel4v2WFAPage(WinLevel4Page):
    def go_to_next_level(self):
        self.manager.wfa = self.manager.generator.generate_random_dwfa(["a", "b"], 20, 8, 10)
        self.manager.screens[game_screens_ids[self.next_page]].automaton_text = f"Please write a word and a state in the input.\n Note, if you want to write empty word, please type epsilon.\n Tip:\n Alphabet of automaton: {self.manager.wfa.alphabet}\n States of automaton: {self.manager.wfa.states}\n Maximal weight of automaton: 20"
        self.manager.screens[game_screens_ids[self.next_page]].answer_text = ""
        super().go_to_next_level()

class WindowManager(ScreenManager):
    dfa = ObjectProperty(None)
    dvpa = ObjectProperty(None)
    wfa = ObjectProperty(None)
    generator = Automata_generator()

kv = Builder.load_file("Game.kv")

class GameApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    GameApp().run()
