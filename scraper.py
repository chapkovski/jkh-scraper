from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from utils import get_filename_from_cd
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
BASE_URL = 'https://www.reformagkh.ru/'


def get_url(i=1):
    """We glue together relative urls and host name plus page number"""
    REL_ENTRY_POINT = f'opendata?gid=2208161&cids=overhaul&pageSize=10&page={i}'
    ABS_ENTRY_POINT = urljoin(BASE_URL, REL_ENTRY_POINT)
    return ABS_ENTRY_POINT


# define num pages to loop through
page = requests.get(get_url())
soup = BeautifulSoup(page.content, 'html.parser')
# get the footer paginator and retrieve page number for the last page to know how to loop
paginator = soup.select('ul.pagination.fl')[0].select('li.last')[0].select('a')[0]
last_page = int(paginator.attrs['data-page'])
for i in range(1, last_page + 1):
    logger.info(f'getting page {i} out of {last_page}')
    page = requests.get(get_url(i))

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        divs = soup.find_all('div', class_='opendata')
        # get all divs with data there, get the url to download, get the file name from the header, save it
        for d in divs:
            lia = d.find('li', class_='opendata-action-export').find('a')
            url = urljoin(BASE_URL, lia.get('href'))
            r = requests.get(url, allow_redirects=True)
            filename = get_filename_from_cd(r.headers.get('content-disposition'))
            logger.info(f'downloading file {filename}...')
            open(f'data/{filename}', 'wb').write(r.content)
