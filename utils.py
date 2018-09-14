
import requests
from bs4 import BeautifulSoup
from datetime import datetime




PROG_URL = 'http://www.alaoula.ma/programmes_inst.php'


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


if __name__ == '__main__':
    """
    resp = requests.get(PROG_URL)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, 'html.parser')
    """
    content = open('soup.bin', 'rb').read()
    soup = BeautifulSoup(content, 'html.parser')
    parseTVPrograms(soup)
    """
    else:
        print("Error: Unable to connect to remote server {}".format(PROG_URL))
    """
