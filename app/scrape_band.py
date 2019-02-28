from app import request_html
from bs4 import BeautifulSoup
import re
import logging
import datetime
import pyodbc





url = 'https://www.metal-archives.com/bands/Mg%C5%82a/44722'

html = request_html.get_raw_html(url)
soup = BeautifulSoup(html, 'html.parser')
id = url[url.rindex("/") + 1:]

band_name = soup.find("h1", {"class": "band_name"}).text
div_band_stats = soup.find("div", {"id": "band_stats"})
stats_categories = [a.text.strip().replace(":", "").lower() for a in div_band_stats.find_all("dt")]
stats_values = [re.sub("(\n|\t\s+)", "", a.text.strip()) for a in div_band_stats.find_all("dd")]
m = dict(zip(stats_categories, stats_values))


cxn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=(localdb)\\MSSQLLocalDB;DATABASE=Metallum;Trusted_Connection=yes')
cursor = cxn.cursor()


try:
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
    f"""
       INSERT INTO band values(
          {id}
        ,'{band_name}'
        ,'{m.get("country of origin", None)}'
        ,'{m.get("location2", None)}'
        ,'{m.get("status", None)}'
        ,'{m.get("formed in", None)}'
        ,'{m.get("years active", None)}'
        ,'{m.get("genre", None)}'
        ,'{m.get("lyrical themes", None)}'
        ,'{m.get("current label", None)}'
        ,'{now}'
        ,'{now}'
       )""")
except pyodbc.IntegrityError:
    logging.error(f"Table: band - Primary key constraint violation: {id}, {band_name}")

cursor.commit()
