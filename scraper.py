from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from utils import get_filename_from_cd
BASE_URL = 'https://www.reformagkh.ru/'
page = requests.get('https://www.reformagkh.ru/opendata?gid=2215422&cids=overhaul&pageSize=100')

if page.status_code == 200:
    soup = BeautifulSoup(page.content, 'html.parser')
    divs = soup.find_all('div', class_='opendata')
    for d in divs:
        lia = d.find('li', class_='opendata-action-export').find('a')
        url = urljoin(BASE_URL, lia.get('href'))
        r = requests.get(url, allow_redirects=True)
        print(get_filename_from_cd(r.headers.get('content-disposition')))
        filename = get_filename_from_cd(r.headers.get('content-disposition'))
        open(filename, 'wb').write(r.content)
