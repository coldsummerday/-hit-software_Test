#!/usr/local/bin/python3
#!-*-coding:utf-8-*-
import cgi

from calendarHomework.Calendar import *
from calendarHomework.Converter import *

print ("Content-type:text/html")
print ()

form = cgi.FieldStorage()

year = form.getvalue("year")
month = form.getvalue("month")
day = form.getvalue("day")
try:
    year = int(year)
    month = int(month)
    day = int(day)
    if(year<1887 or year > 2100):
        print("Illegal date!")
        exit(0)
    date = Calendar(year,month,day)
    date.nextDay()
    print(date)
except ValueError:
    print("Illegal input!")
except ValueError:
    print("Illeagal input!")
