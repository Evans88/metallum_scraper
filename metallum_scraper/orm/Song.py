
from sqlalchemy import Column, NVARCHAR
from metallum_scraper.orm.Base import base

Base = base

class Song(Base):

    def __init__(self, song_id, name, album_id, length):
        self.song_id = song_id
        self.name = name
        self.album_id = album_id
        self.length = length

    __tablename__ = 'song'
    song_id = Column('song_id', NVARCHAR(50), primary_key=True)
    name = Column('name', NVARCHAR(250))
    album_id = Column('album_id', NVARCHAR(50))
    song_length = Column('length', NVARCHAR(10))

    def __repr__(self):
        return "Song (song_id: {}, name: {}, album_id: {}, length: {})"\
            .format(self.song_id, self.name, self.album_id, self.length)
