
import requests
from bs4 import BeautifulSoup
from datetime import datetime


PROG_URL = 'http://www.alaoula.ma/programmes_inst.php?jr=16/09/2018&lang=ar'


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


def getTVPrograms(last_update):
    soup = None
    programs = dict()
    message = ""
    status = 'error'

    if last_update != getCurrentDate():
        content = fetchData(PROG_URL)
        open('content.bin', 'wb').write(content)
    else:
        content = open('content.bin', 'rb').read()

    soup = prepareSoup(content)
    
    if soup:
        programs = parseTVPrograms(soup)
        status = "success"
    else:
        status = "error"
        message = "Error: Unable to connect to remote server {}".format(PROG_URL)
        programs = dict()

    return {'status': status,
            'message': message,
            'programs': programs}
        

if __name__ == '__main__':
    last_update = getCurrentDate()
    print(getTVPrograms(last_update))

    
