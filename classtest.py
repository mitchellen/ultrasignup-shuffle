import re
class Runner:
    '''Doc
    '''
    def __init__(self, array, url):
        self.array = array
        self.url = url
        races = []
        self.first = array[0].split(' ')[0]
        self.last = array[0].split(' ')[1]
        self.age  = self.just_age(array[0].split(' ')[-1])
        self.total = array[1].split(' ')[0]
        self.sex = self.m_or_f(array[0].split(' ')[-1])
    def m_or_f(self, age):
        return (age[:1])
    def just_age(self, age):
        return (age[1:])
   
       
        

r = Runner(['David Reusch M45', '13 Races', 'Photos', 'Rank: 91.73%', 'Age Rank: 94.85%', 'History', '4 Trophies'], 'www.google.com')
vars(r)
