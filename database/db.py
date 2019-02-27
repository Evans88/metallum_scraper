import pyodbc

cxn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=(localdb)\\MSSQLLocalDB;DATABASE=Metallum;Trusted_Connection=yes')
cursor = cxn.cursor()


