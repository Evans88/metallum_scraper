from app import request
from bs4 import BeautifulSoup
import re


def scrape_band_page(url):
    html = request.get_raw(url)
    soup = BeautifulSoup(html, 'html.parser')

    band_id = url[url.rindex("/") + 1:]
    band_name = soup.find("h1", {"class": "band_name"}).text

    div_band_stats = soup.find("div", {"id": "band_stats"})
    stats_categories = [a.text.strip().replace(":", "").lower() for a in div_band_stats.find_all("dt")]
    stats_values = [re.sub("(\n|\t\s+)", "", a.text.strip()) for a in div_band_stats.find_all("dd")]
    ret = dict(zip(stats_categories, stats_values))
    ret['id'] = band_id
    ret['band name'] = band_name

    return ret


def scrape_album_page(url):
    html = request.get_raw(url)
    soup = BeautifulSoup(html, "html.parser")

    album_id = url[url.rindex("/") + 1:]
    album_name = soup.find("h1", {"class": "album_name"}).text

    stats = [album_id, album_name]
    for a in soup.findAll("dl", {"class": ["float_left", "float_right"]}):
        for b in a.findAll("dd"):
            stats.append(b.text)


    stats = [s.strip() for s in stats]
    review_count = 0 if stats[-1] == "None yet" else int(stats[-1][0])
    print(review_count)












url = 'https://www.metal-archives.com/albums/Mg%C5%82a/Exercises_in_Futility/527726'

scrape_album_page(url)
