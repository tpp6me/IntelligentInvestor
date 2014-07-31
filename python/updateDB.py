import sqlite3
from datetime import date
conn = sqlite3.connect('NIFTY_FNO.db')

def convertodate(stri):
    stri=stri.lower()
    info=stri.split("-")
    option = { 'jan' : 1, 'feb': 2, 'mar':3 , 'apr': 4, 'may': 5, 'jun': 6, 'jul':7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec':12}
    fin = date(int(info[2]), int(option[info[1]]), int(info[0]))
    return(fin)


filename="csvfilelist"
with open(filename, "r") as f:
    for line in f:
        info = [x.strip() for x in line.split(" ") if x!='\n']
        print "Analysing file", info[0]
        with open(info[0],"r") as fp:
            for line1 in fp:
                 info1 = [x for x in line1.split(",") if x!='\n']
                 if info1[0]=='OPTIDX' and info1[1]=='NIFTY' and info1[10]!='0':
                     info1[2]=convertodate(info1[2])
                     info1[14]=convertodate(info1[14])
#                     print info1
                     conn.execute("INSERT INTO NIFTY VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", info1)
                     conn.commit()

conn.close()

