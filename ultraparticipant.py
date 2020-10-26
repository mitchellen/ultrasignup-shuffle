import re
import csv
import time
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
class Runner:
   '''Doc
    '''
   def __init__(self, array, url):
      #age,number of races, url
      self.url = url
      self.first = array[0].split(' ')[0]
      self.last = array[0].split(' ')[1]
      self.age  = self.just_age(array[0].split(' ')[-1])
      self.total = array[1].split(' ')[0]
      self.divsion = self.m_or_f(array[0].split(' ')[-1])
      self.events = []
   def m_or_f(self, age):
       return (age[:1])
   def just_age(self, age):
       return (age[1:])

class Race:
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
      #most races completed go here
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
with open('out.txt', mode ='r')as file:
   time.sleep(5)
   output = csv.reader(file)
   notlist = []
   for l in output: #load entire csv into vari to get better data and num properties
      notlist.append(l)
   for u in notlist:
      #URL = 'https://ultrasignup.com/results_participant.aspx?fname=Cera&lname=Jones'
      #URL = 'https://ultrasignup.com/results_participant.aspx?fname=William&lname=Connell'
      URL = 'https://ultrasignup.com' + u[0]
      opts = Options()
      opts.add_argument('--headless')
      browser = Firefox(options=opts)
      browser.get(URL)
      time.sleep(1)
      runners = []
      acchead = browser.find_elements_by_class_name('accordion-heading')
      accordion = browser.find_elements_by_class_name('accordion-content')
      for num, runner in enumerate(acchead, start=0):
         runarray = runner.text.split('\n')
         run = Runner(runarray, URL)
         races = accordion[num].find_elements_by_class_name('rowlines')
         print(run.url)
         for r in races:
            racelist = r.text.split('\n')
            obj = Race(racelist)
            run.events.append(vars(obj))
            #print(vars(obj)) # this is debug/crutch
         print(vars(run))
      browser.close()
         #find out why pace is fucked
