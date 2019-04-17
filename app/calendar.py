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

    def minuteAfter(self):
        year = int(self.endyear)
        month = int(self.endmonth)
        day = int(self.endday)
        hour = int(self.endhour)
        minute = int(self.endminute)
        second = self.endsecond
        offsetsign = self.endoffsetsign
        offsethour = self.endoffsethour
        offsetminute = self.endoffsetminute

        minute += 1
        if minute == 60:
            minute -= 60
            hour += 1
            if hour == 24:
                hour -= 24
                day += 1
                if day == 29 and month == 2 and not isLeapYear(year):
                    day -= 28
                    month += 1
                elif day == 30 and month == 2 and isLeapYear(year):
                    day -= 29
                    month += 1
                elif day == 31 and (month == 4 or month == 6 or month == 9 or month == 11):
                    day -= 30
                    month += 1
                elif day == 32:
                    day -= 31
                    month += 1
                    if month == 13:
                        month -= 12
                        year += 1

        year = str(year)
        month = str(month)
        day = str(day)
        hour = str(hour)
        minute = str(minute)

        if len(month) == 1:
            month = '0' + month
        if len(day) == 1:
            day = '0' + day
        if len(hour) == 1:
            hour = '0' + hour
        if len(minute) == 1:
            minute = '0' + minute

        return(
            year + '-' +
            month + '-' +
            day + 'T' +
            hour + ':' +
            minute + ':' +
            second +
            offsetsign +
            offsethour + ':' +
            offsetminute
        )


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

def isLeapYear(year):
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    else:
        return False

def get_calendar(start, end, timezone):
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

    response = calendar_auth.get_freebusy(body)
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


def get_shared_freetimes(rangestart, rangeend, calendar1, calendar2):
    freetimes = []
    index = 0
    freetimestart = rangestart
    while freetimestart < rangeend:
        # If freetimestart is in the middle of an event on either person's calendar, make it the end of that event.
        if calendar1[index].starttime <= freetimestart < calendar1[index].endtime:
            freetimestart = calendar1[index].endtime
        if calendar2[index].starttime <= freetimestart < calendar2[index].endtime:
            freetimestart = calendar2[index].endtime

        # Check if both calendars have another event.
        if index + 1 < len(calendar1) and index + 1 < len(calendar2):
            # If calendar 1's next event comes before calendar 2's,
            # or they start at the same time,
            # make the end of the freetime period the start of calendar 1's next event.
            if calendar1[index + 1].starttime <= calendar2[index + 1].starttime:
                freetimeend = calendar1[index + 1].starttime
                event = Event(freetimestart, freetimeend)
                freetimes.append(event)
                index += 1
                freetimestart = calendar1[index + 1].starttime
            # If calendar 2's next event comes before calendar 1's,
            # make the end of the freetime period the start of calendar 2's next event.
            elif calendar2[index + 1].starttime < calendar1[index + 1].starttime:
                freetimeend = calendar2[index + 1].starttime
                event = Event(freetimestart, freetimeend)
                freetimes.append(event)
                index += 1
                freetimestart = calendar2[index + 1].starttime
        # If only calendar 1 has another event,
        # make the end of the freetime period the start of its next event.
        elif index + 1 < len(calendar1):
            freetimeend = calendar1[index + 1].starttime
            event = Event(freetimestart, freetimeend)
            freetimes.append(event)
            index += 1
            freetimestart = calendar1[index + 1].starttime
        # If only calendar 2 has another event,
        # make the end of the freetime period the start of its next event.
        elif index + 1 < len(calendar2):
            freetimeend = calendar2[index + 1].starttime
            event = Event(freetimestart, freetimeend)
            freetimes.append(event)
            index += 1
            freetimestart = calendar2[index + 1].starttime
        # If neither calendar has another event,
        # make the end of the freetime period the end of the range.
        else:
            freetimeend = rangeend
            event = Event(freetimestart, freetimeend)
            freetimes.append(event)
            freetimestart = rangeend

    # Finished going through all events. Create a new calendar and return it.
    return Calendar(freetimes)
