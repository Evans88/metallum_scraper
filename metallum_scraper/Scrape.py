import datetime
from bs4 import BeautifulSoup
from metallum_scraper import request
import re, time, json
from urllib import parse
from metallum_scraper.database import Database as db

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

        time.sleep(1)
    return hrefs



def get_album_hrefs(band_name):
    base_album_url = "https://www.metal-archives.com/search/ajax-advanced/searching/albums?"
    params = {'exactBandMatch': '1', "bandName": band_name}
    albums_page = request.get_raw(base_album_url + parse.urlencode(params))
    _json = json.loads(albums_page)
    raw = [a for a in _json['aaData']]


    ret = list()
    for i in raw:
        b_href = i[0][46:]
        a_href_raw = i[1][9:]

        a_href = a_href_raw[: a_href_raw.index('"')]
        print(a_href)
        band_id = b_href[b_href.index("/") + 1: b_href.index('"')]

        #ret.append(scrape_album_page(band_id, a_href))
    print(ret)
    return ret






if __name__ == "__main__":

    get_album_hrefs("Batushka")

    # with open("hrefs.txt", "r") as f:
    #     lines = f.readlines()
    #     ll = []
    #     for t in range(1):
    #         ll.append(get_band_details(lines[t]))



