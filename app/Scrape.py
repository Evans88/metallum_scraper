from app import request_html
from bs4 import BeautifulSoup
url = 'https://www.metal-archives.com/bands/Wormwitch'

html = request_html.get_raw_html(url)

soup = BeautifulSoup(html, 'html.parser')

name = soup.find("h1", {"class": "band_name"}).text

band_stats = soup.find("div", {"id": "band_stats"})

