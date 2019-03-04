from app import request, Scraper as sb
from database import Database as db
from bs4 import BeautifulSoup
import re
import string
db = db.Database()
# for i in string.ascii_uppercase:

main_a = f'https://www.metal-archives.com/browse/ajax-letter/l/A/json/1'
html = request.get_raw(main_a).decode("utf-8")
soup = BeautifulSoup(html, 'html.parser')

# this should work - response is not valid json, have to parse as string
txt = re.sub("\s+", "", soup.text)
max_bands_in_this_letter = int(txt[txt.find(":") + 1 :txt.find(",")])

for display_start in range(0, max_bands_in_this_letter, 500):

    main_a = f'https://www.metal-archives.com/browse/ajax-letter/l/A/json/1?DisplayStart={display_start}'
    html = request.get_raw(main_a).decode("utf-8")
    soup = BeautifulSoup(html, 'html.parser')
    for href in soup.findAll("a", href=True):

        # follow href to band page
        band_details = sb.scrape_band_page(href['href'])
        db.insert_into_band(band_details, auto_commit=True)




