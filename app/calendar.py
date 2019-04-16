from . import calendar_auth

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
