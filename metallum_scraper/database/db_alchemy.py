from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, NVARCHAR, Integer, Float, DateTime

#engine = create_engine("mssql+pyodbc://(localdb)\\MSSQLLocalDB/Metallum?driver=SQL+Server+Native+Client+11.0")
engine = create_engine("sqlite://")
metadata = MetaData()

band = Table('band', metadata
             , Column('id', Integer, primary_key=True)
             , Column('band_id', NVARCHAR(50), nullable=False)
             , Column('Country of Origin', NVARCHAR(75))
             , Column('Location', NVARCHAR(150))
             , Column('Status', NVARCHAR(25))
             , Column('Year Formed', NVARCHAR(10))
             , Column('Genre', NVARCHAR(150))
             , Column('Lyrical Themes', NVARCHAR(150))
             , Column('Current Label', NVARCHAR(150))
             , Column('Years Active', NVARCHAR(200))
             , Column('datetime_added', DateTime)
             , Column('datetime_modified', DateTime)
             )

album = Table('album', metadata
             , Column('id', Integer, primary_key=True)
             , Column('album_id', NVARCHAR(50), nullable=False)
             , Column('band_id', NVARCHAR(50), nullable=False)
             , Column('Name', NVARCHAR(150))
             , Column('Type', NVARCHAR(50))
             , Column('Release Date', NVARCHAR(150))
             , Column('Catalog Id', NVARCHAR(10))
             , Column('Label', NVARCHAR(150))
             , Column('Format', NVARCHAR(150))
             , Column('Review Count', Integer)
             , Column('Average Review', Float(2.2))
             , Column('datetime_added', DateTime)
             , Column('datetime_modified', DateTime)
             )

lkup_band_url = Table('lkup_band_url', metadata,
                    Column('id', Integer, primary_key=True)

                      )

metadata.create_all(engine)


