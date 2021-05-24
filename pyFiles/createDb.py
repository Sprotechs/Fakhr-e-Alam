import sqlite3
con = sqlite3.connect("kitab.db")
con.execute("""CREATE TABLE IF NOT EXISTS buyers
(ID INTEGER PRIMARY KEY AUTOINCREMENT,
NAME           TEXT    NOT NULL,
ADDRESS           TEXT,
CONTACT           TEXT,
DESCRIPTION           TEXT,
MONTHLY_QIST           REAL    NOT NULL,
INVESTOR_ID           INT    NOT NULL,
COST_PRICE           REAL    NOT NULL,
OTHER_AMOUNT           REAL    NOT NULL,
SALE_PRICE           REAL    NOT NULL,
SHARE           REAL    NOT NULL,
REMAINING_PRICE           REAL    NOT NULL,
NET_PROFIT           REAL    NOT NULL,
TOTAL_PAID           REAL    NOT NULL,
RAFF_WORK           REAL    NOT NULL,
JOIN_DATE           TEXT    NOT NULL);""")


con.execute("""CREATE TABLE IF NOT EXISTS investors
(ID INTEGER PRIMARY KEY AUTOINCREMENT,
NAME text NOT NULL,
contact text,
address text,
join_date text not null);""")


con.execute("""CREATE TABLE IF NOT EXISTS monthly_details
(ID INTEGER PRIMARY KEY AUTOINCREMENT,
buyer_id INT NOT NULL,
investor_id INT NOT NULL,
month text not null,
year text not null,
paid real not null,
cost real not null,
profit real not null);""")

con.execute("""CREATE TABLE IF NOT EXISTS ledger
(ID INTEGER PRIMARY KEY AUTOINCREMENT,
buyer_id INT NOT NULL,
investor_id INT NOT NULL,
description text not null,
datentime text not null,
debit real not null,
credit real not null);""")

con.execute("""CREATE TABLE IF NOT EXISTS investment
(ID INTEGER PRIMARY KEY AUTOINCREMENT,
investor_id INT NOT NULL,
amount real not null,
join_date text not null);""")


con.execute("""CREATE TABLE IF NOT EXISTS profit_paid
(ID INTEGER PRIMARY KEY AUTOINCREMENT,
investor_id INT NOT NULL,
amount real not null,
datentime text not null,
month text not null,
year text not null);""")



# con.execute("""INSERT INTO ledger
# (buyer_id,
# investor_id,
# description,
# datentime,
# debit,
# credit) VALUES(1,3,"MOBILE QIST","NOW",2000.0,0.0);""")
# con.execute("""DELETE FROM ledger WHERE id=1""")
con.commit()
con.close()