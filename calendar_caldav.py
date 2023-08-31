# Support module that contains classes used from main script

import datetime
import caldav

class Calendar:
    """
    Represents one server that will be loaded.
    """
    def __init__(self, url, user, password):
        with caldav.DAVClient(
        url=url,
        username=user,
        password=password,
        ) as client:
            self.principal = client.principal()
            self.calendar_list = [x.name for x in self.principal.calendars()]
            self.calendar_list.sort()

class Event:
    """
    Represent one event loaded from caldav.
    """
    def __init__(self, name, calendar, start, end, location, description):
        self.name = name
        self.calendar = calendar
        self.start = start
        self.end = end
        self.location = location
        if self.location == None:
            self.location = ""
        self.description = description
        if self.description == None:
            self.description = ""
    
    # Functions below were added due to sort function.
    def __eq__(self, other):
        zacatek1 = self.start
        if type(zacatek1) is datetime.date:
            zacatek1 = datetime.datetime.combine(zacatek1, datetime.datetime.min.time())
        zacatek2 = other.start
        if type(zacatek2) is datetime.date:
            zacatek2 = datetime.datetime.combine(zacatek2, datetime.datetime.min.time())
        return zacatek1.timestamp() == zacatek2.timestamp()

    def __lt__(self, other):
        zacatek1 = self.start
        if type(zacatek1) is datetime.date:
            zacatek1 = datetime.datetime.combine(zacatek1, datetime.datetime.min.time())
        zacatek2 = other.start
        if type(zacatek2) is datetime.date:
            zacatek2 = datetime.datetime.combine(zacatek2, datetime.datetime.min.time())
        return zacatek1.timestamp() < zacatek2.timestamp()