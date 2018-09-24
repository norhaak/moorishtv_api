
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from database import db_session
from models import Program


PROG_URL = 'http://www.alaoula.ma/programmes_inst.php?jr={}&lang=fr'

def insert_program(program):
    db_session.add(program)
    db_session.commit()


def insert_programs(programs):
    db_session.beginTransaction();
    for program in programs:
        db_session.add(program);
    db_session.setTransactionSuccessful();
    db_session.endTransaction();


def save_programs(date, programs):
    for item in programs:
        program = Program(date, item['time'], item['title'])
        insert_program(program)
    db_session.commit()


def get_programs_by_date(date):
    programs = Program.query.filter(Program.date == date).all()
    return programs


def getNext7Dates():
    currentDate = getCurrentDate()
    dates = []
    for i in range(1,8):
        nextDate = currentDate + timedelta(days=i)
        dates.append(formatDate(nextDate))
    return dates

def getLast7Dates():
    currentDate = getCurrentDate()
    dates = []
    for i in range(1,8):
        nextDate = currentDate - timedelta(days=i)
        dates.append(formatDate(nextDate))
    return dates


def updateDB():
    dates = getNext7Dates()
    for date in dates:
        print('fetching date for {} tv programs...'.format(date))
        content = fetchData(PROG_URL.format(date))
        soup = prepareSoup(content)
        programs = parseTVPrograms(soup)
        print('saving tv programs into db...')
        save_programs(date, programs)
        

def cleanDB(date):
    programs = get_programs_by_date(date)
    for program in programs:
        db_session.delete(program)
    db_session.commit()


def convertStr2Date(date_str):
    date_ = datetime.strptime(date_str, '%d-%m-%y').date()
    return date_.strftime('%d/%m/%Y')

def formatDate(_date):
    return _date.strftime('%d/%m/%Y')

def getCurrentDate():
    current_date = datetime.now().date()
    return current_date


def getCurrentTime():
    time_now = (datetime.now()).strftime('%H:%M')
    return time_now


def fetchMissingTitle(soup, idx):
    title = soup.findAll('div', class_='grille_mid_holder2')[idx].a.text
    return title


def parseTVPrograms(soup):
    prog_time_list = soup.findAll('div', class_='grille_time_off')
    prog_times = []
    for prog_item in prog_time_list:
        prog_time = prog_item.text
        if prog_time == 'Actuellement':
            prog_time = getCurrentTime()
        prog_times.append(prog_time)

    prog_title_list = soup.findAll('div', class_='grille_mid_holder')
    prog_titles = []
    for prog_item in prog_title_list:
        prog_title = prog_item.a.text
        prog_titles.append(prog_title)

    idx = 0
    for i in range(len(prog_titles)):
        if prog_titles[i] == '\n\n':
            prog_titles[i] = fetchMissingTitle(soup, idx)
            idx += 1

    prog_list = []
    for i in range(len(prog_times)):
        program = {
            'time': prog_times[i],
            'title': prog_titles[i]
        }
        prog_list.append(program)

    """
    for prog_time, prog_title in prog_dict.items():
        print("{} {}".format(prog_time, prog_title))
    """

    return prog_list


def fetchData(prog_url):
    content = None
    try:
        resp = requests.get(prog_url)
        if resp.status_code == 200:
            content = resp.content
    except:
        content = open('content.bin', 'rb').read()
    return content


def prepareSoup(content):
    soup = None
    if content:
        soup = BeautifulSoup(content, 'html.parser')
    return soup


def getTVPrograms(date):
    programs = dict()
    message = ""
    status = 'success'

    programs = get_programs_by_date(date)
    programsJson = []
    for program in programs:
        programsJson.append(program.as_json())
    
    return {'status': status,
            'message': message,
            'programs': programsJson}
        

if __name__ == '__main__':
    #updateDB()
    last_days = getLast7Dates()
    for date in last_days:
        cleanDB(date)

    #currentDate = getCurrentDate()
    #print(getTVPrograms(currentDate))

    
