import pytest
from DFA import DFA, NFA

def test_check_if_word_in_language():
    dfa1=DFA(["a", "b"], [0, 1, 2, 3], 0, [3], {(0, "a") : 1, (0, "b") : 1, (1, "a") : 2, (1, "b") : 2, 
        (2, "a") : 3, (2, "b") : 3, (3, "a") : 3, (3, "b") : 3})
    dfa2=DFA(["a", "b"], [0, 1, 2, 3], 0, [3], {(0, "a") : 1, (0, "b") : 2, (1, "a") : 0, (1, "b") : 3, 
        (2, "a") : 3, (2, "b") : 0, (3, "a") : 2, (3, "b") : 1})
    assert dfa1.check_if_word_in_language("") == False
    assert dfa1.check_if_word_in_language("aba") == True
    assert dfa1.check_if_word_in_language("ab") == False
    assert dfa1.check_if_word_in_language("abbabbbabaababaaba") == True
    assert dfa2.check_if_word_in_language("") == False
    assert dfa2.check_if_word_in_language("aba") == False
    assert dfa2.check_if_word_in_language("ab") == True
    assert dfa2.check_if_word_in_language("abbabbbabaababaaba") == True

def test_give_state_when_starting_from_given_configuration():
    dfa1=DFA(["a", "b"], [0, 1, 2, 3], 0, [3], {(0, "a") : 1, (0, "b") : 1, (1, "a") : 2, (1, "b") : 2, 
        (2, "a") : 3, (2, "b") : 3, (3, "a") : 3, (3, "b") : 3})
    dfa2=DFA(["a", "b"], [0, 1, 2, 3], 0, [3], {(0, "a") : 1, (0, "b") : 2, (1, "a") : 0, (1, "b") : 3, 
        (2, "a") : 3, (2, "b") : 0, (3, "a") : 2, (3, "b") : 1})
    for i in range(3):
        assert dfa1.give_state_when_starting_from_given_configuration(i, "") == i
        assert dfa1.give_state_when_starting_from_given_configuration(i, "aba") == 3
        assert dfa1.give_state_when_starting_from_given_configuration(i, "ab") == 2 if i == 0 else 3
        assert dfa1.give_state_when_starting_from_given_configuration(i, "abbabbbabaababaaba") == 3
        assert dfa2.give_state_when_starting_from_given_configuration(i, "") == i
        assert dfa2.give_state_when_starting_from_given_configuration(i, "aba") == (i + 2) % 4
        assert dfa2.give_state_when_starting_from_given_configuration(i, "ab") == 3 - i
        assert dfa2.give_state_when_starting_from_given_configuration(i, "abbabbbabaababaaba") == 3 - i   

def test_complement():
    dfa1=DFA(["a", "b"], [0, 1, 2, 3], 0, [3], {(0, "a") : 1, (0, "b") : 1, (1, "a") : 2, (1, "b") : 2, 
        (2, "a") : 3, (2, "b") : 3, (3, "a") : 3, (3, "b") : 3})
    dfa_compl1 = dfa1.take_complement()
    dfa2=DFA(["a", "b"], [0, 1, 2, 3], 0, [3], {(0, "a") : 1, (0, "b") : 2, (1, "a") : 0, (1, "b") : 3, 
        (2, "a") : 3, (2, "b") : 0, (3, "a") : 2, (3, "b") : 1})
    dfa_compl2 = dfa2.take_complement()
    assert dfa_compl1.check_if_word_in_language("") == True
    assert dfa_compl1.check_if_word_in_language("aba") == False
    assert dfa_compl1.check_if_word_in_language("ab") == True
    assert dfa_compl1.check_if_word_in_language("abbabbbabaababaaba") == False
    assert dfa_compl2.check_if_word_in_language("") == True
    assert dfa_compl2.check_if_word_in_language("aba") == True
    assert dfa_compl2.check_if_word_in_language("ab") == False
    assert dfa_compl2.check_if_word_in_language("abbabbbabaababaaba") == False

def test_intersection():
    dfa1=DFA(["a", "b"], [0, 1, 2, 3], 0, [3], {(0, "a") : 1, (0, "b") : 1, (1, "a") : 2, (1, "b") : 2, 
        (2, "a") : 3, (2, "b") : 3, (3, "a") : 3, (3, "b") : 3})
    dfa2=DFA(["a", "b"], [0, 1, 2, 3], 0, [3], {(0, "a") : 1, (0, "b") : 2, (1, "a") : 0, (1, "b") : 3, 
        (2, "a") : 3, (2, "b") : 0, (3, "a") : 2, (3, "b") : 1})
    intersected = dfa1.take_intersection(dfa2)
    assert intersected.check_if_word_in_language("") == False
    assert intersected.check_if_word_in_language("aba") == False
    assert intersected.check_if_word_in_language("ab") == False
    assert intersected.check_if_word_in_language("abbabbbabaababaaba") == True

def test_have_empty_language():
    dfa1 = DFA(["a", "b"], [0, 1, 2, 3], 0, [3], {(0, "a") : 1, (0, "b") : 1, (1, "a") : 2, (1, "b") : 2, 
        (2, "a") : 3, (2, "b") : 3, (3, "a") : 3, (3, "b") : 3})
    dfa2 = DFA(["a", "b"], [0, 1, 2, 3], 0, [3], {(0, "a") : 1, (0, "b") : 2, (1, "a") : 0, (1, "b") : 3, 
        (2, "a") : 3, (2, "b") : 0, (3, "a") : 2, (3, "b") : 1})
    empty = DFA(["a", "b"], [0], 0, [], {(0, "a") : 0, (0, "b") : 0})
    dfa_compl1 = dfa1.take_complement()
    dfa_compl2 = dfa2.take_complement()
    intersected = dfa1.take_intersection(dfa2)
    assert dfa1.have_empty_language() == (False, "aaa")
    assert dfa2.have_empty_language() == (False, "ab")
    assert empty.have_empty_language() == (True, "")
    assert dfa_compl1.have_empty_language() == (False, "")
    assert dfa_compl2.have_empty_language() == (False, "")
    assert intersected.have_empty_language() == (False, "aaab")

def test_is_equal_to():
    dfa1 = DFA(["a", "b"], [0, 1, 2, 3], 0, [3], {(0, "a") : 1, (0, "b") : 1, (1, "a") : 2, (1, "b") : 2, 
        (2, "a") : 3, (2, "b") : 3, (3, "a") : 3, (3, "b") : 3})
    dfa2 = DFA(["a", "b"], [0, 1, 2, 3], 0, [3], {(0, "a") : 1, (0, "b") : 2, (1, "a") : 0, (1, "b") : 3, 
        (2, "a") : 3, (2, "b") : 0, (3, "a") : 2, (3, "b") : 1})
    assert dfa1.is_equal_to(dfa1) == (True, "")
    assert dfa1.is_equal_to(dfa2) == (False, "aaa")
    assert dfa2.is_equal_to(dfa2) == (True, "")
