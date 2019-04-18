import app.auth as auth


def test1():
    assert auth.check_user_exists('1') == True

def test2():
    assert auth.check_user_exists_nickname('test') == True

def test3():
    assert auth.check_if_friends('1', '2') == True

def test4():
    print(auth.search_user_in_database('test'))

def test5():
    print(auth.get_friends('1'))

def test6():
    print(auth.get_pending_friends('1'))





if __name__ == '__main__':
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    print("Passed all database tests.")


