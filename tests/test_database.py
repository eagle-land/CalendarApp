import app.auth as auth


def test_1():
    assert auth.check_user_exists('1') == True
    assert auth.check_user_exists('1111') == False


def test_2():
    assert auth.check_user_exists_nickname('test') == True
    assert auth.check_user_exists_nickname('tester') == False


def test_3():
    assert auth.check_if_friends('1', '2') == True
    assert auth.check_if_friends('1', '5') == False


def test_4():
    assert auth.search_user_in_database('test') == '1'


def test_5():
    assert auth.get_friends('1') == ['2', '3']


def test_6():
    assert auth.get_pending_friends('1') == ['4']


if __name__ == '__main__':
    test_1()
    test_2()
    test_3()
    test_4()
    test_5()
    test_6()
    print("Passed all database tests.")
