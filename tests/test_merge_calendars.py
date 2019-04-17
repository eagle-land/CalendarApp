import app.calendar as calendar

def test1():
    # Example calendar 1
    user1events = []
    event1 = calendar.Event("2019-04-15T11:00:00-04:00", "2019-04-15T11:50:00-04:00")
    user1events.append(event1)
    calendar1 = calendar.Calendar(user1events)

    # Example calendar 2
    user2events = []
    event2 = calendar.Event("2019-04-15T12:00:00-04:00", "2019-04-15T12:50:00-04:00")
    user2events.append(event2)
    calendar2 = calendar.Calendar(user2events)

    # Correct return value
    mergedevents = [
        calendar.Event("2019-04-15T11:00:00-04:00", "2019-04-15T11:50:00-04:00"),
        calendar.Event("2019-04-15T12:00:00-04:00", "2019-04-15T12:50:00-04:00")
    ]
    mergedcalendar = calendar.Calendar(mergedevents)

    result = calendar.merge_calendars(calendar1, calendar2)
    result_string = ""
    for event in result:
        result_string += event.starttime + ' - ' + event.endtime + '\n'
    print(result_string)
    assert result == mergedcalendar

if __name__ == '__main__':
    test1()
