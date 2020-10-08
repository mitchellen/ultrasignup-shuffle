#import requests
#from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import time
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import matplotlib
#functions
def to_miles(Km):
   return round(Km * 0.621371, 2)
def get_pace(dur, dis):
    try:
       dis = dis.upper()
       if re.search(r'\d*:\d*.*$', dur):
          hours = int(dur.split(':')[0]) *60  + float((dur.split(':')[1]))
          if re.search(r'.*\d*K.*$', dis):
             found = re.search('\d*', dis)
             p = to_miles(int(found.group()))
             result = round(hours / p, 2)
          elif re.search(r'.*\d*.*MILER.*$', dis):
             found = re.search('\d*', dis)
             p = int(found.group())
             
             result = round(hours / p, 2)
          elif re.search(r'^.*MARATHON.*$', dis):
             result = round(hours / 26.2, 2)
       else:
          result = 'WTF'
       return result
    except:
        return 'No Clue'
       # #URL
URL = 'https://ultrasignup.com/results_participant.aspx?fname=Cera&lname=Jones'
#URL = 'https://ultrasignup.com/results_participant.aspx?fname=William&lname=Connell'
# try chrome if it gets too gross
opts = Options()
opts.add_argument('--headless')
# print(opts)
browser = Firefox(options=opts)
browser.get(URL)
store = browser
# There is a wwird thing that all race results show up in the same pot despite multiple participants
# How do I sort this out?
runners = []
acchead = browser.find_elements_by_class_name('accordion-heading')
accordion = browser.find_elements_by_class_name('accordion-content')
for num, runner in enumerate(acchead, start=0):
   rundata = {}
   runarray = runner.text.split('\n')
   runhash = {'Age': runarray[0].split(' ')[-1], 'Number of Races': runarray[1].split(' ')[0]}
   rundata.update(runhash)
   races = accordion[num].find_elements_by_class_name('rowlines')
   #print(accordion[num].text) # works but just a test - need to use find_elements_by_class_name
   #in accordion-content
   event = []
   for r in races:
      iss = ''
      # How do I find DNS,DNF,Future
      race = r.text.split('\n')
      # print(race)
      if len(race) < 3:
         if race[0].split('-')[-1].strip() == 'DNS' or  race[0].split('-')[-1].strip() == 'DNF':
            iss = race[0].split('-')[-1].strip()
            dist = race[0].split('-')[-3].strip()
            endtime = iss
         else:
            dist = race[0].split('-')[-2].strip()
            age = ''
            endtime = 'Future'
            racedict = {"Distance": dist, "Date": race[1], "Time": endtime}
      elif len(race) < 4:
         endtime = race[2]
         age = ''
         dist = race[0].split('-')[-2].strip()
         pace = get_pace(endtime, dist)
         racedict = {"Distance": dist, "Date": race[1], "Time": endtime, "Pace": pace, 'Age': age}
      else:
         dist = race[0].split('-')[-2].strip()
         endtime = race[3]
         age = race[4].split(': ')[1]
         pace = get_pace(endtime, dist)
         racedict = {"Distance": dist, "Date": race[1], "Time": endtime, "Pace": pace , 'Age': age}
      event.append(racedict)
   rundata.update({'Events': event})
   #print(racedict)
   
   runners.append(rundata)
print(runners)
#find out why pace is fucked
    






