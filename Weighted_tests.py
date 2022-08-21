from Weighted import DWFA

def test_weight_of_word_from_given_state():
    dwfa1 = DWFA(["a", "b"], [0, 1, 2, 3], 0, {0 : 11, 1 : 5, 2 : 3, 3 : 7},
        {(0, "a") : (2, 1), (0, "b") : (3, 1), (1, "a") : (7, 2), (1, "b") : (9, 2), 
            (2, "a") : (6, 3), (2, "b") : (11, 3), (3, "a") : (8, 0), (3, "b") : (5, 0)})
    dwfa2 = DWFA(["a", "b"], [0, 1, 2, 3], 0, {0 : 2, 1 : 6, 2 : 4, 3 : 1},
        {(0, "a") : (7, 1), (0, "b") : (5, 2), (1, "a") : (8, 0), (1, "b") : (6, 3), 
            (2, "a") : (3, 3), (2, "b") : (2, 0), (3, "a") : (11, 2), (3, "b") : (9, 1)})

    paths_weights_dwfa1={("", 0): 11, ("", 1): 5, ("", 2): 3, ("", 3): 7, 
        ("aba", 0): 24, ("aba", 1): 37, ("aba", 2): 18, ("aba", 3): 21,
        ("ab", 0): 14, ("ab", 1): 25, ("ab", 2): 22, ("ab", 3): 16}
    paths_weights_dwfa2={("", 0): 2, ("", 1): 6, ("", 2): 4, ("", 3): 1, 
        ("aba", 0): 28, ("aba", 1): 17, ("aba", 2): 22, ("aba", 3): 26,
        ("ab", 0): 14, ("ab", 1): 17, ("ab", 2): 18, ("ab", 3): 15}

    for i in range(4):
        for w in ["", "ab", "aba"]:
            assert dwfa1.weight_of_word_from_given_state(i, w) == paths_weights_dwfa1[(w, i)]
            assert dwfa2.weight_of_word_from_given_state(i, w) == paths_weights_dwfa2[(w, i)]

def test_weight_of_word():
    dwfa1 = DWFA(["a", "b"], [0, 1, 2, 3], 0, {0 : 11, 1 : 5, 2 : 3, 3 : 7},
        {(0, "a") : (2, 1), (0, "b") : (3, 1), (1, "a") : (7, 2), (1, "b") : (9, 2), 
            (2, "a") : (6, 3), (2, "b") : (11, 3), (3, "a") : (8, 0), (3, "b") : (5, 0)})
    dwfa2 = DWFA(["a", "b"], [0, 1, 2, 3], 0, {0 : 2, 1 : 6, 2 : 4, 3 : 1},
        {(0, "a") : (7, 1), (0, "b") : (5, 2), (1, "a") : (8, 0), (1, "b") : (6, 3), 
            (2, "a") : (3, 3), (2, "b") : (2, 0), (3, "a") : (11, 2), (3, "b") : (9, 1)})
    assert dwfa1.weight_of_word("") == 11
    assert dwfa1.weight_of_word("aba") == 24
    assert dwfa1.weight_of_word("ab") == 14
    assert dwfa2.weight_of_word("") == 2
    assert dwfa2.weight_of_word("aba") == 28
    assert dwfa2.weight_of_word("ab") == 14


def test_give_state_when_starting_from_given_configuration():
    dwfa1 = DWFA(["a", "b"], [0, 1, 2, 3], 0, {0 : 11, 1 : 5, 2 : 3, 3 : 7},
        {(0, "a") : (2, 1), (0, "b") : (3, 1), (1, "a") : (7, 2), (1, "b") : (9, 2), 
            (2, "a") : (6, 3), (2, "b") : (11, 3), (3, "a") : (8, 0), (3, "b") : (5, 0)})
    dwfa2 = DWFA(["a", "b"], [0, 1, 2, 3], 0, {0 : 2, 1 : 6, 2 : 4, 3 : 1},
        {(0, "a") : (7, 1), (0, "b") : (5, 2), (1, "a") : (8, 0), (1, "b") : (6, 3), 
            (2, "a") : (3, 3), (2, "b") : (2, 0), (3, "a") : (11, 2), (3, "b") : (9, 1)})
    configurations_dwfa1={("", 0): (0, 11), ("", 1): (1, 5), ("", 2): (2, 3), ("", 3): (3, 7), 
        ("aba", 0): (3, 24), ("aba", 1): (0, 37), ("aba", 2): (1, 18), ("aba", 3): (2, 21),
        ("ab", 0): (2, 14), ("ab", 1): (3, 25), ("ab", 2): (0, 22), ("ab", 3): (1, 16)}
    configurations_dwfa2={("", 0): (0, 2), ("", 1): (1, 6), ("", 2): (2, 4), ("", 3): (3, 1), 
        ("aba", 0): (2, 28), ("aba", 1): (3, 17), ("aba", 2): (0, 22), ("aba", 3): (1, 26),
        ("ab", 0): (3, 14), ("ab", 1): (2, 17), ("ab", 2): (1, 18), ("ab", 3): (0, 15)}
    for i in range(4):
         for w in ["", "ab", "aba"]:
            assert dwfa1.give_state_and_weight_when_starting_from_given_configuration(i, w) == configurations_dwfa1[(w, i)]
            assert dwfa2.give_state_and_weight_when_starting_from_given_configuration(i, w) == configurations_dwfa2[(w, i)]

def test_is_equal_to():
    dwfa1 = DWFA(["a", "b"], [0, 1, 2, 3], 0, {0 : 11, 1 : 5, 2 : 3, 3 : 7},
        {(0, "a") : (2, 1), (0, "b") : (3, 1), (1, "a") : (7, 2), (1, "b") : (9, 2), 
            (2, "a") : (6, 3), (2, "b") : (11, 3), (3, "a") : (8, 0), (3, "b") : (5, 0)})
    dwfa2 = DWFA(["a", "b"], [0, 1, 2, 3], 0, {0 : 2, 1 : 6, 2 : 4, 3 : 1},
        {(0, "a") : (7, 1), (0, "b") : (5, 2), (1, "a") : (8, 0), (1, "b") : (6, 3), 
            (2, "a") : (3, 3), (2, "b") : (2, 0), (3, "a") : (11, 2), (3, "b") : (9, 1)})
    assert dwfa1.is_equal_to(dwfa1) == (True, "")
    assert dwfa1.is_equal_to(dwfa2) == (False, "a")
    assert dwfa2.is_equal_to(dwfa2) == (True, "")

def test_take_difference_automaton():
    dwfa1 = DWFA(["a", "b"], [0, 1, 2, 3], 0, {0 : 11, 1 : 5, 2 : 3, 3 : 7},
        {(0, "a") : (2, 1), (0, "b") : (3, 1), (1, "a") : (7, 2), (1, "b") : (9, 2), 
            (2, "a") : (6, 3), (2, "b") : (11, 3), (3, "a") : (8, 0), (3, "b") : (5, 0)})
    dwfa2 = DWFA(["a", "b"], [0, 1, 2, 3], 0, {0 : 2, 1 : 6, 2 : 4, 3 : 1},
        {(0, "a") : (7, 1), (0, "b") : (5, 2), (1, "a") : (8, 0), (1, "b") : (6, 3), 
            (2, "a") : (3, 3), (2, "b") : (2, 0), (3, "a") : (11, 2), (3, "b") : (9, 1)})
    dwfa_difference = dwfa1.take_difference_automaton(dwfa2)
    assert dwfa_difference.weight_of_word("") == 9
    assert dwfa_difference.weight_of_word("aba") == 999999999996
    assert dwfa_difference.weight_of_word("ab") == 0
    
def test_has_word_with_weight_lower_than():
    dwfa1 = DWFA(["a", "b"], [0, 1, 2, 3], 0, {0 : 11, 1 : 5, 2 : 3, 3 : 7},
        {(0, "a") : (2, 1), (0, "b") : (3, 1), (1, "a") : (7, 2), (1, "b") : (9, 2), 
            (2, "a") : (6, 3), (2, "b") : (11, 3), (3, "a") : (8, 0), (3, "b") : (5, 0)})
    dwfa2 = DWFA(["a", "b"], [0, 1, 2, 3], 0, {0 : 2, 1 : 6, 2 : 4, 3 : 1},
        {(0, "a") : (7, 1), (0, "b") : (5, 2), (1, "a") : (8, 0), (1, "b") : (6, 3), 
            (2, "a") : (3, 3), (2, "b") : (2, 0), (3, "a") : (11, 2), (3, "b") : (9, 1)})
    dwfa3 = DWFA(["a", "b"], [0, 1], 0, {0 : -2, 1 : 6}, 
        {(0, "a") : (5, 1), (0, "b") : (-5, 0), (1, "a") : (-10, 0), (1, "b") : (7, 1)})
    assert dwfa1.has_word_with_weight_lower_than(0) == (False, "")
    assert dwfa1.has_word_with_weight_lower_than(5) == (False, "")
    assert dwfa1.has_word_with_weight_lower_than(15) == (True, "")
    assert dwfa2.has_word_with_weight_lower_than(0) == (False, "")
    assert dwfa2.has_word_with_weight_lower_than(5) == (True, "")
    assert dwfa2.has_word_with_weight_lower_than(15) == (True, "")
    assert dwfa3.has_word_with_weight_lower_than(0) == (True, "b")
