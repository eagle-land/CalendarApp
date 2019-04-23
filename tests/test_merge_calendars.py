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
    mergedevents = [
        calendar.Event("2019-04-15T11:00:00-04:00", "2019-04-15T11:50:00-04:00"),
        calendar.Event("2019-04-15T12:00:00-04:00", "2019-04-15T12:50:00-04:00")
    ]
    mergedcalendar = calendar.Calendar(mergedevents)

    result = calendar.merge_calendars(calendar1, calendar2)
    assert result == mergedcalendar


def test2():
    # Example calendar 1
    user1events = [
        calendar.Event("2019-04-15T11:00:00-04:00", "2019-04-15T12:00:00-04:00")
    ]
    calendar1 = calendar.Calendar(user1events)

    # Example calendar 2
    user2events = [
        calendar.Event("2019-04-15T12:00:00-04:00", "2019-04-15T12:50:00-04:00")
    ]
    calendar2 = calendar.Calendar(user2events)

    # Correct return value
    mergedevents = [
        calendar.Event("2019-04-15T11:00:00-04:00", "2019-04-15T12:50:00-04:00")
    ]
    mergedcalendar = calendar.Calendar(mergedevents)

    result = calendar.merge_calendars(calendar1, calendar2)
    result_string = ""
    for event in result:
        result_string += event.starttime + ' - ' + event.endtime + '\n'
    print(result_string)
    assert result == mergedcalendar


def test3():
    # Example calendar 1
    user1events = [
        calendar.Event("2019-05-15T13:00:00-04:00", "2019-05-15T20:00:00-04:00")
        # year-month-day(T)hours:minutes:seconds(-04 is subtracted from UTC this is EST
    ]
    calendar1 = calendar.Calendar(user1events)  # put user1 events into calendar

    # second user calendar events defined
    user2events = [
        calendar.Event("2019-05-15T8:00:00-04:00", "2019-05-15T22:00:00-04:00")
    ]
    calendar2 = calendar.Calendar(user2events)  # put user2 events into calendar

    # array with correct variables for compare
    mergedevents = [
        calendar.Event("2019-05-15T08:00:00-04:00", "2019-05-15T22:00:00-04:00")
    ]

    mergedcalendar = calendar.Calendar(mergedevents)  # compare calendar variable
    result = calendar.merge_calendars(calendar1, calendar2)  # test variables compare
    result_string = ""
    for event in result:
        result_string += event.starttime + ' - ' + event.endtime + '\n'
    print(result_string)
    assert result == mergedcalendar  # assert will say whether the test failed or not


if __name__ == '__main__':
    test1()
    test2()
    test3()
    print("Passed all tests.")