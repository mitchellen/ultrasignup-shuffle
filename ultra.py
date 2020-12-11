
"""Do some Stuff
"""
###
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import csv
import time
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
#classes
class Runner:
    '''Doc
    '''
    def __init__(self, array, url, expected):
        
       #age,number of races, url
      self.events = []
      self.url = url
      self.expectedfinish = expected
      self.first = array[0].split(' ')[0]
      self.last = array[0].split(' ')[1]
      self.age = self.just_age(array[0].split(' ')[-1])
      self.total = array[1].split(' ')[0]
      self.division = self.m_or_f(array[0].split(' ')[-1])
    def m_or_f(self, age):
        return (age[:1])
    def just_age(self, age):
        return (age[1:])
    def minus_future(self, events):
        notlist = []
        for e in events:
            if e['status'] == 'Complete':
                notlist.append(e)
        return len(notlist)
    

class Race:
    '''Doc for Race
    '''
    def __init__(self, array):
        self.name = array[0].split('-')[0].strip()
        self.distance = array[0].split('-')[1].strip()
        self.date = array[1].strip()
        #these are DNF/DNS and Future races
        if len(array) <= 2:
            if array[0].split('-')[-1].strip() == 'DNS' or  array[0].split('-')[-1].strip() == 'DNF':
                self.status = array[0].split('-')[-1].strip()
                self.distance = array[0].split('-')[-3].strip()
                self.location  = array[0].split('-')[-2].strip()
                #self.weather = ?
            else:
                self.distance = array[0].split('-')[-2].strip()
                self.status = 'Future'
                # these are just odd cases
        elif len(array) < 4:
            self.endtime = array[2]
            self.distance = array[0].split('-')[-2].strip()
            self.location = array[0].split('-')[-1].strip()
            self.status = 'Complete'
            #self.weather = ?
            self.pace = self.get_pace(self.endtime, self.distance)
         #most races completed go into else
        else:
            self.dist = array[0].split('-')[-2].strip()
            self.endtime = array[3]
            self.age = array[4].split(': ')[1]
            self.location = array[0].split('-')[-1].strip()
            self.status = 'Complete'
            self.pace = self.get_pace(self.endtime, self.dist)
    def to_miles(self, Km):
      return round(Km * 0.621371, 2)
    def get_pace(self, dur, dis):
        try:
            dis = dis.upper()
            if re.search(r'\d*:\d*.*$', dur):
                
                hours = int(dur.split(':')[0]) *60  + float((dur.split(':')[1]))
                if re.search(r'.*\d*K.*$', dis):
                    found = re.search('\d*', dis)
                    p = self.to_miles(int(found.group()))
                    result = round(hours / p, 2) # second number for round if for places in decimal
                elif re.search(r'.*\d*.*MILER.*$', dis):
                    found = re.search('\d*', dis)
                    p = int(found.group())
                    result = round(hours / p, 2)
                elif re.search(r'^.*MARATHON.*$', dis):
                    result = round(hours / 26.2, 2)
                elif re.search(r'^.*HALF MARATHON.*$', dis):
                    result = round(hours / 13.1, 2)
              #figure out the hr races too!
         
            else:
                result = 'No Clue'
                return result
        except:
            return 'No Clue'
BASEURL = 'https://ultrasignup.com'
EVENTURL = 'https://ultrasignup.com/register.aspx?did=79789'
#URL = 'https://ultrasignup.com/entrants_event.aspx?did=79789'
URL = 'https://ultrasignup.com/entrants_event.aspx?did=80402'
#start scraping
page = requests.get(URL)
soup = bs(page.text, "html.parser")
racedist = soup.find('span',{'class': 'distances'})
#sometimes there are multiple races per page
if racedist.text.__contains__(","):
    racedist = soup.find('a',{'class': 'event_selected_link'})
ultragrid = soup.findAll('table',{"class":"ultra_grid"})[0]
#Create Headers
head = ultragrid.find('tr')
headers = []
for h in head.find_all('th'):
    if h.text == '':
        headers.append('/')
    else:
        headers.append(h.text.strip())
        headers[-1] = 'Link'
        #Done With Headers
        #Create Runner Rows
runners = []
tr = ultragrid.find_all('tr')
for t in tr:
    runner = []
    runnerurl = []
    for f in t.find_all('td'):
        stats =[]
        if re.match('Results', f.text.strip()):
            for bs in f.find_all('a'):
                runnerurl.append(bs['href'])
                runner.append(bs['href'])
        else:
            runner.append(f.text.strip())
    if len(runner) != 0:
        # this is to get a number to compare with results found against all users with the name given
        expectedfinish = runner[3]
        numofracesfromrace = runner[2]
    if len(runnerurl) != 0:
        # paste ultraparticipant here
        URL = (BASEURL + runnerurl[0])
        opts = Options()
        opts.add_argument('--headless')
        browser = Firefox(options=opts)
        browser.get(URL)
        time.sleep(1)
        acchead = browser.find_elements_by_class_name('accordion-heading')
        accordion = browser.find_elements_by_class_name('accordion-content')
        for num, runner in enumerate(acchead, start=0):
            runarray = runner.text.split('\n')
            run = Runner(runarray, URL, expectedfinish)
            races = accordion[num].find_elements_by_class_name('rowlines')
            print(run.url)
            for r in races:
                racelist = r.text.split('\n')
                obj = Race(racelist)
                run.events.append(vars(obj))
            complete = []
            for e in run.events:
                if e['status'] == 'Complete':
                    complete.append(e)
            print(numofracesfromrace)
            print(len(complete))
            if len(complete) == int(numofracesfromrace):
                print('Match!')
                runners.append(run)
            print(vars(run))
        browser.close()
         # runpage = requests.get(rurl)
         # rsoup = bs(runpage.text, "html.parser") #<= wtf, same prob with selenium or requests - blank array both ways
         # runners.append(runner)
         #done with runners
         #created dataframe
results = []
for r in runners:
    completed = []
    for e in r.events:
        if e['status'] == 'Complete':
            completed.append(e)
    
    #do the work to make the proper table
    rundict = {'predicted pace per mile of current race': Race.get_pace('', r.expectedfinish, racedist.text),# use the fucntions in class?
               'current race distance in miles': racedist.text,
               'current race trail or road': '',# how to find this? scrape page and look for key phrases?
               'gender': r.division,
               'age': r.age,
               'races previously run': len(r.events),
               'months since last race': '', #do some math? count futures
               'last race distance in miles': '',#do some math? ^^
               'difference in last race to current race': '', #do some math?^^^^
               'last race pace per mile': '',# make function work, last non-future
               #'last race elevation gain': '',
               #'last race trail or road': '',
               'ever run farther than distance of current race': '',# parse data and y/n
               'ever run distance of current race': '',# parse data and y/n
               #'temperature last race': '',
    }
    #add r to a new table with cleaned data! dust hands!!!
    
# data = pd.DataFrame(runners)
# data.columns = headers
# data = data.drop(0)

#figure out how to convert total number of entries into a total number of past race
