from app import request
from bs4 import BeautifulSoup
import re


def scrape_band_page(url):
    html = request.get_raw(url)
    soup = BeautifulSoup(html, 'html.parser')

    band_id = url[url.rindex("/") + 1:]
    band_name = soup.find("h1", {"class": "band_name"}).text
    ret = [band_id, band_name]

    div_band_stats = soup.find("div", {"id": "band_stats"})
    stats_categories = [a.text.strip().replace(":", "").lower() for a in div_band_stats.find_all("dt")]
    stats_values = [re.sub("(\n|\t\s+)", "", a.text.strip()) for a in div_band_stats.find_all("dd")]
    print(stats_categories)
    print(stats_values)

    ret.extend(stats_values)



    return ret


def scrape_album_page(url):
    html = request.get_raw(url)
    soup = BeautifulSoup(html, "html.parser")

    album_id = url[url.rindex("/") + 1:]
    album_name = soup.find("h1", {"class": "album_name"}).text

    st = [album_id, album_name]
    for a in soup.findAll("dl", {"class": ["float_left", "float_right"]}):
        for b in a.findAll("dd"):
            st.append(b.text)

    album_stats = [s.strip() for s in st]
    reviews = album_stats[-1]
    review_count = 0 if reviews == "None yet" else int(reviews[:reviews.index(" ")])
    avg_score = None if reviews == "None yet" else int(reviews[reviews.index(". ") + 2: reviews.index("%")])

    album_stats.extend([review_count,avg_score])
    del album_stats[7]

    return album_stats

