#import requests
#from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import time
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
#functions
def to_miles(Km):
   return round(Km * 0.621371, 2)
def get_pace(dur, dis):
    try:
       hours = int(dur.split(':')[0]) + (float((dur.split(':')[1]))/ 60)
       return round(dis / hours, 2)
    except:
       print('%')
       # #URL
URL = 'https://ultrasignup.com/results_participant.aspx?fname=William&lname=Connell'
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
   races = accordion[0].find_elements_by_class_name('rowlines')
   #print(accordion[num].text) # works but just a test - need to use find_elements_by_class_name
   #in accordion-content
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
         dist = dist.upper()
         endtime = 'Future'
   elif len(race) < 4:
      endtime = race[2]
      age = ''
      dist = race[0].split('-')[-2].strip()
   else:
      dist = race[0].split('-')[-2].strip()
      endtime = race[3]
      age = race[4]
   if re.search(r'\d*:\d*.*$', endtime):
      if re.search(r'.*\d*K.*$', dist):
               #convert to mph
                found = re.search('\d*', dist)
                if found.group() == int:
                   p = to_miles(int(found.group()))
                   pace = get_pace(endtime, p)
      elif re.search(r'.*\d*.*MILER.*$', dist):
               found = re.search('\d*', dist)
               p = int(found.group())
               pace = get_pace(endtime, p)
      else:
               pace = 'X'
   else:
      pace = '$'
   racedict = {"Distance": dist, "Date": race[1], "Time": endtime, "Pace": pace, 'Age': age}
   print(racedict)

runners.append(rundata)
print(runners)
#find out why pace is fucked
    






