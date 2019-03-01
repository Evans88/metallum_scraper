from app import request, Scraper as sb
from database import Database as db
from bs4 import BeautifulSoup
import re
import string
db = db.Database()
for i in string.ascii_uppercase:
    try:
        main_a = f'https://www.metal-archives.com/browse/ajax-letter/l/{i}/json/1'
        html = request.get_raw(main_a).decode("utf-8")
        soup = BeautifulSoup(html, 'html.parser')

        #this should work - response is not valid json, have to parse the string
        txt = re.sub("\s+", "", soup.text)
        max_bands_in_this_letter = int(txt[txt.find(":") + 1 :txt.find(",")])
        print(max_bands_in_this_letter)


    except Exception  as e:\
            print(e)
"""
    for href in soup.findAll("a", href=True):

        # follow href to band page
        band_details = sb.scrape_band_page(href['href'])
        db.insert_into_band(band_details, auto_commit=True)
"""


