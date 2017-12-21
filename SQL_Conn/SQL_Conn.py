__author__ = 'cgomezfandino@gmail.com'

import pyodbc
import pandas_datareader.data as web
import datetime
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, select



def sql_cnxn(dataBase):
    conn = pyodbc.connect(
        DRIVER='{ODBC Driver 13 for SQL Server}',
        SERVER='LAPTOP-QEUML1IC\SQLEXPRESS01',
        DATABASE= dataBase,
        Trusted_Connection='yes'
        )
    return(conn)



# conn = sql_cnxn('master')

# cursor = conn.cursor()
#
# sql = "SELECT * FROM [dbo].[spt_monitor] "

# df = pd.read_sql(sql, conn)

# df