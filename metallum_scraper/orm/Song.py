
from sqlalchemy import Column, NVARCHAR, DateTime, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from metallum_scraper import request
from bs4 import BeautifulSoup
import json
from urllib import parse
import datetime

Base = declarative_base()

class Song(Base):

    def __init__(self):
        pass

    __tablename__ = 'song'
    song_id = Column('song_id', NVARCHAR(50), primary_key=True)
    album_id = Column('album_id', NVARCHAR(50))
    song_length = Column('length', NVARCHAR(10))

