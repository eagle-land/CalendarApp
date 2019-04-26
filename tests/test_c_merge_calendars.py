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


def test_merge_calendar6():
    # User ID 1
    user1id = "auth0|5cb50516ee4bd5113d54872b"  # Jareds ID!

    # User ID 2
    user2id = "auth0|5cbe466fd1f05811d6866c0b"  # Jacobs ID!

    # Range
    start = "2019-04-01T00:00:00-04:00"
    end = "2019-04-05T00:00:00-04:00"
    timezone = "America/New_York"

    calendar1 = calendar.get_calendar(user1id, start, end, timezone)
    calendar2 = calendar.get_calendar(user2id, start, end, timezone)

    mergedevents = [
        calendar.Event("2019-04-01T06:00:00-04:00", "2019-04-01T07:30:00-04:00"),
        calendar.Event("2019-04-01T09:00:00-04:00", "2019-04-01T17:00:00-04:00"),
        calendar.Event("2019-04-01T19:00:00-04:00", "2019-04-01T20:15:00-04:00"),
        calendar.Event("2019-04-02T08:30:00-04:00", "2019-04-02T09:30:00-04:00"),
        calendar.Event("2019-04-02T11:00:00-04:00", "2019-04-02T12:15:00-04:00"),
        calendar.Event("2019-04-02T12:30:00-04:00", "2019-04-02T13:45:00-04:00"),
        calendar.Event("2019-04-02T14:30:00-04:00", "2019-04-02T17:00:00-04:00"),
        calendar.Event("2019-04-02T20:00:00-04:00", "2019-04-02T22:00:00-04:00"),
        calendar.Event("2019-04-03T08:00:00-04:00", "2019-04-03T12:00:00-04:00"),
        calendar.Event("2019-04-03T13:10:00-04:00", "2019-04-03T14:00:00-04:00"),
        calendar.Event("2019-04-03T15:30:00-04:00", "2019-04-03T16:30:00-04:00"),
        calendar.Event("2019-04-03T17:30:00-04:00", "2019-04-03T18:45:00-04:00"),
        calendar.Event("2019-04-03T19:00:00-04:00", "2019-04-03T20:15:00-04:00"),
        calendar.Event("2019-04-04T07:00:00-04:00", "2019-04-04T08:30:00-04:00"),
        calendar.Event("2019-04-04T11:00:00-04:00", "2019-04-04T12:15:00-04:00"),
        calendar.Event("2019-04-04T12:30:00-04:00", "2019-04-04T13:45:00-04:00"),
        calendar.Event("2019-04-04T14:30:00-04:00", "2019-04-04T17:00:00-04:00"),
        calendar.Event("2019-04-04T21:00:00-04:00", "2019-04-04T22:30:00-04:00")
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
    test_merge_calendar6()
    print("Passed all tests.")
