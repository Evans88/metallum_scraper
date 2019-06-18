from sqlalchemy import Column, NVARCHAR, DateTime, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from metallum_scraper import request
from bs4 import BeautifulSoup
import re
import datetime

Base = declarative_base()


class Album(Base):

    def __init__(self, url):
        self.url = url
        self.__get_band_details()

    __tablename__ = 'album'

    album_id =          Column('album_id', NVARCHAR(50), primary_key=True)
    band_id =           Column('band_id', NVARCHAR(50), nullable=False)
    name =              Column('Name', NVARCHAR(150))
    type =              Column('Type', NVARCHAR(50))
    release_date =      Column('Release Date', NVARCHAR(150))
    catalog_id =        Column('Catalog Id', NVARCHAR(35))
    label =             Column('Label', NVARCHAR(150))
    format =            Column('Format', NVARCHAR(150))
    review_count =      Column('Review Count', Integer)
    average_review =    Column('Average Review', Float(2, 2))
    datetime_added =    Column('datetime_added', DateTime)
    datetime_modified = Column('datetime_modified', DateTime)

    def scrape_album_page(band_id, url):
        categories = ['album_id', 'band_id', 'Name', 'Type', 'Release Date', 'Catalog Id', 'Label', 'Format',
                      'Review Count', 'Average Review', 'datetime_added', 'datetime_modified']
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        soup = BeautifulSoup(request.get_raw(url), "html.parser")
        album_id = url[url.rindex("/") + 1:]
        album_name = soup.find("h1", {"class": "album_name"}).text

        st = [album_id, band_id, album_name]

        new_label = []
        new_label_values = []
        for a in soup.findAll("dl", {"class": ["float_left", "float_right"]}):
            # get all labels
            for b in a.findAll(["dd"]):
                new_label_values.append(b.text)
            # get all values
            for c in a.findAll("dt"):
                new_label.append(c.text)

        # combine labels and values
        nn = dict(zip(new_label, new_label_values))
        if 'Version desc.:' in nn.keys():  # This label is rare, dont really need
            del nn['Version desc.:']
        if 'Limitation:' in nn.keys():
            del nn['Limitation:']

        st.extend(nn.values())

        album_stats = [str(s).strip() for s in st]
        reviews = album_stats[-1]

        review_count = None if reviews == "None yet" else int(reviews[:reviews.index(" ")])
        avg_score = None if reviews == "None yet" else int(reviews[reviews.index(". ") + 2: reviews.index("%")])

        album_stats.extend([review_count, avg_score, now, now])
        del album_stats[8]

        return dict(zip(categories, album_stats))

    def __repr__(self):
        return f"<Band({self.data})>"

