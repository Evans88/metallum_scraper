from app import request_html, scrape_band as sb
from database import Database as db
from bs4 import BeautifulSoup
import string


db = db.Database()
for i in string.ascii_uppercase:
    try:
        main_a = f'https://www.metal-archives.com/browse/ajax-letter/l/{i}/json/1'
        html = request_html.get_raw_json(main_a).decode("utf-8")
        soup = BeautifulSoup(html, 'html.parser')

        for i in soup.findAll("a", href=True):

            band_details = sb.scrape_band(i['href'])
            db.insert_into_band(band_details, auto_commit=True)
    except Exception :
        pass

#table_bands = soup.findAll("table", {"class": "display dataTable"})
#print(table_bands)