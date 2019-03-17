import pyodbc
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Column, Integer, String

#engine = create_engine("mssql+pyodbc://(localdb)\\MSSQLLocalDB/Metallum?driver=SQL+Server+Native+Client+11.0")


#engine = create_engine("sqlite:///some.db")
#sql = "Create table employee(emp_id integer primary key, emp_name varchar(30))"
#
# engine.execute('insert into employee (emp_name) values(:name)', name="james")
# row = engine.execute("select * from employee").fetchall()

# creates in memory db
engine = create_engine("sqlite://")

class Database:

    def __init__(self):
        cxn_string = 'DRIVER={SQL Server Native Client 11.0;SERVER=(localdb)\\MSSQLLocalDB;DATABASE=Metallum;Trusted_Connection=yes'
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
