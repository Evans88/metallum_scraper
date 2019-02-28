from app import request_html, scrape_band
from database import Database
from bs4 import BeautifulSoup


db = Database()

main_a = 'https://www.metal-archives.com/browse/ajax-letter/l/B/json/1'
html = request_html.get_raw_json(main_a).decode("utf-8")
soup = BeautifulSoup(html, 'html.parser')

for i in soup.findAll("a", href=True):
    db.insert_into_band(scrape_band(i), auto_commit=True)


#table_bands = soup.findAll("table", {"class": "display dataTable"})
#print(table_bands)