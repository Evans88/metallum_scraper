from sqlalchemy import Column, NVARCHAR, DateTime, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from metallum_scraper import request
from bs4 import BeautifulSoup
import json
from urllib import parse
import datetime

Base = declarative_base()


class Albums():

    def __init__(self, band_id, band_name):
        self.band_id = band_id
        self.band_name = band_name
        self.albums = []
        self.__get_album_hrefs()

    def __get_album_hrefs(self):
        base_album_url = "https://www.metal-archives.com/search/ajax-advanced/searching/albums?"
        params = {'exactBandMatch': '1', "bandName": self.band_name}
        albums_page = request.get_raw(base_album_url + parse.urlencode(params))

        _json = json.loads(albums_page)
        raw = [x for x in _json['aaData']]
        ret = list()
        for i in raw:
            b_href = i[0][46:]
            a_href_raw = i[1][9:]
            a_href = a_href_raw[: a_href_raw.index('"')]
            band_id = b_href[b_href.index("/") + 1: b_href.index('"')]

            """
            cannot search by band_id but only band name, so in cases where
            there are more than one band with the same name, have to filter by id post request
            """
            if band_id == self.band_id:
                ret.append([band_id, a_href])

        self.albums += [Album(i[0], i[1])for i in ret]


class Album(Base):

    def __init__(self, band_id, url):
        self.scrape_album_page(band_id,url)

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


    def scrape_album_page(self,band_id,url):

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        soup = BeautifulSoup(request.get_raw(url), "html.parser")


        for i in soup.findAll("table", {"class": "display table_lyrics"}):
            d= [p.text.strip() for p in i.findAll("tr")]
            print(d)





        print("_"*50)

        labels, values = [], []
        for desc in soup.findAll("dl", {"class": ["float_left", "float_right"]}):
            labels += [c.text for c in desc.findAll("dt")]
            values += [b.text for b in desc.findAll("dd")]

        page_raw = dict(zip(labels, values))
        reviews = page_raw["Reviews:"].strip()

        self.album_id = url[url.rindex("/") + 1:]
        self.band_id = band_id
        self.name = soup.find("h1", {"class": "album_name"}).text
        self.type = page_raw.get("Type:", None)
        self.release_date = page_raw.get("Release date:", None)
        self.catalog_id = page_raw.get("Catalog ID:", None)
        self.label = page_raw.get("Label:", None)
        self.format = page_raw.get("Format:", None)
        self.review_count = None if reviews == "None yet" else int(reviews[:reviews.index(" ")])
        self.average_review = None if reviews == "None yet" else int(reviews[reviews.index(". ") + 2: reviews.index("%")])
        self.datetime_added = now
        self.datetime_modified = now

    def get_songs(self):
        pass


    def __repr__(self):
        return "Album (band_id={}, album_id={}, name={})".format(self.band_id, self.album_id, self.name)



if __name__ == "__main__":
    a = Albums('44722','Mgła')