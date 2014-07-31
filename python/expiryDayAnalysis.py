import numpy as np
from scipy import special, optimize
from pylab import plot, show
from Data import *



def prevday(day, datearray):
    closest=datearray[0]
    for i in datearray:
        if i  <= day and i - day > closest -day:
            closest = i
    return closest

my_nse= Data("NIFTYdata.csv")
my_nse.CreateFiftyDayPE()
my_bse= Data("BSE30data.csv")
expiryday=[]
cnt=0
my_nse.returnTradingDays()
klist=[]
for m in my_nse.TradingDays:
    pe1=[my_nse.pe[i] for i,j in enumerate(my_nse.date) if j==m] 
    dy1=[my_nse.dy[i] for i,j in enumerate(my_nse.date) if j==m] 
    pe2=[my_bse.pe[i] for i,j in enumerate(my_bse.date) if j==m] 
    dy2=[my_bse.dy[i] for i,j in enumerate(my_bse.date) if j==m] 
    info=GetScore(pe1[0], pe1[0], dy1[0], pe2[0], pe2[0], dy2[0])
    klist.append(info[2])


for j in range(my_nse.date[0].year, my_nse.date[len(my_nse.date)-1].year+1):
    for k in range(1, 13):
        startday=date(j, k, 1)
        for i in range(1,8):
            someday = startday - datetime.timedelta(days=i)
            if someday.weekday()== 3 and someday > my_nse.date[0] and someday < my_nse.date[len(my_nse.date)-1] :
                expiryday.append(prevday(someday, my_nse.date))

prevIndex='NA'
optionTyp='CE'
profit=5000
for m in range(len(expiryday)-1):
    pe=[my_nse.pe[i] for i,j in enumerate(my_nse.date) if j==expiryday[m]] 
    dy=[my_nse.dy[i] for i,j in enumerate(my_nse.date) if j==expiryday[m]] 
    indexValue=[my_nse.nifty[i] for i,j in enumerate(my_nse.date) if j==expiryday[m]]
    kval=klist[expiryday[m].year-1999]
    if kval>0:
        optionTyp='CE'
    else:
        optionTyp='PE'
    if prevIndex != 'NA':
        roundOffIndex=100*int(indexValue[0]/100+0.5)
 #       print expiryday[m], pe[0], indexValue[0], roundOffIndex
	import sqlite3
	conn = sqlite3.connect('NIFTY_FNO.db')
	c= conn.cursor()
	timestamp=expiryday[m]
	expiry=expiryday[m+1]
	selldate=expiryday[m+1]
	c.execute("SELECT * FROM NIFTY WHERE INSTRUMENT='OPTIDX' AND TIMESTAMP=:timestamp AND EXPIRY_DT=:expiry AND STRIKE_PR=:strike AND OPTION_TYP=:optionTyp",{"optionTyp": optionTyp, "strike": roundOffIndex, "timestamp": timestamp, "expiry": expiry})
        row=c.fetchone()	
        c.execute("SELECT * FROM NIFTY WHERE INSTRUMENT='OPTIDX' AND TIMESTAMP=:timestamp AND EXPIRY_DT=:expiry AND STRIKE_PR=:strike AND OPTION_TYP=:optionTyp",{"optionTyp": optionTyp, "strike": roundOffIndex, "timestamp": selldate, "expiry": expiry})
        row2=c.fetchone()
#        print "Buy", row
#        print "Sell", row2
        if row != None:
            number=int(profit/(100*row[8]))
            if number < 1:
                number=1
	    deal=row2[8]-row[8]
	    costPercent=row[8]/indexValue[0]*100
            profit*=1.005
	    if costPercent<100:
	        profit+=number*deal
	    print expiry, indexValue[0], kval, pe[0], dy[0], row[3], row[4], row[8], row2[8], costPercent, deal, number, profit
	conn.close()
    prevIndex=indexValue[0]

