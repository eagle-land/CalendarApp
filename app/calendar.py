import app.calendar_auth as calendar_auth


class Event:
    def __init__(self, startdatetime: str, enddatetime: str):
        # startdatetime: '2019-04-10T11:00:00-04:00'
        startdatetime = startdatetime.split('T')
        # startdatetime: ['2019-04-10', '11:00:00-04:00']

        startdate = startdatetime[0].split('-')
        # startdate: ['2019', '04', '10']
        self.startyear = startdate[0]               # '2019'
        self.startmonth = startdate[1]              # '04'
        self.startday = startdate[2]                # '10'

        starttime = startdatetime[1][:8].split(':')
        # starttime: ['11', '50', '00']
        self.starthour = starttime[0]               # '11'
        self.startminute = starttime[1]             # '50'
        self.startsecond = starttime[2][0:2]        # '00'

        startoffset = startdatetime[1][8:].split(':')
        # startoffset: ['-04', '00']
        self.startoffsetsign = startoffset[0][0:1]  # '-'
        self.startoffsethour = startoffset[0][1:]   # '04'
        self.startoffsetminute = startoffset[1]     # '00'

        # enddatetime: '2019-04-10T12:50:00-04:00'
        enddatetime = enddatetime.split('T')
        # enddatetime: ['2019-04-10', '12:50:00-04:00']

        enddate = enddatetime[0].split('-')
        # enddate: ['2019', '04', '10']
        self.endyear = enddate[0]  # '2019'
        self.endmonth = enddate[1]  # '04'
        self.endday = enddate[2]  # '10'

        endtime = enddatetime[1][:8].split(':')
        # endtime: ['12', '50', '00']
        self.endhour = endtime[0]  # '12'
        self.endminute = endtime[1]  # '50'
        self.endsecond = endtime[2][0:2]  # '00'

        endoffset = enddatetime[1][8:].split(':')
        # endoffset: ['-04', '00']
        self.endoffsetsign = endoffset[0][0:1]  # '-'
        self.endoffsethour = endoffset[0][1:]  # '04'
        self.endoffsetminute = endoffset[1]  # '00'

        self.starttime = self.toString('start')
        self.endtime = self.toString('end')

    def __eq__(self, other):
        if self.starttime == other.starttime and self.endtime == other.endtime:
            return True
        else:
            return False

    def toString(self, data):
        if data == 'start':
            return (
                    self.startyear + '-' +
                    self.startmonth + '-' +
                    self.startday + 'T' +
                    self.starthour + ':' +
                    self.startminute + ':' +
                    self.startsecond +
                    self.startoffsetsign +
                    self.startoffsethour + ':' +
                    self.startoffsetminute
            )
        elif data == 'end':
            return (
                    self.endyear + '-' +
                    self.endmonth + '-' +
                    self.endday + 'T' +
                    self.endhour + ':' +
                    self.endminute + ':' +
                    self.endsecond +
                    self.endoffsetsign +
                    self.endoffsethour + ':' +
                    self.endoffsetminute
            )
        else:
            return 'NULL'


class Calendar:
    def __init__(self, events):
        self.events = events

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.events):
            event = self.events[self.index]
            self.index += 1
            return event
        else:
            raise StopIteration

    def __getitem__(self, index):
        return self.events[index]

    def __len__(self):
        return len(self.events)

    def __eq__(self, other):
        if self.events == other.events:
            return True
        else:
            return False

    def __ne__(self, other):
        if self == other:
            return False
        else:
            return True


def compare_user_calendars(user1id, user2id, start, end, timezone):
    calendar1 = get_calendar(user1id, start, end, timezone)
    calendar2 = get_calendar(user2id, start, end, timezone)
    return get_shared_freetimes(start, end, calendar1, calendar2)


def get_calendar(userid, start, end, timezone):
    body = {
        "timeMin": start,
        "timeMax": end,
        "timeZone": timezone,
        "items": [
            {
                "id": "primary"
            }
        ],
    }

    response = calendar_auth.get_freebusy(userid, body)
    if not response:
        print('Error.')

    userevents = []
    calendars = response['calendars']
    calendar = calendars[body['items'][0]['id']]
    for busytimes in calendar:
        index = 0
        for busy in calendar[busytimes]:
            event = Event(calendar[busytimes][index]['start'], calendar[busytimes][index]['end'])
            userevents.append(event)
            index += 1

    return Calendar(userevents)


def getstarttime(elem):
    return elem.starttime


def merge_calendars(calendar1, calendar2):
    allevents = calendar1.events
    for event in calendar2:
        allevents.append(event)

    allevents.sort(key=getstarttime)
    index = 0
    while index + 1 < len(allevents):
        event1 = allevents[index]
        event2 = allevents[index + 1]
        # Event 2 fits inside event1.
        if event2.starttime >= event1.starttime and event2.endtime <= event1.endtime:
            allevents.pop(index + 1)
        # Event2 starts during the duration of event 1 and ends after event 1.
        elif event1.starttime <= event2.starttime <= event1.endtime < event2.endtime:
            allevents[index] = Event(event1.starttime, event2.endtime)
            allevents.pop(index + 1)
        index += 1
    return Calendar(allevents)


def get_shared_freetimes(rangestart, rangeend, calendar1, calendar2):
    # Merge calendars into one.
    calendar = merge_calendars(calendar1, calendar2)

    freetimes = []
    index = -1
    freetimestart = rangestart
    while index < len(calendar):
        if index == -1:
            event = calendar[index + 1]
        else:
            event = calendar[index]
        # If freetimestart is in the middle of an event on the calendar, make it the end of that event.
        if event.starttime <= freetimestart < event.endtime:
            freetimestart = event.endtime

        # If this is not the last event in the calendar, set the end time for the current free event as the start
        # time of the next event. Then, make the next free event start when the next event ends.
        if index + 1 < len(calendar):
            freetimeend = calendar[index + 1].starttime
            freeevent = Event(freetimestart, freetimeend)
            freetimestart = calendar[index + 1].endtime
        # If this is the last event, set the end time for the current free event as the end of the range.
        else:
            freetimeend = rangeend
            freeevent = Event(freetimestart, freetimeend)

        # Make sure we're not creating an event that's 0 minutes long.
        if not freeevent.starttime == freeevent.endtime:
            freetimes.append(freeevent)
        index += 1

    # Finished going through all events. Create a new calendar and return it.
    return Calendar(freetimes)
