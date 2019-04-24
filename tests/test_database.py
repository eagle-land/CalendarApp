import app.database as database

#####   test in order
#1 check_user_exists
#2 check_user_exists_nickname
#3 check_if_friends
#5 get_friends
#6 get_pending_friends


def testing_user_exists():
    assert database.check_user_exists('1') == True
    assert database.check_user_exists('1111') == False


def testing_nickname_exists():
    assert database.check_user_exists_nickname('test') == True
    assert database.check_user_exists_nickname('tester') == False


def testing_if_friendd():
    assert database.check_if_friends('1', '2') == True
    assert database.check_if_friends('1', '5') == False


def testing_email_search():
    assert database.search_user_by_email('test@test.com') == '1'  
    assert database.search_user_by_email('test@test.com') != '0'  



def testing_get_friends():
    assert database.get_friends('1') == ['2', '3']
    assert database.get_friends('1') != ['2', '8']


def testing_get_friends_pending():
    assert database.get_pending_friends('1') == ['4']
    assert database.get_pending_friends('1') != ['3']


if __name__ == '__main__':
    testing_user_exists()
    testing_nickname_exists()
    testing_if_friendd()
    testing_email_search()
    testing_get_friends()
    testing_get_friends_pending()
    print("Passed all database tests.")
