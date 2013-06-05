#!/usr/bin/env python
# -*- coding: UTF-8 -*-

try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree
import gdata.calendar.data
import gdata.calendar.client
import gdata.acl.data
import atom.data
import time
import local_settings

import  csv, unidecode, re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

tipus_actual = ''
dia_actual = ''
hora_actual = ''

if len(sys.argv) < 2:
    sys.stderr.write('Usage: sys.argv[0] inputfile')
    sys.exit(1)

infilepath = sys.argv[1]

def PrintUserCalendars(calendar_client):
    feed = calendar_client.GetAllCalendarsFeed()
    print feed.title.text
    for i, a_calendar in enumerate(feed.entry):
        print '\t%s. %s. %s' % (i, a_calendar.title.text,a_calendar.content.src,)
    return feed.entry

def GetCalendarUrl(calendar_list,calendar_name):
    url = ''
    for i, a_calendar in enumerate(calendar_list):
        if a_calendar.title.text == calendar_name:
            url = a_calendar.content.src
            break
    return url




def CreateCalendar(calendar_client):
    # Create the calendar
    calendar = gdata.calendar.data.CalendarEntry()
    calendar.title = atom.data.Title(text='XVI JAEM - Palma 2013')
    calendar.summary = atom.data.Summary(text='Agenda XVI JAEM')
    calendar.where.append(gdata.calendar.data.CalendarWhere(value='Palma'))
    calendar.color = gdata.calendar.data.ColorProperty(value='#2F6309')
    calendar.timezone = gdata.calendar.data.TimeZoneProperty(value='Europe/Madrid')
    calendar.hidden = gdata.calendar.data.HiddenProperty(value='false')
    new_calendar = calendar_client.InsertCalendar(new_calendar=calendar)
    return new_calendar

def InsertSingleEvent(calendar_client, calendar_url, title,content, where,start_time=None, end_time=None):
    event = gdata.calendar.data.CalendarEventEntry()
    event.title = atom.data.Title(text=title)
    event.content = atom.data.Content(text=content)
    event.where.append(gdata.calendar.data.CalendarWhere(value=where))

    if start_time is None:
      # Use current time for the start_time and have the event last 1 hour
      start_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
      end_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime(time.time() + 3600))
    event.when.append(gdata.calendar.data.When(start=start_time, end=end_time))

    new_event = calendar_client.InsertEvent(event,calendar_url)

    print 'New single event inserted: %s' % (new_event.id.text,)
    print '\tEvent edit URL: %s' % (new_event.GetEditLink().href,)
    print '\tEvent HTML URL: %s' % (new_event.GetHtmlLink().href,)

    return new_event

def local_to_utc(t):
    secs = time.mktime(t)
    return time.gmtime(secs)

def main():
    client = gdata.calendar.client.CalendarClient(source='xvijaem-generacalendari-v1')
    client.ClientLogin(local_settings.CAL_USER, local_settings.CAL_PWD, client.source)
    #
    calendar_list = PrintUserCalendars(client)
    calendari_url = GetCalendarUrl(calendar_list,'XVI JAEM - Palma 2013')
    if len(calendari_url) == 0:
        CreateCalendar(client)
        calendar_list = PrintUserCalendars(client)
        calendari_url = GetCalendarUrl(calendar_list,'XVI JAEM - Palma 2013')

    print calendari_url

    seccions = []

    with open(infilepath, 'rb') as infile:
        aportacions = csv.DictReader(infile, delimiter=',')
        for aportacio in aportacions:
            title = "%s - %s" % (aportacio['Tipologia'].decode('utf-8') ,aportacio['Títol'].decode('utf-8'))
            print 'Processa ', title
            where = aportacio['Edifici'].decode('utf-8') + '. ' + aportacio['Aula'].decode('utf-8')

            autors = aportacio['Autors'].decode('utf-8')
            afiliacio = aportacio['Afiliació'].decode('utf-8')
            resum = aportacio['Resum'].decode('utf-8')
            content = autors + '\n' + afiliacio + '\n\n' + resum

            hora = aportacio['Hora'].decode('utf-8')
            hora_parts = hora.split(' ')

            str_start_time = '2013-07-0%s %s' % (aportacio['Dia'].decode('utf-8'),hora_parts[0])
            t_start_time = time.strptime(str_start_time,'%Y-%m-%d %H:%M')

            str_end_time = '2013-07-0%s %s' % (aportacio['Dia'].decode('utf-8'),hora_parts[2])
            t_end_time = time.strptime(str_end_time,'%Y-%m-%d %H:%M')

            start_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', local_to_utc(t_start_time))
            end_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', local_to_utc(t_end_time))
            InsertSingleEvent(client, calendari_url, title,content, where,start_time,end_time)



if __name__ == '__main__':
    main()