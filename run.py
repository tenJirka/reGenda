import datetime
import calendar_caldav
import pytz
import yaml
import caldav
import calendar
import languages
from copy import deepcopy
from rm_pySAS import *

# Location of config file
CONFIG_FILE = '/opt/etc/reGenda/config.yml'

try:
        with open(CONFIG_FILE, 'r') as file:
            config = yaml.safe_load(file)
except:
    scene = Scene()
    scene.add(Label(50, 50, 150, 300, languages.english.configError))
    scene.display()
    exit()


# Setting up language
if "language" not in config:
    LANGUAGE = languages.english
else:
    if config['language'] == "czech":
        LANGUAGE = languages.czech
    elif config['language'] == "english":
        LANGUAGE = languages.english
    else:
        LANGUAGE = languages.english



def createListOfLabels(items, list = None, x=50, y=150) -> list:
    """
    Take list of strings and returns widgets that can could be displayed
    """
    if list == None:
        list = []
    for text in items:
        if list == []:
            list.append(Label(x, y, 150, 50, text))
        else:
            list.append(Label(list[-1].x, list[-1].y+50, list[-1].w, list[-1].h, text))
    return list
    


def createButtonArray(items, name, x=50, y=150, w=150, h=50) -> list:
    list = []
    index = 0
    for text in items:
        if list == []:
            list.append(Button(x, y, w, h, text, id=name+str(index)))
        else:
            list.append(Button(list[-1].x, list[-1].y+50, list[-1].w, list[-1].h, text, id=name+str(index)))
        index = index + 1
    return list

def daysInMonth(month: int, year: int) -> int:
    """
    Helper function that returns how many days does month have.
    """
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if calendar.isleap(year):
        days[1] = 29
    return days[month-1]


def monthView(month: int, year: int):
    """
    Scene with day pick from month view.
    """
    while(True):        
        y = 500
        x = 352
        deltaX = 100
        deltaY = 100

        today = datetime.date.today()

        if month > 12:
            year = year + 1
            month = month - 12
        elif month < 1:
            year = year - 1
            month = month + 12
        scene = Scene()
        first = datetime.date(int(year), int(month), 1).weekday()
        day = 0
        alldays = daysInMonth(month, year)
        
        
        scene.add(Justify("center"))
        scene.add(FontSize(40))
        i = 0
        while(i < 7):
            scene.add(Label(x+i*deltaX, y, deltaX, deltaY, LANGUAGE.daysOfWeek[i][:2]))
            i = i + 1

        y = y + deltaY
        if first == 0:
            y = y - deltaY
        
        while(day < alldays):
            weekday = (day + first) % 7
            if weekday == 0:
                y = y + deltaX
            scene.add(Button(x+weekday*deltaX, y, deltaX, deltaY, str(day+1), id=str(day+1)))
            if datetime.date(year, month, day+1) == today:
                scene.add(Label(x+weekday*deltaX, y+55, deltaX, 30, LANGUAGE.today, fontSize=20))
                scene.add(FontSize(40))
            day = day + 1
        
        scene.add(Label(0, 300, 1404, 100, LANGUAGE.months[month-1] + " " + str(year), id="next", justify="center", fontSize=70))
        scene.add(Button(75, 1750, 400, 50, "<<", id="previous", fontSize=50, justify="left"))
        scene.add(Button(929, 1750, 400, 50, ">>", id="next", justify="right", fontSize=50))
        scene.display()

        if "previous" == scene.input[0]:
            month = month - 1
        elif "next" == scene.input[0]:
            month = month + 1
        else:
            return[int(scene.input[0]), month, year]

def about():
    """
    About scene
    """
    scene = Scene()
    scene.add(Label(0, 400, 1404, 100, "reGenda", fontSize=100, justify="center"))
    scene.add(Label(0, 600, 1404, 100, "https://github.com/tenJirka/reGenda", fontSize=40))
    scene.add(Label(0, 670, 1404, 100, "Simple agenda app for reMarkable tablets", fontSize=40))
    scene.add(Label(0, 720, 1404, 100, "Written by tenJirka", fontSize=30))
    scene.add(Label(0, 1000, 1404, 100, "Credits:", fontSize=50))
    scene.add(Label(0, 1100, 1404, 100, "https://github.com/python-caldav/caldav", fontSize=30))
    scene.add(Label(0, 1170, 1404, 100, "https://github.com/rmkit-dev/rmkit"))
    scene.add(Button(1200, 50, 150, 50, LANGUAGE.back, id="exit"))

    scene.display()


def settings(principal):
    """
    Settings scene
    """
    global LANGUAGE
    with open(CONFIG_FILE, 'r') as file:
            config = yaml.safe_load(file)

    if 'toshow' not in config:
        with open(CONFIG_FILE, 'w') as file:
            config['toshow'] = []
            yaml.dump(config, file)
        toshow = []
    else:
        toshow=config['toshow']
    for event in toshow:
        if event not in principal.calendar_list:
            toshow.remove(event)
    while(True):
        widgets = []
        widgets.append(Justify("left"))
        widgets.append(FontSize(40))
        widgets.append(Label(200, 150, 150, 400, LANGUAGE.allCals))
        widgets.append(FontSize(30))
        widgets = widgets + createButtonArray(principal.calendar_list, "calendar", x=250, y=widgets[-2].y + 50, w=500)
        widgets.append(FontSize(40))
        widgets.append(Label(200, widgets[-2].y + 150, 150, 400, LANGUAGE.calsToSee))
        widgets.append(FontSize(30))
        widgets = widgets + createListOfLabels(toshow, x=250, y=widgets[-2].y + 50)
        widgets.append(Button(1200, 50, 150, 50, LANGUAGE.back, id="exit"))
        widgets.append(Justify("center"))
        widgets.append(Label(0, 1600, 1404, 50, LANGUAGE.language))
        widgets.append(Justify("left"))
        widgets.append(Button(520, 1650, 100, 50, "Czech", "czech"))
        widgets.append(Justify("right"))
        widgets.append(Button(784, 1650, 100, 50, "English", "english"))
        widgets.append(Button(652, 1750, 100, 50, "About", "about", justify="center"))
        output = passToSimple(widgets)[0]
        print(output)
        if "exit" in output:
            break
        elif "calendar" in output:
            selected=output.split(' ')
            for word in selected:
                if 'calendar' in word:
                    selected = word
                    break
            index = int(selected.replace('calendar', ''))
            if principal.calendar_list[index] in toshow:
                toshow.remove(principal.calendar_list[index])
            else:
                toshow.append(principal.calendar_list[index])
            toshow.sort()
        elif "czech" in output:
            config['language'] = "czech"
            LANGUAGE = languages.czech
            with open(CONFIG_FILE, 'w') as file:
                yaml.dump(config, file)
        elif "about" in output:
            about()
        elif "english" in output:
            config['language'] = "english"
            LANGUAGE = languages.english
            with open(CONFIG_FILE, 'w') as file:
                yaml.dump(config, file)


    with open(CONFIG_FILE, 'w') as file:
            config['toshow'] = toshow
            yaml.dump(config, file)



def selectCalendars(principal, names):
    """
    Gets lists of calendar and then initialize related calendar connections
    """
    calendars = []
    for calendar in names:
        calendars.append(principal.principal.calendar(name=calendar))
    return calendars


def connect():
    """
    Function that connects to server
    """
    with open(CONFIG_FILE, 'r') as file:
            config = yaml.safe_load(file)

    server = config['server']
    try:
        kalendar = calendar_caldav.Calendar(server['url'], server['user'], server['password'])
    except caldav.lib.error.AuthorizationError:
        scene = Scene(timeOut=1)
        scene.add(Label(150, 150, 150, 400, LANGUAGE.loginFailed, fontSize=30))
        scene.display()
        exit()
    except:
        scene = Scene()
        scene.add(Label(150, 150, 150, 400, LANGUAGE.somethingError, fontSize=30))
        scene.add(Button(1000, 1500, 400, 50, LANGUAGE.retry))
        scene.display()
        kalendar = connect()
    return kalendar


def getEvents(start, toshow):
    """
    Get events from server based on start date and calendars that will be downloaded from
    """
    events = []
    for calendar in toshow:
        calendarEvents = calendar.search(
            start=start,
            end=start + datetime.timedelta(days=1),
            event=True,
            expand=True,
        )
        if calendarEvents:
            for event in calendarEvents:
                dtstart = event.icalendar_component.get("dtstart")
                dtstart_dt = dtstart and dtstart.dt
                dtend = event.icalendar_component.get("dtend")
                dtend_dt = dtend and dtend.dt
                try:
                    dtstart_dt = dtstart_dt.astimezone(pytz.timezone("Europe/Prague"))
                    dtend_dt = dtend_dt.astimezone(pytz.timezone("Europe/Prague"))
                except:
                    pass
                if "LOCATION" in event.icalendar_component:
                    location = event.icalendar_component['location']
                else:
                    location = None  
                if "DESCRIPTION" in event.icalendar_component:
                    description = event.icalendar_component['description']
                else:
                    description = None                 
                events.append(calendar_caldav.Event(event.icalendar_component["summary"],\
                                                    calendar.name, dtstart_dt, dtend_dt, location, description))
    return events

def eventsToWidgets(events, start, x = 100, y=300) -> list:
    """
    Takes list of widgets and return list of widgets that can be displayed
    """    
    sas = []
    i = 0
    for event in events:
        yy = 0
        calendar = event.calendar
        if len(calendar) > 19:
            calendar = calendar[:19] + "..."
        location = event.location
        if len(location) > 19:
            location = location[:19] + "..."
        name = event.name
        if len(name) > 41:
            name = name[:39] + "..."
        try:
            zacatek = str(event.start.hour).zfill(2) + ":" + str(event.start.minute).zfill(2)
            konec = str(event.end.hour).zfill(2) + ":" + str(event.end.minute).zfill(2)
            if event.start.timestamp() < datetime.datetime.combine(start, datetime.datetime.min.time()).timestamp():
                zacatek = "00:00"
            if event.end.timestamp() > datetime.datetime.combine(start, datetime.datetime.max.time()).timestamp():
                konec = "00:00"
            cas = zacatek + " - " + konec
        except:
            cas = LANGUAGE.allday
        if cas == "00:00 - 00:00":
            cas = LANGUAGE.allday

        sas.append(Justify("left"))
        sas.append(FontSize(40))
        sas.append(Button(x + 350, y, 300, 50, name, id=str(i)))
        sas.append(FontSize(22))
        sas.append(Justify("center"))
        sas.append(Label(x, y, 300, 50, calendar))
        y = y + 30
        sas.append(FontSize(35))
        sas.append(Justify("center"))
        sas.append(Label(x, y, 300, 50, cas))
        sas.append(FontSize(22))
        y = y + 30
        if event.description != "":
            sas.append(Justify("left"))
            sas.append(Paragraph(x + 370, y, 700, 50, event.description))
            for letter in event.description:
                if letter == '\n':
                    yy = yy + 22
        y = y + 20
        if event.location != "":
            sas.append(Justify("center"))
            sas.append(Label(x, y, 300, 50, location))
        y = y+60+yy
        i = i + 1

    return sas


def eventDetails(event: calendar_caldav.Event) -> None:
    """
    Scene with details of one vent
    """
    scene = Scene()

    scene.add(Button(1200, 50, 150, 50, LANGUAGE.back, id="exit"))

    # Event name
    scene.add(Label(200, 200, 1004, 100, event.name, justify="left", fontSize=70))

    # Source calendar
    scene.add(Label(200, 400, 200, 100, LANGUAGE.calendar, fontSize=40, justify="right"))
    scene.add(Label(450, 400, 754, 100, event.calendar, fontSize=40, justify="left"))

    # Start of event
    scene.add(Label(200, 480, 200, 100, LANGUAGE.start, fontSize=40, justify="right"))
    if type(event.start) is datetime.date:
        scene.add(Label(450, 480, 754, 100, LANGUAGE.daysOfWeek[event.start.weekday()] + " - " + str(event.start.day) + "." + str(event.start.month) + "." + str(event.start.year),\
                        fontSize=40, justify="left"))
    else:
        scene.add(Label(450, 480, 754, 100, LANGUAGE.daysOfWeek[event.start.weekday()] + " " + str(event.start.hour).zfill(2) + ":" + str(event.start.minute).zfill(2) + " - " +\
                        str(event.start.day) + "." + str(event.start.month) + "." + str(event.start.year), fontSize=40, justify="left"))
    
    # End of event
    scene.add(Label(200, 560, 200, 100, LANGUAGE.end, fontSize=40, justify="right"))
    if type(event.end) is datetime.date:
        scene.add(Label(450, 560, 754, 100, LANGUAGE.daysOfWeek[event.end.weekday()] + " - " + str(event.end.day) + "." + str(event.end.month) + "." + str(event.end.year),\
                        fontSize=40, justify="left"))
    else:
        scene.add(Label(450, 560, 754, 100, LANGUAGE.daysOfWeek[event.end.weekday()] + " " + str(event.end.hour).zfill(2) + ":" + str(event.end.minute).zfill(2) + " - " +\
                        str(event.end.day) + "." + str(event.end.month) + "." + str(event.end.year), fontSize=40, justify="left"))

    # Event location
    if event.location != "":
        scene.add(Label(200, 640, 200, 100, LANGUAGE.location, fontSize=40, justify="right"))
        scene.add(Label(450, 640, 754, 100, event.location, fontSize=40, justify="left"))
    
    # Event description
    if event.description != "":
        scene.add(Label(200, 720, 200, 100, LANGUAGE.description, fontSize=40, justify="right"))
        scene.add(Paragraph(450, 720, 754, 1000, event.description, fontSize=40, justify="left"))

    scene.display()

def dayAgenda():
    """
    Day based interactive agenda
    """
    with open(CONFIG_FILE, 'r') as file:
            config = yaml.safe_load(file)
    start = datetime.date.today()

    kalendar = connect()

    if 'toshow' not in config:
        settings(kalendar)
        with open(CONFIG_FILE, 'r') as file:
            config = yaml.safe_load(file)

    toshow = selectCalendars(kalendar, config['toshow'])

    dayScene = Scene()
    dayScene.add(Button(75, 1750, 400, 50, LANGUAGE.prevDay, id="previous", fontSize=50, justify="left"))
    dayScene.add(Button(929, 1750, 400, 50, LANGUAGE.nextDay, id="next", justify="right", fontSize=50))
    dayScene.add(Button(1200, 50, 500, 50, LANGUAGE.settings, id="settings", fontSize=35, justify="left"))
    dayScene.add(Button(50, 50, 500, 50, LANGUAGE.exit, id="exit", fontSize=35, justify="left"))
    dayScene.add(Button(500, 1750, 200, 50, LANGUAGE.today, id="today", fontSize=50, justify="left"))
    dayScene.add(Button(800, 1750, 250, 50, LANGUAGE.jump, id="jump", fontSize=50, justify="left"))

    reload = True

    while(True):
        if reload:
            tmpDayScene = deepcopy(dayScene)
            events = getEvents(start, toshow)
            tmpDayScene.add(Label(100, 150, 150, 50, "" + LANGUAGE.daysOfWeek[start.weekday()]+ " " +str(start.day) + "." + str(start.month) + "." + str(start.year), justify="left", fontSize=50))
            if events != []:
                events.sort()
                labels = eventsToWidgets(events, start, x=150, y=300)
            else:
                labels = []
                labels.append(Label(200, 300, 150, 50, LANGUAGE.noEvents))

            tmpDayScene.add(labels)

        reload = True

        tmpDayScene.display()

        if "next" == tmpDayScene.input[0]:
            start = start + datetime.timedelta(days=1)
        elif "previous" == tmpDayScene.input[0]:
            start = start - datetime.timedelta(days=1)
        elif "today" == tmpDayScene.input[0]:
            start = datetime.date.today()
        elif "exit" == tmpDayScene.input[0]:
            break
        elif "jump" == tmpDayScene.input[0]:
            pick = monthView(start.month, start.year)
            start = datetime.date(pick[2], pick[1], pick[0])
        elif "settings" == tmpDayScene.input[0]:
            settings(kalendar)
            with open(CONFIG_FILE, 'r') as file:
                config = yaml.safe_load(file)
            toshow = selectCalendars(kalendar, config['toshow'])
        else:
            eventDetails(events[int(tmpDayScene.input[0])])         
            reload = False



def loading():
    """
    Just place up holder.
    """
    scene = Scene(timeOut=1)
    scene.add(Label(0, 700, 1404, 400, "reGenda", fontSize=100, justify="center"))
    scene.add(Label(0, 800, 1404, 400, LANGUAGE.loading, fontSize=40))
    scene.display()

def main():
    loading()
    dayAgenda()       

main()