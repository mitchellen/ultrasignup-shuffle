#import requests
#from bs4 import BeautifulSoup as bs
import pandas as pd
import time
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

# #URL
URL = 'https://ultrasignup.com/results_participant.aspx?fname=William&lname=Connell'
# try chrome if it gets too gross
opts = Options()
opts.add_argument('--headless')
# print(opts)
browser = Firefox(options=opts)
browser.get(URL)
store = browser
panel = browser.find_element_by_class_name('panel') # this looks like garbage
# There is a wwird thing that all race results show up in the same pot despite multiple participants
# How do I sort this out?
gheader = browser.find_elements_by_class_name('groupheader') # racer bio info - each person by the same requested
accordion = browser.find_elements_by_class_name('accordion-content') #<-all races - how do I pin them to the racer? one pot




