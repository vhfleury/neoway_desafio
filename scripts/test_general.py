import general

def test_created_payload():
    
    test_argument1, test_argument2 = "GO", 1
    
    actual = general.created_payload(test_argument1, test_argument2)
    
    expected1 = dict
    assert type(actual) == expected1

    expected2 = 6
    assert len(actual) == expected2

    expected3 = str
    for value in actual.values():
        
        assert type(value) == expected3


def test_is_init():
    
    test_argument = 2
    expected = False
    
    actual = general.is_init(test_argument)

    assert actual == expected
    
    
    
    