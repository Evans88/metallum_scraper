from metallum_scraper import request
from bs4 import BeautifulSoup
import re
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Scraper:

    def __init__(self):
        driver_opts = Options()
        driver_opts.add_argument("--headless")
        driver_path = 'C:\\Users\\evansdar\\Code\\Python\\metallum_scraper\\metallum_scraper\\driver\\chromedriver.exe',
        self.driver = webdriver.Chrome(driver_path, chrome_options=driver_opts)


    def scrape_band_page(self, url):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.driver.get(url)

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        band_id = url[url.rindex("/") + 1:]
        band_name = soup.find("h1", {"class": "band_name"}).text
        print(band_name, url)
        ret_band = [band_id, band_name]

        div_band_stats = soup.find("div", {"id": "band_stats"})
        # stats_categories = [a.text.strip().replace(":", "").lower() for a in div_band_stats.find_all("dt")]
        stats_values = [re.sub("(\n|\t\s+)", "", a.text.strip()) for a in div_band_stats.find_all("dd")]

        ret_band.extend(stats_values)
        ret_band.extend([now, now])  # create date, update date

        #discog_table = soup.find("table", {"class": "display discog"})
        # TODO not sure if this list of css classes is exhaustive
        ret_albums = []
        m = soup.findAll("a", {"class": ["other", "album", "single", "demo"]}, href=True)
        print(m)
        for album in m:
            album_details = Scraper.scrape_album_page(self, album['href'], band_id)
            ret_albums.append(album_details)

        return ret_band, ret_albums

    def scrape_album_page(self, url, band_id):

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.driver.get(url)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")

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

        album_stats.extend([review_count, avg_score, now, now])
        del album_stats[7]
        album_stats.insert(1, band_id)

        return album_stats

"""
s = Scraper()
html2 = 'https://www.metal-archives.com/bands/B-612/3540394819'
print(s.scrape_band_page('https://www.metal-archives.com/bands/B-Low/23527'))
"""
