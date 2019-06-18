from sqlalchemy import create_engine, MetaData, select
from sqlalchemy import Table, Column, NVARCHAR, Integer, Float, DateTime


class Database:

    def __init__(self):
        #engine = create_engine("sqlite://")
        db_url = "mssql+pyodbc://(localdb)\\MSSQLLocalDB/Metallum?driver=SQL+Server+Native+Client+11.0"

        self.engine = create_engine(db_url)
        self.metadata = MetaData()


    def create_all_tables(self):

        band = Table('band', self.metadata
                     , Column('band_id', NVARCHAR(50),primary_key=True)
                     , Column('Name', NVARCHAR(150))
                     , Column('Country of Origin', NVARCHAR(75))
                     , Column('Location', NVARCHAR(150))
                     , Column('Status', NVARCHAR(25))
                     , Column('Year Formed', NVARCHAR(10))
                     , Column('Genre', NVARCHAR(150))
                     , Column('Lyrical Themes', NVARCHAR(150))
                     , Column('Current Label', NVARCHAR(150))
                     , Column('Last Label', NVARCHAR(150))
                     , Column('Years Active', NVARCHAR(200))
                     , Column('datetime_added', DateTime)
                     , Column('datetime_modified', DateTime)
                     )

        album = Table('album', self.metadata
                      , Column('album_id', NVARCHAR(50), primary_key=True)
                      , Column('band_id', NVARCHAR(50), nullable=False)
                      , Column('Name', NVARCHAR(150))
                      , Column('Type', NVARCHAR(50))
                      , Column('Release Date', NVARCHAR(150))
                      , Column('Catalog Id', NVARCHAR(35))
                      , Column('Label', NVARCHAR(150))
                      , Column('Format', NVARCHAR(150))
                      , Column('Review Count', Integer)
                      , Column('Average Review', Float(2, 2))
                      , Column('datetime_added', DateTime)
                      , Column('datetime_modified', DateTime)
                      )

        self.metadata.create_all(self.engine)




