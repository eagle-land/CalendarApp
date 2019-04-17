import app.calendar as calendar

def test1():
    user1events = []
    event1 = calendar.Event("2019-04-15T11:00:00-04:00", "2019-04-15T11:50:00-04:00")
    user1events.append(event1)
    calendar1 = calendar.Calendar(user1events)

    user2events = []
    event2 = calendar.Event("2019-04-15T12:00:00-04:00", "2019-04-15T12:50:00-04:00")
    user2events.append(event2)
    calendar2 = calendar.Calendar(user2events)

    freeevents = []
    freeevent = calendar.Event("2019-04-15T11:50:00-04:00", "2019-04-15T12:00:00-04:00")
    freeevents.append(freeevent)
    freecalendar = calendar.Calendar(freeevents)

    rangestart = event1.starttime
    rangeend = event2.endtime
    result = calendar.get_shared_freetimes(rangestart, rangeend, calendar1, calendar2)
    result_string =""
    for event in result:
        result_string += event.starttime + ' - ' + event.endtime + '\n'
    print(result_string)
    assert result == freecalendar

if __name__ == '__main__':
    test1()
