import app.calendar as calendar

def test1():
    #Example calendar 1
    user1events = [
        calendar.Event("2019-04-15T11:00:00-04:00", "2019-04-15T11:50:00-04:00")
    ]
    calendar1 = calendar.Calendar(user1events)
    start = "2019-04-15T00:00:00-04:00"
    end = "2019-04-21T00:00:00-04:00"
    timezone = "America/New York"
    userid1 = 123

    result = calendar.get_calendar(userid1, start, end, timezone)
    #result_string = ""
    #for event in result:
       # result_string += event.starttime + ' - ' + event.endtime + '\n'
    #print(result_string)
    assert result == calendar1


    #Example calendar 2
    user2events = [
        calendar.Event("2019-04-15T20:00:00-04:00", "2019-04-15T20:50:00-04:00")
    ]
    calendar2 = calendar.Calendar(user2events)
    start = "2019-04-15T20:00:00-04:00"
    end = "2019-04-15T20:50:00-04:00"
    timezone = "England/London"
    userid2 = 456
    result = calendar.get_calendar(userid2, start, end, timezone)
    #result_string = ""
   # for event in result:
     #   result_string += event.starttime + ' - ' + event.endtime + '\n'
   # print(result_string)
    assert result == calendar2


def test2():
    #Example calendar 1
    user3events = [
        calendar.Event("2019-04-15T22:00:00-04:00", "2019-04-15T22:50:00-04:00")
    ]
    calendar3 = calendar.Calendar(user3events)
    start = "2019-04-15T22:00:00-04:00"
    end = "2019-04-21T22:00:00-04:00"
    timezone = "America/California"
    userid3 = 789
    result = calendar.get_calendar(userid3, start, end, timezone)
    #result_string = ""
    #for event in result:
       # result_string += event.starttime + ' - ' + event.endtime + '\n'
    #print(result_string)
    assert result == calendar3


if __name__ == '__main__':
    test1()
    print("Passed all tests.")

