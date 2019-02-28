import pyodbc
import datetime
import logging


class Database:

    def __init__(self):
        cxn_string = 'DRIVER={SQL Server Native Client 11.0};SERVER=(localdb)\\MSSQLLocalDB;DATABASE=Metallum;Trusted_Connection=yes'
        cxn = pyodbc.connect(cxn_string)
        self.cursor = cxn.cursor()

    def insert_into_band(self, m, auto_commit=False):
        try:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute(
                f"""
                    INSERT INTO band values(
                          {m.get("id")}
                        ,'{m.get("band name")}'
                        ,'{m.get("country of origin", None)}'
                        ,'{m.get("location", None)}' 
                        ,'{m.get("status", None)}'
                        ,'{m.get("formed in", None)}'
                        ,'{m.get("years active", None)}'
                        ,'{m.get("genre", None)}'
                        ,'{m.get("lyrical themes", None)}'
                        ,'{m.get("current label", None)}'
                        ,'{now}'
                        ,'{now}'
                    )""")
            if auto_commit:
                self.commit()
        except pyodbc.IntegrityError:
            logging.error(f'Table: band - Primary key constraint violation: '.format(m.get("id"), m.get('band_name')))

    def commit(self):
        self.cursor.commit()

