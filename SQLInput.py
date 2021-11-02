import  pandas as pd
from sqlalchemy import create_engine
import sqlite3

con = sqlite3.connect('db.sqlite3')

engine = create_engine('sqlite:///db.sqlite3')
sqlite_connection = engine.connect()
data = pd.read_csv('Data/PlayerBasics.csv')
sqlite_table = "playerbasics"

cur = con.cursor()
for rows in data.values.tolist():
    cur.execute('INSERT INTO players_playerbasics VALUES(?,?,?,?,?,?,?)', (rows[0], rows[1], rows[2], rows[3], rows[4], rows[5], rows[6]))  # execute执行
con.commit()  # commit提交