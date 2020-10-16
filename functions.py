'''Functions
'''
def to_miles(Km):
    
    '''convert to miles. Should I be converting to metric?!
    '''
    return round(Km * 0.621371, 2)
def get_pace(dur, dis):
    '''Get the time per mile pace
    '''
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
