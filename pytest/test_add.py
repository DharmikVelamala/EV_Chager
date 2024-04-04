import add
 
def test_add():
    assert add.add(7,3) == 10
    assert add.add(7) == 9
    assert add.add(5) == 7

def test_product():
    assert add.product(5,5) == 25
    #assert add.product(5) == 57
    #assert add.product(7) == 14
