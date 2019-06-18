from sqlalchemy import Column, NVARCHAR, DateTime
from sqlalchemy.ext.declarative import declarative_base
from metallum_scraper import request
from bs4 import BeautifulSoup
import re
import datetime

Base = declarative_base()


class Band(Base):

    def __init__(self, url):
        self.url = url
        self.__get_band_details()

    __tablename__ = 'band'
    band_id =           Column('band_id', NVARCHAR(50), primary_key=True)
    name =              Column('name', NVARCHAR(150))
    country_of_origin = Column('Country of Origin', NVARCHAR(75))
    location =          Column('Location', NVARCHAR(150))
    status =            Column('Status', NVARCHAR(25))
    year_formed =       Column('Year Formed', NVARCHAR(10))
    genre =             Column('Genre', NVARCHAR(150))
    lyrical_themes =    Column('Lyrical Themes', NVARCHAR(150))
    current_label =     Column('Current Label', NVARCHAR(150))
    last_label =        Column('Last Label', NVARCHAR(150))
    years_active =      Column('Years Active', NVARCHAR(200))
    datetime_added =    Column('datetime_added', DateTime)
    datetime_modified = Column('datetime_modified', DateTime)

    def __get_band_details(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        band_page = request.get_raw(self.url)
        soup = BeautifulSoup(band_page, 'html.parser')

        div_band_stats = soup.find("div", {"id": "band_stats"})
        stats_categories = [a.text for a in div_band_stats.find_all("dt")]
        stats_values = [" ".join(a.text.strip().split()) for a in div_band_stats.find_all("dd")]
        page_raw = dict(zip(stats_categories, stats_values))

        self.band_id = re.sub("\n", "", self.url[self.url.rindex("/") + 1:])
        self.name = soup.find("h1", {"class": "band_name"}).text
        self.country_of_origin = page_raw.get('Country of origin:', None)
        self.location = page_raw['Location:']
        self.status = page_raw['Status:']
        self.year_formed = page_raw['Formed in:']
        self.genre = page_raw['Genre:']
        self.lyrical_themes = page_raw['Lyrical themes:']
        self.last_label = page_raw.get('Last label:', None)
        self.current_label = page_raw.get('Current label:', None)
        self.years_active = page_raw['Years active:']
        self.datetime_added = now
        self.datetime_modified = now

        albums = []



    def __repr__(self):
        return f"<Band({self.data})>"

