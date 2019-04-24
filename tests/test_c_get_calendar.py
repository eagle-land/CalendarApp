import app.calendar as calendar


def test1():
    userid = "auth0|5cb50516ee4bd5113d54872b"
    start = "2019-04-15T00:00:00-04:00"
    end = "2019-04-21T00:00:00-04:00"
    timezone = "America/New_York"

    events = [
        calendar.Event("2019-04-15T11:00:00-04:00", "2019-04-15T11:50:00-04:00"),
        calendar.Event("2019-04-15T12:30:00-04:00", "2019-04-15T13:45:00-04:00"),
        calendar.Event("2019-04-15T19:00:00-04:00", "2019-04-15T20:15:00-04:00"),
        calendar.Event("2019-04-16T12:30:00-04:00", "2019-04-16T13:45:00-04:00"),
        calendar.Event("2019-04-16T20:00:00-04:00", "2019-04-16T22:00:00-04:00"),
        calendar.Event("2019-04-17T11:00:00-04:00", "2019-04-17T11:50:00-04:00"),
        calendar.Event("2019-04-17T12:30:00-04:00", "2019-04-17T13:45:00-04:00"),
        calendar.Event("2019-04-17T19:00:00-04:00", "2019-04-17T20:15:00-04:00"),
        calendar.Event("2019-04-18T12:30:00-04:00", "2019-04-18T13:45:00-04:00"),
        calendar.Event("2019-04-18T15:30:00-04:00", "2019-04-18T16:00:00-04:00"),
        calendar.Event("2019-04-19T11:00:00-04:00", "2019-04-19T11:50:00-04:00")
    ]
    correct_calendar = calendar.Calendar(events)

    result = calendar.get_calendar(userid, start, end, timezone)
    assert result == correct_calendar


if __name__ == '__main__':
    test1()
    print("Passed all tests.")
