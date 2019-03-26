from sqlalchemy import create_engine, MetaData, ForeignKey
from sqlalchemy import Table, Column, NVARCHAR, Integer, Float, DateTime


class Database:

    def __init__(self):
        # engine = create_engine("sqlite://")
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
                     , Column('Years Active', NVARCHAR(200))
                     , Column('datetime_added', DateTime)
                     , Column('datetime_modified', DateTime)
                     )

        album = Table('album', self.metadata
                      , Column('album_id', NVARCHAR(50), primary_key=True)
                      , Column('band_id', NVARCHAR(50), ForeignKey('band.band_id'), nullable=False)
                      , Column('Name', NVARCHAR(150))
                      , Column('Type', NVARCHAR(50))
                      , Column('Release Date', NVARCHAR(150))
                      , Column('Catalog Id', NVARCHAR(10))
                      , Column('Label', NVARCHAR(150))
                      , Column('Format', NVARCHAR(150))
                      , Column('Review Count', Integer)
                      , Column('Average Review', Float(2, 2))
                      , Column('datetime_added', DateTime)
                      , Column('datetime_modified', DateTime)
                      )

        self.metadata.create_all(self.engine)

    def insert_into(self, table_name, list_of_dicts):

        cxn = self.engine.connect()
        table = Table(table_name, self.metadata, autoload=True)

        cxn.execute(
            table.insert(), list_of_dicts

        )




if __name__ == '__main__':
    db2 = Database()
    db2.create_all_tables()
    db2.insert_into("band",
                    [{'band_id': '16265', 'Name': '!T.O.O.H.!', 'Country of Origin': 'Czech Republic',
                      'Location': 'Prague', 'Status': 'Active', 'Year Formed': '1993',
                      'Genre': 'Progressive Death Metal/Grindcore', 'Lyrical Themes': 'Politics, Misanthropy, Gore',
                      'Current Label': 'Unsigned/independent',
                      'Years Active': '1990-1993 (as Devastator), 1993-2005, 2011-2013, 2017-present',
                      'datetime_added': '2019-03-26 09:25:01', 'datetime_modified': '2019-03-26 09:25:01'},
                     {'band_id': '109481', 'Name': '!úl..', 'Country of Origin': 'Czech Republic', 'Location': 'Prague',
                      'Status': 'Split-up', 'Year Formed': '2002', 'Genre': 'Death/Black Metal',
                      'Lyrical Themes': 'Destiny, Emotions, Life', 'Current Label': 'Quatuka Records',
                      'Years Active': '2002-2011', 'datetime_added': '2019-03-26 09:25:02',
                      'datetime_modified': '2019-03-26 09:25:02'},
                     {'band_id': '3540423227', 'Name': '$Greed$', 'Country of Origin': 'United States',
                      'Location': 'Los Angeles, California', 'Status': 'On hold', 'Year Formed': '1999',
                      'Genre': 'Heavy/Thrash Metal', 'Lyrical Themes': 'Political, Humanity',
                      'Current Label': 'Unsigned/independent',
                      'Years Active': '1992-1994 (as Simon Le Greed), 1994-1996 (as Greed), 1999-present',
                      'datetime_added': '2019-03-26 09:25:02', 'datetime_modified': '2019-03-26 09:25:02'},
                     {'band_id': '60323', 'Name': '$ilverdollar', 'Country of Origin': 'Sweden', 'Location': 'Nyköping',
                      'Status': 'Active', 'Year Formed': '1996', 'Genre': 'Heavy/Power Metal',
                      'Lyrical Themes': 'Occult, Fantasy, Human issues', 'Current Label': 'Massacre Records',
                      'Years Active': '1996-present', 'datetime_added': '2019-03-26 09:25:02',
                      'datetime_modified': '2019-03-26 09:25:02'},
                     {'band_id': '3540445218', 'Name': '$lamboy$', 'Country of Origin': 'United States',
                      'Location': 'Cary, Illinois', 'Status': 'Active', 'Year Formed': '2016',
                      'Genre': 'Death Metal/Grindcore (early), Brutal Death Metal (later)',
                      'Lyrical Themes': 'Memes, Nonsense', 'Current Label': 'Unsigned/independent',
                      'Years Active': '2016-2017, 2017-present', 'datetime_added': '2019-03-26 09:25:02',
                      'datetime_modified': '2019-03-26 09:25:02'},
                     {'band_id': '3540438154', 'Name': '$lutrot', 'Country of Origin': 'United States',
                      'Location': 'Nevada / North Carolina / Texas', 'Status': 'Split-up', 'Year Formed': '2013',
                      'Genre': 'Brutal Death Metal', 'Lyrical Themes': 'N/A',
                      'Current Label': 'Pathologically Explicit Recordings', 'Years Active': '2013-2015, 2017-2019',
                      'datetime_added': '2019-03-26 09:25:03', 'datetime_modified': '2019-03-26 09:25:03'},
                     {'band_id': '35843', 'Name': '$uicide $olution', 'Country of Origin': 'Singapore',
                      'Location': 'Tampines', 'Status': 'Active', 'Year Formed': '1998', 'Genre': 'Heavy Metal',
                      'Lyrical Themes': 'Darkness, Death, Horror', 'Current Label': 'Media Corpse',
                      'Years Active': '1998-2006, 2008-present', 'datetime_added': '2019-03-26 09:25:03',
                      'datetime_modified': '2019-03-26 09:25:03'},
                     {'band_id': '67530', 'Name': "'. . . [l]ight am I' . . .", 'Country of Origin': 'Canada',
                      'Location': 'Cartier/Kitchener, Ontario', 'Status': 'Unknown', 'Year Formed': '1996',
                      'Genre': 'Black Metal', 'Lyrical Themes': 'Conquering, Destroying, Possessing, Creating',
                      'Current Label': 'Serpents Head Reprisal', 'Years Active': '1996-?',
                      'datetime_added': '2019-03-26 09:25:03', 'datetime_modified': '2019-03-26 09:25:03'},
                     {'band_id': '3540451613', 'Name': "'Ain", 'Country of Origin': 'Mexico', 'Location': 'Mexico City',
                      'Status': 'Active', 'Year Formed': '2010', 'Genre': 'Symphonic Metal', 'Lyrical Themes': 'N/A',
                      'Current Label': 'Unsigned/independent', 'Years Active': '2010-present',
                      'datetime_added': '2019-03-26 09:25:03', 'datetime_modified': '2019-03-26 09:25:03'},
                     {'band_id': '3540352410', 'Name': "'Big Jim' Shively", 'Country of Origin': 'United States',
                      'Location': 'Nashville, Tennessee', 'Status': 'Active', 'Year Formed': 'N/A',
                      'Genre': 'Doom Metal/Psychedelic Rock', 'Lyrical Themes': 'N/A',
                      'Current Label': 'Unsigned/independent', 'Years Active': 'N/A',
                      'datetime_added': '2019-03-26 09:25:03', 'datetime_modified': '2019-03-26 09:25:03'}]

                    )

"""
    m = MetaData()
    m.reflect(db2.engine)
    for table in m.tables.values():
        print(table.name)
"""
