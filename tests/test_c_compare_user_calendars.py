import app.calendar as calendar




def test1():
    # User ID 1
    user1id = ""    # Fill this in!

    # User ID 2
    user2id = ""    # Fill this in!

    # Range
    start = "2019-04-01T00:00:00-04:00" # year-month-day(T)two digit hours: two digit minutes: two digit seconds(-04 is subtracted from UTC, this for example is EST eastern time)
    end = "2019-04-02T00:00:00-04:00"
    timezone = "America/New_York" #only use this as the timezone

    # Correct return value
    freeevents = [
        # Create a calendar containing the correct shared freetimes between both user calendars.
    ]
    freecalendar = calendar.Calendar(freeevents)

    result = calendar.compare_user_calendars(user1id, user2id, start, end, timezone)
    assert result == freecalendar


if __name__ == '__main__':
    test1()
    print("Passed all tests.")
