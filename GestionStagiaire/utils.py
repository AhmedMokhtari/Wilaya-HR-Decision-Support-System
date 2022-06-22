from datetime import datetime,timedelta

def datestage(date,nbmois):
    date1 = datetime.fromisoformat(date)
    return date1 + timedelta(int(nbmois)*30)

def divabbr(divname):
    abbr = ''
    for char in divname:
        if char.isupper():
            abbr = abbr+char
    return abbr