import app.calendar as calendar


def test1():
    # Example calendar 1
    user1events = [
        calendar.Event("2019-04-15T11:00:00-04:00", "2019-04-15T11:50:00-04:00")
    ]
    calendar1 = calendar.Calendar(user1events)

    # Example calendar 2
    user2events = [
        calendar.Event("2019-04-15T12:00:00-04:00", "2019-04-15T12:50:00-04:00")
    ]
    calendar2 = calendar.Calendar(user2events)

    # Correct return value
    freeevents = [
        calendar.Event("2019-04-15T11:50:00-04:00", "2019-04-15T12:00:00-04:00")
    ]
    freecalendar = calendar.Calendar(freeevents)

    rangestart = "2019-04-15T11:00:00-04:00"
    rangeend = "2019-04-15T12:50:00-04:00"
    result = calendar.get_shared_freetimes(rangestart, rangeend, calendar1, calendar2)
    result_string =""
    for event in result:
        result_string += event.starttime + ' - ' + event.endtime + '\n'
    print(result_string)
    assert result == freecalendar

def test2(): #testing to see if it can find events that are in range even when the beginning/end event are out of range
    # Example calendar 1
    user1events = [
        calendar.Event("2019-04-15T10:00:00-04:00", "2019-04-15T13:20:00-08:00")
    ]
    calendar1 = calendar.Calendar(user1events)

    # Example calendar 2
    user2events = [
        calendar.Event("2019-04-15T14:00:00-04:00", "2019-04-15T16:00:00-04:00")
    ]
    calendar2 = calendar.Calendar(user2events)

    # Correct return value
    freeevents = [
        calendar.Event("2019-04-15T11:50:00-04:00", "2019-04-15T14:30:00-08:00")
    ]
    freecalendar = calendar.Calendar(freeevents)

    rangestart = "2019-04-15T11:00:00-04:00"
    rangeend = "2019-04-15T15:60:00-02:00"
    result = calendar.get_shared_freetimes(rangestart, rangeend, calendar1, calendar2)
    result_string =""
    for event in result:
        result_string += event.starttime + ' - ' + event.endtime + '\n'
    print(result_string)
    assert result == freecalendar


def test3(): #seeing the error that occurs when an event is out of range 
    # Example calendar 1
    user1events = [
        calendar.Event("2019-04-15T9:00:00-04:00", "2019-04-15T11:50:00-04:00")
    ]
    calendar1 = calendar.Calendar(user1events)

    # Example calendar 2
    user2events = [
        calendar.Event("2019-04-15T12:00:00-04:00", "2019-04-15T12:50:00-04:00")
    ]
    calendar2 = calendar.Calendar(user2events)

    # Correct return value
    freeevents = [
        calendar.Event("2019-04-15T11:50:00-04:00", "2019-04-15T12:00:00-04:00")
    ]
    freecalendar = calendar.Calendar(freeevents)

    rangestart = "2019-04-15T11:00:00-04:00"
    rangeend = "2019-04-15T12:50:00-04:00"
    result = calendar.get_shared_freetimes(rangestart, rangeend, calendar1, calendar2)
    result_string =""
    for event in result:
        result_string += event.starttime + ' - ' + event.endtime + '\n'
    print(result_string)
    assert result == freecalendar


if __name__ == '__main__':
    test1()
    test2()
    test3()
    print("Passed all tests.")
