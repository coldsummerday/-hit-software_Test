#!/usr/bin/python3
from .Converter import LunarSolarConverter,Lunar,Solar

class Calendar(object):

    def __init__(self,year,month,day):
        self.year = year
        self.month = month
        self.day = day
        self.monthDayHash ={1:31,2:28,3:31,4:30,5:31,
                         6:30,7:31,8:31,9:30,10:31,11:30,12:31}
        self.judgeLeapYear()
        self.heavenlysStems = ["甲","乙","丙","丁","戊","己","庚","辛","壬	","癸"]
        self.earthlyBranches = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
        self.weekdays = ["周一","周二","周三","周四","周五","周六","周日"]
        self.convert = LunarSolarConverter()

    def judgeLeapYear(self):
        self.flag = False
        if((self.year %100)==0 ):
            if ((self.year %400) ==0):
                self.flag = True
        else:
            if ((self.year %4)==0):
                self.flag = True

        if(self.flag):
            self.monthDayHash[2]=29
        else:
            self.monthDayHash[2]=28


    def nextDay(self):
        if(not self.legalDate()):
            return
        if ((self.day+1)<=self.monthDayHash[self.month]):
            self.day = self.day+1
        else:
            self.day = 1
            self.year  = self.year + (self.month) / 12
            if (self.year > 2101):
                self.year = 1900
            self.judgeLeapYear()
            self.month = (self.month + 1 ) % 12
            self.month = 12 if self.month==0 else self.month

    def getWeekDayIndex(self,y,m,d):
        if m==1 or m==2:
            m = m+12
            y = y-1
        w = ((d + 2 * m + 3 * (m+1) / 5 + y + y/4 - y/100 + y/400) + 1) % 7
        return int(w)



    def legalDate(self):
        self.legal = True
        self.weekday = self.weekdays[self.getWeekDayIndex(self.year,self.month,self.day)]
        if (self.year>=2101 or self.year <= 1899):
            self.legal = False
            return self.legal
        if (self.month>12 or self.month < 1):
            self.legal = False
            return self.legal
        if (self.day<1 or self.day > self.monthDayHash[self.month]):
            self.legal =False
            return self.legal
        return self.legal

    def getweek(self):
        from datetime import date
        self.weekday = self.weekdays[date(int(self.year),int(self.month),int(self.day)).weekday()]




    def __str__(self):
        self.legalDate()
        self.getweek()
        Lunar=self.convert.SolarToLunar(Solar(int(self.year),int(self.month),int(self.day)))
        if (self.legal):
            return "%s\n%d年/%d月/%d日\t%s" %( Lunar.__str__(),self.year,self.month,self.day,self.weekday)
        else:
            return "Illegal date!"+"%d/%d/%d" %(self.year,self.month,self.day)






