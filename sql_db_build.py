"""
This file creates the database, and you run it only once.
"""

import pymysql.cursors
import mysql.connector
import configuration as cfg

# Create database
con = mysql.connector.connect(host=cfg.CONNECT_DB_HOST,
                              user=cfg.CONNECT_DB_USER,
                              password='Ab123456')

cur = con.cursor()
cur.execute(cfg.SQL_CREATE_DB)

# Create tables
con = pymysql.connect(host=cfg.CONNECT_DB_HOST,
                      user=cfg.CONNECT_DB_USER,
                      password='Ab123456',
                      db=cfg.CONNECT_DB_DB,
                      charset=cfg.CONNECT_DB_CHARSET,
                      cursorclass=pymysql.cursors.DictCursor)

cur = con.cursor()
with cur:
    cur = con.cursor()
    cur.execute(cfg.SQL_TABLE_PRODUCTS)
    cur.execute(cfg.SQL_TABLE_DRESSES)
    cur.execute(cfg.SQL_TABLE_T_SHIRTS)
    cur.execute(cfg.SQL_TABLE_SWIMWEAR)
    cur.execute(cfg.SQL_TABLE_COMMON_DESC)
