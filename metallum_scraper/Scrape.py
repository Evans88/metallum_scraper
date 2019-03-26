import datetime
from bs4 import BeautifulSoup
from metallum_scraper import request
from metallum_scraper.database import Database as db
import re
import time
import json


def get_band_hrefs():
    base_url = 'https://www.metal-archives.com/search/ajax-advanced/searching/bands?iDisplayStart='
    response = request.get_raw(base_url)
    band_count = json.loads(response)['iTotalRecords']
    hrefs = []
    for page in range(0, band_count, 200):  # 200 bands / page

        url = base_url + str(page)
        response = request.get_raw(url)
        _json = json.loads(response)
        raw = [a[0] for a in _json['aaData']]

        hrefs.extend([b[9:b.index("\">")] for b in raw])

        print(len(hrefs))

        time.sleep(1)
    return hrefs


def get_band_details(url):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    categories = ['band_id', 'Name', 'Country of Origin', 'Location', 'Status', 'Year Formed', 'Genre', 'Lyrical Themes',
                  'Current Label', 'Years Active', 'datetime_added', 'datetime_modified']
    band_page = request.get_raw(url)

    soup = BeautifulSoup(band_page, 'html.parser')

    band_id = re.sub("\n", "", url[url.rindex("/") + 1:])
    band_name = soup.find("h1", {"class": "band_name"}).text
    ret_band = [band_id, band_name]

    div_band_stats = soup.find("div", {"id": "band_stats"})

    stats_values = [" ".join(a.text.strip().split()) for a in div_band_stats.find_all("dd")]
    ret_band.extend(stats_values)
    ret_band.extend([now, now])  # create date, update date

    r_dict = dict(zip(categories, ret_band))

    return r_dict


with open("hrefs.txt", "r") as f:
    lines = f.readlines()
    ll = []
    for t in range(10):
        ll.append(get_band_details(lines[t]))
print(ll)
db1 = db.Database()
db1.create_all_tables()
db1.insert_into('band',ll)

