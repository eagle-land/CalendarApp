import app.calendar as calendar


def test_merge_calendar1():
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


def test_merge_calendar2():
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
    assert result == mergedcalendar


def test_merge_calendar3():
    # Example calendar 1
    user1events = [
        calendar.Event("2019-05-15T13:00:00-04:00", "2019-05-15T20:00:00-04:00")
        # year-month-day(T)two digit hours: two digit minutes: two digit seconds(-04 is subtracted from UTC, this for example is EST eastern time)
    ]
    calendar1 = calendar.Calendar(user1events)  # put user1 events into calendar

    # second user calendar events defined
    user2events = [
        calendar.Event("2019-05-15T08:00:00-04:00", "2019-05-15T22:00:00-04:00")
    ]
    calendar2 = calendar.Calendar(user2events)  # put user2 events into calendar

    # array with correct variables for compare
    mergedevents = [
        calendar.Event("2019-05-15T08:00:00-04:00", "2019-05-15T22:00:00-04:00")
    ]

    mergedcalendar = calendar.Calendar(mergedevents)  # compare calendar variable
    result = calendar.merge_calendars(calendar1, calendar2)  # test variables compare
    assert result == mergedcalendar  # assert will say whether the test failed or not
def test_merge_calendar4():
    # Example calendar 1
    user1events = [
        calendar.Event("2019-05-16T13:00:00-04:00", "2019-05-16T20:00:00-04:00")
        # year-month-day(T)hours:minutes:seconds(-04 is subtracted from UTC this is EST
    ]
    calendar1 = calendar.Calendar(user1events)  # put user1 events into calendar

    # second user calendar events defined
    user2events = [
        calendar.Event("2019-05-16T08:00:00-04:00", "2019-05-16T22:00:00-04:00")
    ]
    calendar2 = calendar.Calendar(user2events)  # put user2 events into calendar

    # array with correct variables for compare
    mergedevents = [
        calendar.Event("2019-05-16T08:00:00-04:00", "2019-05-16T22:00:00-04:00")
    ]

    mergedcalendar = calendar.Calendar(mergedevents)  # compare calendar variable
    result = calendar.merge_calendars(calendar1, calendar2)  # test variables compare
    assert result == mergedcalendar  # assert will say whether the test failed or not

def test_merge_calendar5():
    # Example calendar 1
    user1events = [
        calendar.Event("2019-05-15T10:00:00-04:00", "2019-05-15T20:00:00-04:00")
        # year-month-day(T)hours:minutes:seconds(-04 is subtracted from UTC this is EST
    ]
    calendar1 = calendar.Calendar(user1events)  # put user1 events into calendar

    # second user calendar events defined
    user2events = [
        calendar.Event("2019-05-15T10:00:00-04:00", "2019-05-15T22:00:00-04:00")
    ]
    calendar2 = calendar.Calendar(user2events)  # put user2 events into calendar

    # array with correct variables for compare
    mergedevents = [
        calendar.Event("2019-05-15T10:00:00-04:00", "2019-05-15T22:00:00-04:00")
    ]

    mergedcalendar = calendar.Calendar(mergedevents)  # compare calendar variable
    result = calendar.merge_calendars(calendar1, calendar2)  # test variables compare
    assert result == mergedcalendar  # assert will say whether the test failed or not

if __name__ == '__main__':
    test_merge_calendar1()
    test_merge_calendar2()
    test_merge_calendar3()
    test_merge_calendar4()
    test_merge_calendar5()
    print("Passed all tests.")
