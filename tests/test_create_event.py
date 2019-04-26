import app.calendar as calendar
import app.calendar_auth as calendar_auth


def test1():
    #user1id, user2id, summary, location, startdatetime, enddatetime, timezone
    user1id = "auth0|5cb50516ee4bd5113d54872b"
    user2id = "auth0|5cb50516ee4bd5113d54872b"
    summary = "Test Event 1"
    location = "Location"
    start = "2019-04-26T07:30:00-04:00"
    end = "2019-04-26T07:31:00-04:00"
    timezone = "America/New_York"

    print(calendar_auth.create_event(user1id, user2id, summary, location, start, end, timezone))


if __name__ == '__main__':
    test1()
    print("Passed all tests.")
