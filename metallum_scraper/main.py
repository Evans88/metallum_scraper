from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from metallum_scraper.orm.Base import base
from metallum_scraper.orm.Band import Band
from metallum_scraper.orm.Album import Albums



db_url = "sqlite://"
#db_url = "mssql+pyodbc://(localdb)\\MSSQLLocalDB/Metallum?driver=SQL+Server+Native+Client+11.0"

engine = create_engine(db_url)
Base = base

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


with open('hrefs.txt') as f:
    files = f.readlines()

s = Session()

for i in range(10):

    band = Band(files[i])
    print(i, band.name)

    albums = Albums(band.band_id, band.name).albums

    s.add(band)
    for album in albums:
        s.add(album)
        for song in album.songs:
            s.add(song)

    s.commit()

