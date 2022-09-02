from lib2to3.pgen2 import grammar
from VPA import DVPA, ContextFreeGrammar

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


def test_get_all_reachable_states():
    dvpa1=DVPA(["a"], ["b"], ["c"], [0, 1], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 1, (0, "b", "Z"): 1, 
            (0, "c"): 1, (1, "a"): (0, "A"), (1, "b", "A"): 0, (1, "b", "Z"): 0, (1, "c"): 0})
    dvpa2=DVPA(["a"], ["b"], ["c"], [0, 1, 2, 3], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (1, "A"), (0, "b", "A"): 2, (0, "b", "Z"): 2, (0, "c"): 0, 
            (1, "a"): (0, "A"), (1, "b", "A"): 3, (1, "b", "Z"): 3, (1, "c"): 1,
            (2, "a"): (3, "A"), (2, "b", "A"): 0, (2, "b", "Z"): 0, (2, "c"): 2, 
            (3, "a"): (2, "A"), (3, "b", "A"): 1, (3, "b", "Z"): 1, (3, "c"): 3})
    intersected = dvpa1.take_intersection(dvpa2)
    intersected_with_itself = dvpa2.take_intersection(dvpa2)
    assert dvpa1.get_all_reachable_states() == [0, 1]
    assert dvpa2.get_all_reachable_states() == [0, 1, 2, 3]
    assert intersected.get_all_reachable_states() == [(0, 0), (1, 0), (1, 1), (1, 2), (0, 1), (0, 2), (0, 3), (1, 3)]
    assert intersected_with_itself.get_all_reachable_states() == [(0, 0), (1, 1), (2, 2), (3, 3)]

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

def test_to_CFG():
    dvpa1=DVPA(["a"], ["b"], ["c"], [0], ["A", "Z"], 0, [0], "Z", 
        {(0, "a"): (0, "A"), (0, "b", "A"): 0, (0, "b", "Z"): 0, (0, "c"): 0})
    grammar1=dvpa1.to_CFG()
    assert grammar1.nonterminals == ["S", (0, 0)]
    assert grammar1.terminals == ["a", "b", "c"]
    assert grammar1.productions == [((0, 0), []), ((0, 0), [(0, 0), (0, 0)]), ((0, 0), ["a", (0, 0), "b"]), ((0, 0), ["c", (0, 0)]), ("S", [(0, 0)])]
    assert grammar1.start_symbol == "S"

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
    empty2= dvpa1.take_intersection(dvpa_compl1)
    empty3= dvpa2.take_intersection(dvpa_compl2)
    intersected = dvpa1.take_intersection(dvpa2)
    assert dvpa1.have_empty_language() == (False, "")
    assert dvpa2.have_empty_language() == (False, "")
    assert empty.have_empty_language() == (True, "")
    assert dvpa_compl1.have_empty_language() == (False, "acb")
    assert dvpa_compl2.have_empty_language() == (False, "ab")
    assert empty2.have_empty_language() == (True, "")
    assert empty3.have_empty_language() == (True, "")
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
    assert dvpa1.is_equal_to(dvpa2) == (False, "cabc")
    assert dvpa2.is_equal_to(dvpa2) == (True, "")

def test_grammar_is_empty():
    grammar1=ContextFreeGrammar(["S"], ["a", "b"], [("S", ["a", "S", "b"]), ("S", [])], "S")
    grammar2=ContextFreeGrammar(["S", "A", "B"], ["a", "b"], 
        [("S", ["a", "A"]), ("S", ["B", "b"]), ("A", ["a", "A"]), ("A", ["a", "A", "b"]), ("A", []), ("B", ["B", "b"]), ("B", ["a", "B", "b"]), ("B", [])], "S")
    grammar3=ContextFreeGrammar(["S"], ["a", "b"], [("S", ["a", "S", "b"])], "S")
    assert grammar1.is_empty() == (False, "")
    assert grammar2.is_empty() == (False, "a")
    assert grammar3.is_empty() == (True, "")
