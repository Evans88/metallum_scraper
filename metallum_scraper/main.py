from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from metallum_scraper.orm.Band import Band
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine('mssql+pyodbc://(localdb)\\MSSQLLocalDB/Metallum?driver=SQL+Server+Native+Client+11.0')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


with open('hrefs.txt') as f:
    files = f.readlines()

s = Session()
for i in range(150):
    band = Band(files[i])

    s.add(band)
    s.commit()