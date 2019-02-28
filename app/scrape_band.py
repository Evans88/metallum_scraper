from app import request_html
from bs4 import BeautifulSoup
import re


def scrape_band(url):

    html = request_html.get_raw_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    id = url[url.rindex("/") + 1:]

    band_name = soup.find("h1", {"class": "band_name"}).text
    div_band_stats = soup.find("div", {"id": "band_stats"})
    stats_categories = [a.text.strip().replace(":", "").lower() for a in div_band_stats.find_all("dt")]
    stats_values = [re.sub("(\n|\t\s+)", "", a.text.strip()) for a in div_band_stats.find_all("dd")]
    ret = dict(zip(stats_categories, stats_values))
    ret['id'] = id
    ret['band name'] = band_name
    return ret






