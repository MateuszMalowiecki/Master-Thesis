import pytest
from VPA import DVPA

#TODO: check find_word_in_language if it returns always string.
def test_check_if_word_in_language():
    dvpa1=DVPA(["a"], ["b"], ["c"], [0, 1], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 1, (0, "b", "Z"): 1, 
            (0, "c"): 1, (1, "a"): (0, "A"), (1, "b", "A"): 0, (1, "b", "Z"): 0, (1, "c"): 0})
    dvpa2=DVPA(["a"], ["b"], ["c"], [0, 1, 2, 3], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 2, (0, "b", "Z"): 2, (0, "c"): 0, 
            (1, "a"): (0, "A"), (1, "b", "A"): 3, (1, "b", "Z"): 3, (1, "c"): 1,
            (2, "a"): (3, "A"), (2, "b", "A"): 0, (2, "b", "Z"): 0, (2, "c"): 2, 
            (3, "a"): (2, "A"), (3, "b", "A"): 1, (3, "b", "Z"): 1, (3, "c"): 3})
    assert dvpa1.check_if_word_in_language("") == True
    assert dvpa1.check_if_word_in_language("abc") == False
    assert dvpa1.check_if_word_in_language("ab") == True
    assert dvpa1.check_if_word_in_language("abccbacaccbabaa") == False
    assert dvpa2.check_if_word_in_language("") == True
    assert dvpa2.check_if_word_in_language("aba") == False
    assert dvpa2.check_if_word_in_language("ab") == False
    assert dvpa2.check_if_word_in_language("abccbacaccbabaa") == True

def test_give_state_when_starting_from_given_configuration():
    dvpa1=DVPA(["a"], ["b"], ["c"], [0, 1], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 1, (0, "b", "Z"): 1, 
            (0, "c"): 1, (1, "a"): (0, "A"), (1, "b", "A"): 0, (1, "b", "Z"): 0, (1, "c"): 0})
    dvpa2=DVPA(["a"], ["b"], ["c"], [0, 1, 2, 3], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 2, (0, "b", "Z"): 2, (0, "c"): 0, 
            (1, "a"): (0, "A"), (1, "b", "A"): 3, (1, "b", "Z"): 3, (1, "c"): 1,
            (2, "a"): (3, "A"), (2, "b", "A"): 0, (2, "b", "Z"): 0, (2, "c"): 2, 
            (3, "a"): (2, "A"), (3, "b", "A"): 1, (3, "b", "Z"): 1, (3, "c"): 3})
    for stack in [["Z"], ["A", "Z"], ["A", "A", "Z"]]:
        assert dvpa1.give_state_and_stack_when_starting_from_given_configuration(0, "", stack) == (0, stack)
        assert dvpa1.give_state_and_stack_when_starting_from_given_configuration(1, "abc", stack) == (0, stack)
        assert dvpa1.give_state_and_stack_when_starting_from_given_configuration(1, "ab", stack) == (1, stack)
        if len(stack) == 1:
            assert dvpa1.give_state_and_stack_when_starting_from_given_configuration(0, "abccbacaccbabaa", stack) == (1, ["A", "A", "A", "Z"]) 
        else:
            assert dvpa1.give_state_and_stack_when_starting_from_given_configuration(0, "abccbacaccbabaa", stack) == (1, ["A", "A"] + stack)
        for i in range(3):
            assert dvpa2.give_state_and_stack_when_starting_from_given_configuration(i, "", stack) == (i, stack)
            assert dvpa2.give_state_and_stack_when_starting_from_given_configuration(i, "abc", stack) == (3 - i, stack)
            assert dvpa2.give_state_and_stack_when_starting_from_given_configuration(i, "ab", stack) == (3 - i, stack)
            if len(stack) == 1:
                assert dvpa2.give_state_and_stack_when_starting_from_given_configuration(i, "abccbacaccbabaa", stack) == (i, ["A", "A", "A", "Z"]) 
            else:
                assert dvpa2.give_state_and_stack_when_starting_from_given_configuration(i, "abccbacaccbabaa", stack) == (i, ["A", "A"] + stack)

def test_complement():
    dvpa1=DVPA(["a"], ["b"], ["c"], [0, 1], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 1, (0, "b", "Z"): 1, 
            (0, "c"): 1, (1, "a"): (0, "A"), (1, "b", "A"): 0, (1, "b", "Z"): 0, (1, "c"): 0})
    dvpa_compl1 = dvpa1.take_complement()
    dvpa2=DVPA(["a"], ["b"], ["c"], [0, 1, 2, 3], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 2, (0, "b", "Z"): 2, (0, "c"): 0, 
            (1, "a"): (0, "A"), (1, "b", "A"): 3, (1, "b", "Z"): 3, (1, "c"): 1,
            (2, "a"): (3, "A"), (2, "b", "A"): 0, (2, "b", "Z"): 0, (2, "c"): 2, 
            (3, "a"): (2, "A"), (3, "b", "A"): 1, (3, "b", "Z"): 1, (3, "c"): 3})
    dvpa_compl2 = dvpa2.take_complement()
    assert dvpa_compl1.check_if_word_in_language("") == False
    assert dvpa_compl1.check_if_word_in_language("abc") == True
    assert dvpa_compl1.check_if_word_in_language("ab") == False
    assert dvpa_compl1.check_if_word_in_language("abccbacaccbabaa") == True
    assert dvpa_compl2.check_if_word_in_language("") == False
    assert dvpa_compl2.check_if_word_in_language("abc") == True
    assert dvpa_compl2.check_if_word_in_language("ab") == True
    assert dvpa_compl2.check_if_word_in_language("abccbacaccbabaa") == False

def test_intersection():
    dvpa1=DVPA(["a"], ["b"], ["c"], [0, 1], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 1, (0, "b", "Z"): 1, 
            (0, "c"): 1, (1, "a"): (0, "A"), (1, "b", "A"): 0, (1, "b", "Z"): 0, (1, "c"): 0})
    dvpa2=DVPA(["a"], ["b"], ["c"], [0, 1, 2, 3], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 2, (0, "b", "Z"): 2, (0, "c"): 0, 
            (1, "a"): (0, "A"), (1, "b", "A"): 3, (1, "b", "Z"): 3, (1, "c"): 1,
            (2, "a"): (3, "A"), (2, "b", "A"): 0, (2, "b", "Z"): 0, (2, "c"): 2, 
            (3, "a"): (2, "A"), (3, "b", "A"): 1, (3, "b", "Z"): 1, (3, "c"): 3})
    intersected = dvpa1.take_intersection(dvpa2)
    assert intersected.check_if_word_in_language("") == True
    assert intersected.check_if_word_in_language("abc") == False
    assert intersected.check_if_word_in_language("ab") == False
    assert intersected.check_if_word_in_language("abccbacaccbabaa") == False

def test_have_empty_language():
    dvpa1=DVPA(["a"], ["b"], ["c"], [0, 1], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 1, (0, "b", "Z"): 1, 
            (0, "c"): 1, (1, "a"): (0, "A"), (1, "b", "A"): 0, (1, "b", "Z"): 0, (1, "c"): 0})
    dvpa2=DVPA(["a"], ["b"], ["c"], [0, 1, 2, 3], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 2, (0, "b", "Z"): 2, (0, "c"): 0, 
            (1, "a"): (0, "A"), (1, "b", "A"): 3, (1, "b", "Z"): 3, (1, "c"): 1,
            (2, "a"): (3, "A"), (2, "b", "A"): 0, (2, "b", "Z"): 0, (2, "c"): 2, 
            (3, "a"): (2, "A"), (3, "b", "A"): 1, (3, "b", "Z"): 1, (3, "c"): 3})
    empty = DVPA(["a"], ["b"], ["c"], [0], ["A", "Z"], 0, [], "Z", {(0, "a"): (0, "A"), (0, "b", "A"): 0, (0, "b", "Z"): 0, (0, "c"): 0})
    dvpa_compl1 = dvpa1.take_complement()
    dvpa_compl2 = dvpa2.take_complement()
    intersected = dvpa1.take_intersection(dvpa2)
    assert dvpa1.have_empty_language() == (False, "")
    assert dvpa2.have_empty_language() == (False, "")
    assert empty.have_empty_language() == (True, "")
    assert dvpa_compl1.have_empty_language() == (False, "c")
    assert dvpa_compl2.have_empty_language() == (False, "a")
    assert intersected.have_empty_language() == (False, "")

def test_is_equal_to():
    dvpa1=DVPA(["a"], ["b"], ["c"], [0, 1], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 1, (0, "b", "Z"): 1, 
            (0, "c"): 1, (1, "a"): (0, "A"), (1, "b", "A"): 0, (1, "b", "Z"): 0, (1, "c"): 0})
    dvpa2=DVPA(["a"], ["b"], ["c"], [0, 1, 2, 3], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 2, (0, "b", "Z"): 2, (0, "c"): 0, 
            (1, "a"): (0, "A"), (1, "b", "A"): 3, (1, "b", "Z"): 3, (1, "c"): 1,
            (2, "a"): (3, "A"), (2, "b", "A"): 0, (2, "b", "Z"): 0, (2, "c"): 2, 
            (3, "a"): (2, "A"), (3, "b", "A"): 1, (3, "b", "Z"): 1, (3, "c"): 3})
    assert dvpa1.is_equal_to(dvpa1) == (True, "")
    assert dvpa1.is_equal_to(dvpa2) == (False, "ca")
    assert dvpa2.is_equal_to(dvpa2) == (True, "")
