from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from DFA import DFA, NFA
from VPA import DVPA


#TODO:
#1. Think of informing player about stack alpahabet in VPA
#2. Reload of window after passing wrong automata, should clear this window.
#3. Create levels
#4. Think what should be done after passing wrong automata
#5. Think about other asserts
#6. Make clean-up
# And of course make huge tests for everything

class MainWindow(Screen):
    pass


class SecondWindow(Screen):
    pass

class GameWindow(Screen):
    automata_text = StringProperty("")
    button_text = StringProperty("")
    input = ObjectProperty(None)
    name = StringProperty("")
    first_label_x = NumericProperty(0)
    first_label_y = NumericProperty(0)
    second_label_x = NumericProperty(0)
    second_label_y = NumericProperty(0)
    guess_form_name = StringProperty("")


class GameDFAv1Window(GameWindow):
    dfa=DFA(["a", "b"], [0, 1, 2, 3], 0, [3], {(0, "a") : 1, (0, "b") : 1, (1, "a") : 2, (1, "b") : 2, 
        (2, "a") : 3, (2, "b") : 3, (3, "a") : 3, (3, "b") : 3})
    
    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = "Please write a word in the input."
        self.button_text = "Check if this word is in language."
        self.tip_text= f"Tip: Alphabet is {self.dfa.alphabet} and automata has {len(self.dfa.states)} states"

    def check_if_word_in_language(self):
        try:
            word = self.input.text
            for letter in word:
                assert letter in self.dfa.alphabet,  f"Error: Letter {letter} is not in the alpahbet."
            if self.dfa.check_if_word_in_language(word):
                self.automata_text = f"word {word} is in language"
            else:
                self.automata_text = f"word {word} is not in language"
            self.input.text=""
        except AssertionError as e:
            self.automata_text = str(e)
class GameDFAv2Window(GameWindow):
    dfa=DFA(["a", "b"], [0, 1, 2, 3], 0, [3], {(0, "a") : 1, (0, "b") : 1, (1, "a") : 2, (1, "b") : 2, 
        (2, "a") : 3, (2, "b") : 3, (3, "a") : 3, (3, "b") : 3})
    
    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = "Please write a word and a state in the input."
        self.button_text = "Check in which state we will finish."
        self.tip_text= f"Tip: Alphabet is {self.dfa.alphabet} and automata has {len(self.dfa.states)} states"


    def check_if_word_in_language(self):
        try:
            input_content = self.input.text.split()
            assert len(input_content) == 2, "Error: You should give exactly 2 values separated by space."
            word, state = input_content[0], int(input_content[1])
            for letter in word:
                assert letter in self.dfa.alphabet, f"Error: letter {letter} is not in the alphabet."
            assert state in self.dfa.states, f"Error: state should be a number between 0 and {len(self.dfa.states) - 1}."
            end_state=self.dfa.give_state_when_starting_from_given_configuration(int(state), word)
            self.automata_text = f"We finished in state: {end_state}"
            self.input.text=""
        except ValueError as e:
            invalid_state = str(e).split()[-1]
            self.automata_text = f"Error: States in automata are numbers, but you put {invalid_state} as state."
        except AssertionError as e:
            self.automata_text = str(e) 

class GameNFAv1Window(GameWindow):
    nfa = NFA(["a", "b"], [0, 1], 0, [1], 
        [(0, "a", 0), (0, "b", 0), (0, "b", 1)])

    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = "Please write a word in the input."
        self.button_text = "Check if this word is in language."
        self.tip_text= f"Tip: Alphabet is {self.nfa.alphabet} and automata has {len(self.nfa.states)} states"

    def check_if_word_in_language(self):
        try:
            word = self.input.text
            for letter in word:
                assert letter in self.nfa.alphabet,  f"Error: Letter {letter} is not in the alpahbet."
            if self.nfa.check_if_word_in_language(word):
                self.automata_text = f"word {word} is in language"
            else:
                self.automata_text = f"word {word} is not in language"
            self.input.text=""
        except AssertionError as e:
            self.automata_text = str(e)

class GameNFAv2Window(GameWindow):
    nfa = NFA(["a", "b"], [0, 1], 0, [1], 
        [(0, "a", 0), (0, "b", 0), (0, "b", 1)])
    
    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = "Please write a word and a state in the input."
        self.button_text = "Check in which states we will finish."
        self.tip_text= f"Tip: Alphabet is {self.nfa.alphabet} and automata has {len(self.nfa.states)} states"

    def check_if_word_in_language(self):
        try:
            input_content = self.input.text.split()
            assert len(input_content) == 2, "Error: You should give exactly 2 values separated by space."
            word, state = input_content[0], int(input_content[1])
            for letter in word:
                assert letter in self.nfa.alphabet, f"Error: letter {letter} is not in the alphabet."
            assert state in self.nfa.states, f"Error: state should be a number between 0 and {len(self.nfa.states) - 1}."
            end_states=self.nfa.give_states_when_starting_from_given_configuration(state, word)
            self.automata_text = f"We finished in states: {end_states}"
            self.input.text=""
        except ValueError as e:
            invalid_state = str(e).split()[-1]
            self.automata_text = f"Error: States in automata are numbers, but you put {invalid_state} as state."
        except AssertionError as e:
            self.automata_text = str(e) 

class GameVPAv1Window(GameWindow):
    dvpa=DVPA(["a"], ["b"], ["c"], [0, 1], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 1, (0, "b", "Z"): 1, 
            (0, "c"): 1, (1, "a"): (0, "A"), (1, "b", "A"): 0, (1, "b", "Z"): 0, (1, "c"): 0})
    
    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = "Please write a word in the input."
        self.button_text = "Check if this word is in language."
        self.tip_text= f"Tip: Automata has {len(self.dvpa.states)} states, and alphabets are {self.dvpa.calls_alphabet}, {self.dvpa.return_alphabet} and {self.dvpa.internal_alpahbet}"

    def check_if_word_in_language(self):
        try:
            word = self.input.text
            for letter in word:
                assert (letter in self.dvpa.calls_alphabet) or (letter in self.dvpa.return_alphabet) or (letter in self.dvpa.internal_alpahbet), (
                    f"Error: Letter {letter} is not in any alpahbet.")
            if self.dvpa.check_if_word_in_language(word):
                self.automata_text = f"word {word} is in language"
            else:
                self.automata_text = f"word {word} is not in language"
            self.input.text=""
        except AssertionError as e:
            self.automata_text = str(e)

class GameVPAv2Window(GameWindow):
    dvpa=DVPA(["a"], ["b"], ["c"], [0, 1], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 1, (0, "b", "Z"): 1, 
            (0, "c"): 1, (1, "a"): (0, "A"), (1, "b", "A"): 0, (1, "b", "Z"): 0, (1, "c"): 0})
    
    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = "Please write a word, a state and a stack in the input."
        self.button_text = "Check in which states and stacks we will finish."
        self.tip_text= f"Tip: Automata has {len(self.dvpa.states)} states, and alphabets are {self.dvpa.calls_alphabet}, {self.dvpa.return_alphabet} and {self.dvpa.internal_alpahbet}"

    def check_if_word_in_language(self):
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
            self.automata_text = f"We finished in states: {end_states} and stacks: {end_stacks}"
            self.input.text=""
        except ValueError as e:
            invalid_state = str(e).split()[-1]
            self.automata_text = f"Error: States in automata are numbers, but you put {invalid_state} as state."
        except AssertionError as e:
            self.automata_text = str(e)

class GameVPAv3Window(GameWindow):
    dvpa=DVPA(["a"], ["b"], ["c"], [0, 1], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 1, (0, "b", "Z"): 1, 
            (0, "c"): 1, (1, "a"): (0, "A"), (1, "b", "A"): 0, (1, "b", "Z"): 0, (1, "c"): 0})
    
    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = "Please write a word, a state and a stack in the input."
        self.button_text = "Check in which states we will finish."
        self.tip_text= f"Tip: Automata has {len(self.dvpa.states)} states, and alphabets are {self.dvpa.calls_alphabet}, {self.dvpa.return_alphabet} and {self.dvpa.internal_alpahbet}"

    def check_if_word_in_language(self):
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
            self.automata_text = f"We finished in states: {end_states}"
            self.input.text=""
        except ValueError as e:
            invalid_state = str(e).split()[-1]
            self.automata_text = f"Error: States in automata are numbers, but you put {invalid_state} as state."
        except AssertionError as e:
            self.automata_text = str(e)

class GameVPAv4Window(GameWindow):
    dvpa=DVPA(["a"], ["b"], ["c"], [0, 1], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 1, (0, "b", "Z"): 1, 
            (0, "c"): 1, (1, "a"): (0, "A"), (1, "b", "A"): 0, (1, "b", "Z"): 0, (1, "c"): 0})
    
    def __init__(self, **kw):
        super().__init__(**kw)
        self.automata_text = "Please write a word, a state and a stack in the input."
        self.button_text = "Check in which stacks we will finish."
        self.tip_text= f"Tip: Automata has {len(self.dvpa.states)} states, and alphabets are {self.dvpa.calls_alphabet}, {self.dvpa.return_alphabet} and {self.dvpa.internal_alpahbet}"

    def check_if_word_in_language(self):
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
            self.automata_text = f"We finished in stacks: {end_stacks}"
            self.input.text=""
        except ValueError as e:
            invalid_state = str(e).split()[-1]
            self.automata_text = f"Error: States in automata are numbers, but you put {invalid_state} as state."
        except AssertionError as e:
            self.automata_text = str(e)

class DFAGuessForm(Screen):
    dfa=DFA(["a", "b"], [0, 1, 2, 3], 0, [3], {(0, "a") : 1, (0, "b") : 1, (1, "a") : 2, (1, "b") : 2, 
        (2, "a") : 3, (2, "b") : 3, (3, "a") : 3, (3, "b") : 3})
    finals_input = ObjectProperty(None)
    transitions_input = ObjectProperty(None)
    last_game_name = StringProperty("")
    def check_automata_correctness(self):
        try:
            finals = [int(state) for state in self.finals_input.text.split(", ")]
            trans_strings=self.transitions_input.text.split("\n")
            transitions={}
            for s in trans_strings:
                old_state, letter, new_state = s.split(", ")
                transitions[(int(old_state), letter)] = int(new_state)
            guessed_automata=DFA(self.dfa.alphabet, self.dfa.states, 0, finals, transitions)
            self.finals_input.text = ""
            self.transitions_input.text = ""
            return self.dfa.is_equal_to(guessed_automata)
        except:
            return False

class DFAGuessFormv1(DFAGuessForm):
    def __init__(self, **kw):
        super().__init__(**kw)

class DFAGuessFormv2(DFAGuessForm):
    def __init__(self, **kw):
        super().__init__(**kw)

class NFAGuessForm(Screen):
    nfa = NFA(["a", "b"], [0, 1], 0, [1], 
        [(0, "a", 0), (0, "b", 0), (0, "b", 1)])
    finals_input = ObjectProperty(None)
    transitions_input = ObjectProperty(None)
    last_game_name = StringProperty("")
    def check_automata_correctness(self):
        try:
            finals = [int(state) for state in self.finals_input.text.split(", ")]
            trans_strings=self.transitions_input.text.split("\n")
            transitions=[]
            for s in trans_strings:
                old_state, letter, new_state = s.split(", ")
                transitions.append((int(old_state), letter, int(new_state)))
            guessed_automata=NFA(self.nfa.alphabet, self.nfa.states, 0, finals, transitions)
            self.finals_input.text = ""
            self.transitions_input.text = ""
            return self.nfa.is_equal_to(guessed_automata)
        except:
            return False

class NFAGuessFormv1(NFAGuessForm):
    def __init__(self, **kw):
        super().__init__(**kw)

class NFAGuessFormv2(NFAGuessForm):
    def __init__(self, **kw):
        super().__init__(**kw)

class VPAGuessForm(Screen):
    dvpa=DVPA(["a"], ["b"], ["c"], [0, 1], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 1, (0, "b", "Z"): 1, 
            (0, "c"): 1, (1, "a"): (0, "A"), (1, "b", "A"): 0, (1, "b", "Z"): 0, (1, "c"): 0})
    ini_stack_input = ObjectProperty(None)
    stack_input = ObjectProperty(None)
    finals_input = ObjectProperty(None)
    transitions_input = ObjectProperty(None)
    def check_automata_correctness(self):
        try:
            initial_stack_symbol = self.ini_stack_input.text
            stack_alphabet = self.stack_input.text.split(", ")
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
            guessed_automata=DVPA(self.dvpa.calls_alphabet, self.dvpa.return_alphabet, self.dvpa.internal_alpahbet, self.dvpa.states, stack_alphabet, 0, finals, initial_stack_symbol, transitions)
            self.ini_stack_input.text = ""
            self.stack_input.text = ""
            self.finals_input.text = ""
            self.transitions_input.text = ""
            return self.dvpa.is_equal_to(guessed_automata)
        except:
            return False

class VPAGuessFormv1(VPAGuessForm):
    def __init__(self, **kw):
        super().__init__(**kw)

class VPAGuessFormv2(VPAGuessForm):
    def __init__(self, **kw):
        super().__init__(**kw)

class VPAGuessFormv3(VPAGuessForm):
    def __init__(self, **kw):
        super().__init__(**kw)

class VPAGuessFormv4(VPAGuessForm):
    def __init__(self, **kw):
        super().__init__(**kw)

class WinPage(Screen):
    pass

class LosePage(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("Game.kv")


class GameApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    GameApp().run()
