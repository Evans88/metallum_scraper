
import datetime
from bs4 import BeautifulSoup
from metallum_scraper import request
import re


class Scraper:

    def get_band_details(self,url):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        categories = ['band_id', 'Name', 'Country of Origin', 'Location', 'Status', 'Year Formed', 'Genre',
                      'Lyrical Themes',
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