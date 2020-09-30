
"""Do some Stuff
"""
###Start with Sky to Summit
import re
import requests
import pandas as pd
#import csv
from bs4 import BeautifulSoup as bs



#url)
BASEURL = 'https://ultrasignup.com'
URL = 'https://ultrasignup.com/entrants_event.aspx?did=73067#id1695141'
#start scraping
page = requests.get(URL)
soup = bs(page.text, "html.parser")
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
    if len(runnerurl) != 0: 
        rurl = (BASEURL + runnerurl[0])
        runpage = requests.get(rurl)
        rsoup = bs(runpage.text, "html.parser") #<= wtf, same prob with selenium or requests - blank array both ways
        runners.append(runner)
        #done with runners
       #created dataframe
data = pd.DataFrame(runners)
data.columns = headers
data = data.drop(0)
# Junk Columns
# drops = ['/','Age Rank','Bib','Finishes']
# for d in drops:
#     data = data.drop(d,axis=1)
#     # why does age rank look like two columns?

