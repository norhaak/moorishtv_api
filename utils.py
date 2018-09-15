
import requests
from bs4 import BeautifulSoup
from datetime import datetime




PROG_URL = 'http://www.alaoula.ma/programmes_inst.php'


def getCurrentDate():
    current_date = datetime.now().date()
    return current_date

def getCurrentTime():
    time_now = (datetime.now()).strftime('%H:%M')
    return time_now

def parseTVPrograms(soup):
    print("Welcome to MoorishTV!\n")


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

    print(prog_titles[25])
    prog_dict = {}
    for i in range(len(prog_times)):
        prog_dict[prog_times[i]] = prog_titles[i]

    for prog_time, prog_title in prog_dict.items():
        print("{} {}".format(prog_time, prog_title))


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

if __name__ == '__main__':
    soup = None
    last_update = None

    if last_update != getCurrentDate():
        last_update = getCurrentDate()
        content = fetchData(PROG_URL)
        open('content.bin', 'wb').write(content)
    else:
        content = open('content.bin', 'rb').read()

    soup = prepareSoup(content)
    
    if soup:
        parseTVPrograms(soup)
    else:
        print("Error: Unable to connect to remote server {}".format(PROG_URL))
