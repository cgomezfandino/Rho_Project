import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas_datareader import data as web
import datetime
import requests
from io import StringIO
from pandas.io.common import urlencode
import Google_Conn.Google_Conn as gc
import SQL_Conn.SQL_Conn as sqlconn
from sqlalchemy import create_engine, MetaData, Table, select



# start = datetime.datetime(2000, 1, 1)
# end = datetime.datetime.today()
# sym = 'googl'
# url = gc.build_url(sym, start, end)
#
# data = requests.get(url).text
# df = pd.read_csv(StringIO(data), index_col='Date', parse_dates=True)


ServerName = "LAPTOP-QEUML1IC\SQLEXPRESS01"
Database = "master"
TableName = "mytable"

engine = create_engine('mssql+pyodbc://' + ServerName + '/' + Database)
conn = engine.connect()

# conn = sqlconn.sql_cnxn('master')




