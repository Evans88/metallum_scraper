from sqlalchemy import Column, NVARCHAR, DateTime, Integer, Float

from metallum_scraper import request
from bs4 import BeautifulSoup
import json
from urllib import parse
import datetime
from metallum_scraper.orm.Song import Song

from metallum_scraper.orm.Base import base

Base = base


class Albums():

    def __init__(self, band_id, band_name):
        self.band_id = band_id
        self.band_name = band_name
        self.albums = []
        self.__get_album_hrefs()

    def __get_album_hrefs(self):
        base_album_url = "https://www.metal-archives.com/search/ajax-advanced/searching/albums?"
        params = {'exactBandMatch': 1, 'bandName': self.band_name}
        albums_page = request.get_raw(base_album_url + parse.urlencode(params))
        _json = json.loads(albums_page)

        # sometimes exact match doesnt work
        if _json['iTotalRecords'] == 0:
            params = {'bandName': self.band_name}

        albums_page = request.get_raw(base_album_url + parse.urlencode(params))
        print(base_album_url + parse.urlencode(params))

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
        self.songs = []
        self.scrape_album_page(band_id, url)


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

    def scrape_album_page(self, band_id,url):

        now = datetime.datetime.now()

        soup = BeautifulSoup(request.get_raw(url), "html.parser")

        #get album information
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

        self.__get_songs(soup)

    def __get_songs(self, soups):
        for i in soups.findAll("table", {"class": "display table_lyrics"}):
            song_ids, titles, runtime = [], [], []
            for p in i.findAll("tr"):
                titles.append(''.join([mm.text.strip() for mm in p.findAll("td", {"class": "wrapWords"})]))
                runtime.append(''.join(map(str,[mm for mm in p.findAll("td", {"align": "right"})])))
                sids = ''.join(map(str,[a for a in p.findAll("a")]))
                if "name=" in sids:
                    song_ids.append(sids[sids.index("name=") + 6: sids.index(">") - 1])

            runtime = list(filter(lambda x: len(x) > 0, runtime))
            runtime = [i[i.index(">") + 1: -5] for i in runtime]
            titles = list(filter(lambda x: len(x) > 0, titles))

            songs = list(zip(song_ids, titles, runtime))
            for i in songs:
                _s = Song(i[0], i[1], self.album_id, i[2])
                self.songs.append(_s)


    def __repr__(self):
        return "Album (band_id={}, album_id={}, name={})".format(self.band_id, self.album_id, self.name)


if __name__ == "__main__":
    pass
    #ba = Albums('44722','Mgła')
    #a = Albums('97694','Healthy Drain')
