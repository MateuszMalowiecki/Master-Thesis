from Weighted import DWFA

def test_weight_of_word_from_given_state():
    dwfa1 = DWFA(["a", "b"], [0, 1, 2, 3], {0 : 4, 1 : 6, 2 : 1, 3: 2}, {0 : 11, 1 : 5, 2 : 3, 3 : 7},
        {(0, "a") : (2, 1), (0, "b") : (3, 1), (1, "a") : (7, 2), (1, "b") : (9, 2), 
            (2, "a") : (6, 3), (2, "b") : (11, 3), (3, "a") : (8, 0), (3, "b") : (5, 0)})
    dwfa2 = DWFA(["a", "b"], [0, 1, 2, 3], {0 : 3, 1 : 5, 2 : 7, 3: 11}, {0 : 2, 1 : 6, 2 : 4, 3 : 1},
        {(0, "a") : (7, 1), (0, "b") : (5, 2), (1, "a") : (8, 0), (1, "b") : (6, 3), 
            (2, "a") : (3, 3), (2, "b") : (2, 0), (3, "a") : (11, 2), (3, "b") : (9, 1)})

    paths_weights_dwfa1={("", 0): 15, ("", 1): 11, ("", 2): 4, ("", 3): 9, 
        ("aba", 0): 28, ("aba", 1): 43, ("aba", 2): 19, ("aba", 3): 23,
        ("ab", 0): 18, ("ab", 1): 31, ("ab", 2): 23, ("ab", 3): 18}
    paths_weights_dwfa2={("", 0): 5, ("", 1): 11, ("", 2): 11, ("", 3): 12, 
        ("aba", 0): 31, ("aba", 1): 22, ("aba", 2): 29, ("aba", 3): 37,
        ("ab", 0): 17, ("ab", 1): 22, ("ab", 2): 25, ("ab", 3): 26}

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
    assert dwfa1.weight_of_word("") == 39
    assert dwfa1.weight_of_word("aba") == 113
    assert dwfa1.weight_of_word("ab") == 90
    assert dwfa2.weight_of_word("") == 39
    assert dwfa2.weight_of_word("aba") == 119
    assert dwfa2.weight_of_word("ab") == 90

def test_give_state_when_starting_from_given_configuration():
    dwfa1 = DWFA(["a", "b"], [0, 1, 2, 3], {0 : 4, 1 : 6, 2 : 1, 3: 2}, {0 : 11, 1 : 5, 2 : 3, 3 : 7},
        {(0, "a") : (2, 1), (0, "b") : (3, 1), (1, "a") : (7, 2), (1, "b") : (9, 2), 
            (2, "a") : (6, 3), (2, "b") : (11, 3), (3, "a") : (8, 0), (3, "b") : (5, 0)})
    dwfa2 = DWFA(["a", "b"], [0, 1, 2, 3], {0 : 3, 1 : 5, 2 : 7, 3: 11}, {0 : 2, 1 : 6, 2 : 4, 3 : 1},
        {(0, "a") : (7, 1), (0, "b") : (5, 2), (1, "a") : (8, 0), (1, "b") : (6, 3), 
            (2, "a") : (3, 3), (2, "b") : (2, 0), (3, "a") : (11, 2), (3, "b") : (9, 1)})
    configurations_dwfa1={("", 0): (0, 15), ("", 1): (1, 11), ("", 2): (2, 4), ("", 3): (3, 9), 
        ("aba", 0): (3, 28), ("aba", 1): (0, 43), ("aba", 2): (1, 19), ("aba", 3): (2, 23),
        ("ab", 0): (2, 18), ("ab", 1): (3, 31), ("ab", 2): (0, 23), ("ab", 3): (1, 18)}
    configurations_dwfa2={("", 0): (0, 5), ("", 1): (1, 11), ("", 2): (2, 11), ("", 3): (3, 12), 
        ("aba", 0): (2, 31), ("aba", 1): (3, 22), ("aba", 2): (0, 29), ("aba", 3): (1, 37),
        ("ab", 0): (3, 17), ("ab", 1): (2, 22), ("ab", 2): (1, 25), ("ab", 3): (0, 26)}
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
