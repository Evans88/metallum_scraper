import pyodbc


class Database:

    def __init__(self):
        cxn_string = 'DRIVER={SQL Server Native Client 11.0};SERVER=(localdb)\\MSSQLLocalDB;DATABASE=Metallum;Trusted_Connection=yes;'
        cxn = pyodbc.connect(cxn_string)
        self.cursor = cxn.cursor()

    def insert_into(self, table_name, values, auto_commit=False):
        try:
            sql = f"INSERT INTO {table_name} values(?,?,?,?,?,?,?,?,?,?,?,?)"
            self.cursor.execute(sql, values)
            if auto_commit:
                self.commit()
        except pyodbc.IntegrityError:
            # TODO format this right
            pass#logging.error(f'Table: {table_name} - Primary key constraint violation: {m.get("id")},{m.get("band name")}')

    def commit(self):
        self.cursor.commit()


db = Database()