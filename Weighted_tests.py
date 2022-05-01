import pytest
from Weighted import DWFA

def test_weight_of_word_from_given_state():
    dwfa1 = DWFA(["a", "b"], [0, 1, 2, 3], {0 : 4, 1 : 6, 2 : 1, 3: 2}, {0 : 11, 1 : 5, 2 : 3, 3 : 7},
        {(0, "a") : (2, 1), (0, "b") : (3, 1), (1, "a") : (7, 2), (1, "b") : (9, 2), 
            (2, "a") : (6, 3), (2, "b") : (11, 3), (3, "a") : (8, 0), (3, "b") : (5, 0)})
    dwfa2 = DWFA(["a", "b"], [0, 1, 2, 3], {0 : 3, 1 : 5, 2 : 7, 3: 11}, {0 : 2, 1 : 6, 2 : 4, 3 : 1},
        {(0, "a") : (7, 1), (0, "b") : (5, 2), (1, "a") : (8, 0), (1, "b") : (6, 3), 
            (2, "a") : (3, 3), (2, "b") : (2, 0), (3, "a") : (11, 2), (3, "b") : (9, 1)})

    paths_weights_dwfa1={("", 0): 44, ("", 1): 30, ("", 2): 3, ("", 3): 14, 
        ("aba", 0): 3024, ("aba", 1): 40656, ("aba", 2): 300, ("aba", 3): 1008,
        ("ab", 0): 216, ("ab", 1): 3234, ("ab", 2): 330, ("ab", 3): 240}
    paths_weights_dwfa2={("", 0): 6, ("", 1): 30, ("", 2): 28, ("", 3): 11, 
        ("aba", 0): 5544, ("aba", 1): 600, ("aba", 2): 3024, ("aba", 3): 10164,
        ("ab", 0): 126, ("ab", 1): 800, ("ab", 2): 1134, ("ab", 3): 484}

    for i in range(4):
        for w in ["", "ab", "aba"]:
            assert dwfa1.weight_of_word_from_given_state(i, w) == paths_weights_dwfa1[(w, i)]
            assert dwfa2.weight_of_word_from_given_state(i, w) == paths_weights_dwfa2[(w, i)]

def test_weight_of_word():
    dwfa1 = DWFA(["a", "b"], [0, 1, 2, 3], {0 : 4, 1 : 6, 2 : 1, 3: 2}, {0 : 11, 1 : 5, 2 : 3, 3 : 7},
        {(0, "a") : (2, 1), (0, "b") : (3, 1), (1, "a") : (7, 2), (1, "b") : (9, 2), 
            (2, "a") : (6, 3), (2, "b") : (11, 3), (3, "a") : (8, 0), (3, "b") : (5, 0)})
    dwfa2 = DWFA(["a", "b"], [0, 1, 2, 3], {0 : 3, 1 : 5, 2 : 7, 3: 11}, {0 : 2, 1 : 6, 2 : 4, 3 : 1},
        {(0, "a") : (7, 1), (0, "b") : (5, 2), (1, "a") : (8, 0), (1, "b") : (6, 3), 
            (2, "a") : (3, 3), (2, "b") : (2, 0), (3, "a") : (11, 2), (3, "b") : (9, 1)})
    assert dwfa1.weight_of_word("") == 91
    assert dwfa1.weight_of_word("aba") == 44988
    assert dwfa1.weight_of_word("ab") == 4020
    assert dwfa2.weight_of_word("") == 75
    assert dwfa2.weight_of_word("aba") == 19332
    assert dwfa2.weight_of_word("ab") == 2544


def test_give_state_when_starting_from_given_configuration():
    dwfa1 = DWFA(["a", "b"], [0, 1, 2, 3], {0 : 4, 1 : 6, 2 : 1, 3: 2}, {0 : 11, 1 : 5, 2 : 3, 3 : 7},
        {(0, "a") : (2, 1), (0, "b") : (3, 1), (1, "a") : (7, 2), (1, "b") : (9, 2), 
            (2, "a") : (6, 3), (2, "b") : (11, 3), (3, "a") : (8, 0), (3, "b") : (5, 0)})
    dwfa2 = DWFA(["a", "b"], [0, 1, 2, 3], {0 : 3, 1 : 5, 2 : 7, 3: 11}, {0 : 2, 1 : 6, 2 : 4, 3 : 1},
        {(0, "a") : (7, 1), (0, "b") : (5, 2), (1, "a") : (8, 0), (1, "b") : (6, 3), 
            (2, "a") : (3, 3), (2, "b") : (2, 0), (3, "a") : (11, 2), (3, "b") : (9, 1)})
    configurations_dwfa1={("", 0): (0, 44), ("", 1): (1, 30), ("", 2): (2, 3), ("", 3): (3, 14), 
        ("aba", 0): (3, 3024), ("aba", 1): (0, 40656), ("aba", 2): (1, 300), ("aba", 3): (2, 1008),
        ("ab", 0): (2, 216), ("ab", 1): (3, 3234), ("ab", 2): (0, 330), ("ab", 3): (1, 240)}
    configurations_dwfa2={("", 0): (0, 6), ("", 1): (1, 30), ("", 2): (2, 28), ("", 3): (3, 11), 
        ("aba", 0): (2, 5544), ("aba", 1): (3, 600), ("aba", 2): (0, 3024), ("aba", 3): (1, 10164),
        ("ab", 0): (3, 126), ("ab", 1): (2, 800), ("ab", 2): (1, 1134), ("ab", 3): (0, 484)}
    for i in range(4):
         for w in ["", "ab", "aba"]:
            assert dwfa1.give_state_and_weight_when_starting_from_given_configuration(i, w) == configurations_dwfa1[(w, i)]
            assert dwfa2.give_state_and_weight_when_starting_from_given_configuration(i, w) == configurations_dwfa2[(w, i)]

def test_is_equal_to():
    dwfa1 = DWFA(["a", "b"], [0, 1, 2, 3], {0 : 4, 1 : 6, 2 : 1, 3: 2}, {0 : 11, 1 : 5, 2 : 3, 3 : 7},
        {(0, "a") : (2, 1), (0, "b") : (3, 1), (1, "a") : (7, 2), (1, "b") : (9, 2), 
            (2, "a") : (6, 3), (2, "b") : (11, 3), (3, "a") : (8, 0), (3, "b") : (5, 0)})
    dwfa2 = DWFA(["a", "b"], [0, 1, 2, 3], {0 : 3, 1 : 5, 2 : 7, 3: 11}, {0 : 2, 1 : 6, 2 : 4, 3 : 1},
        {(0, "a") : (7, 1), (0, "b") : (5, 2), (1, "a") : (8, 0), (1, "b") : (6, 3), 
            (2, "a") : (3, 3), (2, "b") : (2, 0), (3, "a") : (11, 2), (3, "b") : (9, 1)})
    assert dwfa1.is_equal_to(dwfa1)[0] == True
    assert dwfa1.is_equal_to(dwfa2)[0] == False
    assert dwfa2.is_equal_to(dwfa2)[0] == True
