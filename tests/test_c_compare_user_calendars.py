import app.calendar as calendar

def test1():
    # User ID 1
    user1id = "auth0|5cb50516ee4bd5113d54872b"    # Jared's ID

    # User ID 2
    user2id = "auth0|5cbe466fd1f05811d6866c0b"    # Jacob's ID

    # Range
    start = "2019-04-01T00:00:00-04:00" # year-month-day(T)two digit hours: two digit minutes: two digit seconds(-04 is subtracted from UTC, this for example is EST eastern time)
    end = "2019-04-05T00:00:00-04:00"
    timezone = "America/New_York" #only use this as the timezone

    # Correct return value
    # Create a calendar containing the correct shared freetimes between both user calendars.
    freeevents = [
        calendar.Event("2019-04-01T00:00:00-04:00", "2019-04-01T06:00:00-04:00"),
        calendar.Event("2019-04-01T07:30:00-04:00", "2019-04-01T09:00:00-04:00"),
        calendar.Event("2019-04-01T17:00:00-04:00", "2019-04-01T19:00:00-04:00"),
        calendar.Event("2019-04-01T20:15:00-04:00", "2019-04-02T08:30:00-04:00"),
        calendar.Event("2019-04-02T09:30:00-04:00", "2019-04-02T11:00:00-04:00"),
        calendar.Event("2019-04-02T12:15:00-04:00", "2019-04-02T12:30:00-04:00"),
        calendar.Event("2019-04-02T13:45:00-04:00", "2019-04-02T14:30:00-04:00"),
        calendar.Event("2019-04-02T17:00:00-04:00", "2019-04-02T20:00:00-04:00"),
        calendar.Event("2019-04-02T22:00:00-04:00", "2019-04-03T08:00:00-04:00"),
        calendar.Event("2019-04-03T12:00:00-04:00", "2019-04-03T13:10:00-04:00"),
        calendar.Event("2019-04-03T14:00:00-04:00", "2019-04-03T15:30:00-04:00"),
        calendar.Event("2019-04-03T16:30:00-04:00", "2019-04-03T17:30:00-04:00"),
        calendar.Event("2019-04-03T18:45:00-04:00", "2019-04-03T19:00:00-04:00"),
        calendar.Event("2019-04-03T20:15:00-04:00", "2019-04-04T07:00:00-04:00"),
        calendar.Event("2019-04-04T08:30:00-04:00", "2019-04-04T11:00:00-04:00"),
        calendar.Event("2019-04-04T12:15:00-04:00", "2019-04-04T12:30:00-04:00"),
        calendar.Event("2019-04-04T13:45:00-04:00", "2019-04-04T14:30:00-04:00"),
        calendar.Event("2019-04-04T17:00:00-04:00", "2019-04-04T21:00:00-04:00"),
        calendar.Event("2019-04-04T22:30:00-04:00", "2019-04-05T00:00:00-04:00"),
    ]
    freecalendar = calendar.Calendar(freeevents)

    result = calendar.compare_user_calendars(user1id, user2id, start, end, timezone)
    assert result == freecalendar


if __name__ == '__main__':
    test1()
    print("Passed all tests.")
