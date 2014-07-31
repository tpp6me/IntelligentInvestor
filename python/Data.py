from datetime import date
import datetime
import re

def GetScore(pe1, pe5d1, dy1, pe2, pe5d2, dy2):
    InvestmentGrade=[]
    
        
    if pe1<15 and pe1!='NA':
        InvestmentGrade.append(1)
    elif pe1>20 and pe1!='NA':
        InvestmentGrade.append(-1)
    elif pe1<20 and pe1!='NA':
        InvestmentGrade.append(0)
    if dy1<1.11 and dy1!='NA':
        InvestmentGrade.append(-1)
    elif dy1>1.6 and dy1!='NA':
        InvestmentGrade.append(1)
    elif dy1<1.6 and dy1!='NA':
        InvestmentGrade.append(0)

    if pe2<15 and pe2!='NA':
        InvestmentGrade.append(1)
    elif pe2>20 and pe2!='NA':
        InvestmentGrade.append(-1)
    elif pe2<20 and pe2!='NA':
        InvestmentGrade.append(0)

    if dy2<1.11 and dy2!='NA':
        InvestmentGrade.append(-1)
    elif dy2>1.6 and dy2!='NA':
        InvestmentGrade.append(1)
    elif dy2<1.6 and dy2!='NA':
        InvestmentGrade.append(0)
    av=sum(InvestmentGrade, 0.0)/len(InvestmentGrade)
    k=0.9
    if av>0.25:
        k=1
    elif av>-0.1:
        k=0.7
    elif av>-0.51:
        k=0.3
    elif av<-0.51:
        k=0
    return InvestmentGrade, av, k
        
def percentile(array, numb):
    sum=0
    for i in array:
        if i < numb:
            sum=sum+1
    return float(sum)/float(len(array))

class Data(object):
    def __init__(self, filename):
        self.DefaultEquityRatio=0.7
        count=0
        self.date=[]
        self.pe=[]
        self.pb=[]
        self.dy=[]
        self.nifty=[]
        self.earnings=[]
        self.dividend=[]
        self.investment=[]
        self.interest=8
        self.regular=1
        self.tradingFrequency=1
        with open(filename, "r") as f:       
            for line in f:
                if re.search(r"[a-z]", line)==None:
                    info = [x for x in line.split(",") ]
                    d1= [int(y) for y in info[1].split("/")]                   
                    self.date.append(date(d1[2], d1[0], d1[1]))
                    self.pe.append(float(info[2]))
                    self.pb.append(float(info[3]))
                    self.dy.append(float(info[4]))
                    self.nifty.append(float(info[5]))
                    self.earnings.append(float(info[5])/float(info[2]))
                    self.dividend.append(float(info[4])*float(info[5]))
                    count=count+1
        f.close()

# 50d translates to 35 trading days
    def CreateFiftyDayPE(self):
        self.FiftyDayPE=[]
        self.FiftyDayPE= ['NA' for m in range(1, 35)]
        for i in range(34, len(self.date)):
            list1=[]
            list1 = [self.pe[m] for m in range(i-34,i)]          
            self.FiftyDayPE.append(sum(list1)/34)

# 50d translates to 35 trading days
    def CreateFiftyDayDY(self):
        self.FiftyDayDY=[]
        self.FiftyDayDY= ['NA' for m in range(1, 35)]
        for i in range(34, len(self.date)):
            list1=[]
            list1 = [self.dy[m] for m in range(i-34,i)]          
            self.FiftyDayDY.append(sum(list1)/34)

# Method identify date for max nifty or pe etc
    def returndateformax(self, array):
        maxa=max(array)
        maxi=[self.date[i] for i,j in enumerate(array) if j==maxa]
        print maxi[0], maxa
        return maxi[0]

# Method to identify date with min pe, nifty etc
    def returndateformin(self, array):
        mina=min(array)
        mini=[self.date[i] for i,j in enumerate(array) if j==mina]
        print mini[0], mina
        return mini[0]

# Identify closest trading day to some date    
    def takeClosest(self, d1):
        closest = self.date[0]
        for i in self.date:
            if abs(closest - d1) > abs(i-d1):
                closest=i
        return closest

#List of days closest to new years    
    def returnTradingDays(self):
        minyear=min(self.date)
        maxyear=max(self.date)
        self.TradingDays=[]
        from datetime import timedelta
        for j in range(minyear.year, maxyear.year+1):
            start=date(j, 1, 1)
            self.TradingDays.append(self.takeClosest(start))

            for i in range(self.tradingFrequency-1):
                start+=datetime.timedelta(days=365.25/self.tradingFrequency)
                self.TradingDays.append(self.takeClosest(start))
        
#        self.TradingDays=[self.takeClosest(date(i, 1, 1)) for i in range(minyear.year, maxyear.year+1)]
        return self.TradingDays
        
    
        
    def equityratio50dpe(self, pe, lower, upper, indx):
#        print "indicator", indx, pe, lower, upper
        if pe=='NA':
            return 1
        elif indx=='pe' and pe < lower:
            return 1
        elif indx=='pe' and pe > upper:
            return 0
        elif indx=='dy' and pe < lower:
            return 0
        elif indx=='dy' and pe > upper:
            return 1
        else:
            return self.DefaultEquityRatio

    def std_dev(self, array):
        mean = sum(array,0.0) / len(array)
        d= [(i-mean)**2 for i in array]
        stddev= (sum(d)**(0.5))/len(array)
        self.avreturn=mean
        self.stddevreturn=stddev
    

    def DynamicAllocation(self, lower, upper, frequency, indx):
        capital=1
        self.tradingFrequency=frequency #Number of times in a year
        self.FixedIncome=[]
        self.Equity=[]
        self.Net=[]
        self.returnTradingDays()
        self.CreateFiftyDayPE()
        self.CreateFiftyDayDY()
        self.AnnualReturn=[]
        prevDate=self.TradingDays[0]
        count=0
        kprev=self.DefaultEquityRatio
        tax=0
        for m in self.TradingDays:
            pe=[self.FiftyDayPE[i] for i,j in enumerate(self.date) if j==m]
            if indx=='dy':
                pe=[self.dy[i] for i,j in enumerate(self.date) if j==m]                
            nifty=[self.nifty[i] for i,j in enumerate(self.date) if j==m]
            prevnifty=[self.nifty[i] for i,j in enumerate(self.date) if j==prevDate]
            divy=[self.dy[i] for i,j in enumerate(self.date) if j==prevDate]
            k=self.equityratio50dpe(pe[0], lower, upper, indx )
            if (indx == 'none'):
                k=1
#            if k==self.DefaultEquityRatio and kprev > k:
#                k=kprev
            kprev=k    
            delta=m-prevDate
            if str(delta)== '0:00:00':
                self.Equity.append(capital*k)
                self.FixedIncome.append(capital*(1-k))
                self.Net.append(capital)
                equity=capital*k
                fixedincome=capital*(1-k)
                self.AnnualReturn.append('NA')
                divi=0
                self.investment.append(capital)
            else:
                equity=self.Equity[count-1]*float(nifty[0])/float(prevnifty[0])
                divi=self.Equity[count-1]*(1+divy[0]/100)**float(float(delta.days)/365)-self.Equity[count-1]
                fixedincome=self.FixedIncome[count-1]*(1+self.interest*0.01)**float(float(delta.days)/365)
                tot=equity+fixedincome+divi+self.regular
                self.Net.append(tot)
                self.Equity.append((tot)*k)
                self.FixedIncome.append(tot*(1-k))
                self.AnnualReturn.append(100*(self.Net[count]/self.Net[count-1]-1))
                tax=0
                self.investment.append(self.regular)
                
                    
                
#            print m, prevDate, nifty[0], prevnifty[0], pe[0], divy[0], k, equity, fixedincome, divi, self.Net[count], self.Equity[count], self.FixedIncome[count], self.AnnualReturn[count], tax               
            
            prevDate=m
            count=count+1
        delta=self.TradingDays[count-1]-self.TradingDays[0]
        self.returns=((self.Net[count-1]/self.Net[0])**(1/(float(delta.days)/365.25)) -1 )*100 
        self.stddev=self.std_dev(self.AnnualReturn[1::])
        return [self.returns, self.avreturn, self.stddevreturn]

    def CalculateEffectiveReturn(self):
        r1=1
        r2=20
        error=100
        while error>0.005:
            inc1=0
            inc2=0
            for i in range(len(self.TradingDays)):
                delta=self.TradingDays[len(self.TradingDays)-1]-self.TradingDays[i]
                inc1+=self.investment[i]*((1+r1*0.01)**((float(delta.days))/365.25))
                inc2+=self.investment[i]*(1+r2*0.01)**(float(delta.days)/365.25)
 #               print self.TradingDays[i], self.investment[i], self.Net[i], delta.days/365.25, inc1, inc2
            r0=r1+(self.Net[len(self.TradingDays)-1]-inc1)*(r2-r1)/(inc2-inc1)
            error=abs(1-r0/r1)
#            print inc1, inc2, r0, r1, r2, error, (self.Net[len(self.TradingDays)-1])
#            break
            if abs(r2-r0) > abs(r1-r0):
                r2=r0
            else:
                r1=r0
        return(r0)

        
            

    def DynamicAllocationVer2(self, DataObject2, frequency):
        capital=1
        self.tradingFrequency=frequency #Number of times in a year
        self.FixedIncome=[]
        self.Equity=[]
        self.Net=[]
        self.returnTradingDays()
        self.CreateFiftyDayPE()
        DataObject2.CreateFiftyDayPE()
        self.AnnualReturn=[]
        prevDate=self.TradingDays[0]
        count=0
        kprev=self.DefaultEquityRatio
        tax=0
        for m in self.TradingDays:
            pe1=[self.pe[i] for i,j in enumerate(self.date) if j==m]
            pe50d1=[self.FiftyDayPE[i] for i,j in enumerate(self.date) if j==m]
            dy1=[self.dy[i] for i,j in enumerate(self.date) if j==m]
            pe2=[DataObject2.pe[i] for i,j in enumerate(DataObject2.date) if j==m]
            pe50d2=[DataObject2.FiftyDayPE[i] for i,j in enumerate(DataObject2.date) if j==m]
            dy2=[DataObject2.dy[i] for i,j in enumerate(DataObject2.date) if j==m]
            if len(pe2)==0:
                pe2.append('NA')
            if len(pe50d2)==0:
                pe50d2.append('NA')
            if len(dy2)==0:
                dy2.append('NA')
                
            nifty=[self.nifty[i] for i,j in enumerate(self.date) if j==m]
            prevnifty=[self.nifty[i] for i,j in enumerate(self.date) if j==prevDate]
            divy=[self.dy[i] for i,j in enumerate(self.date) if j==prevDate]
            klist=GetScore(pe1[0], pe50d1[0], dy1[0], pe2[0], pe50d2[0], dy2[0])
            k=klist[2]
#            if k==self.DefaultEquityRatio and kprev > k:
#                k=kprev
            kprev=k    
            delta=m-prevDate
            if str(delta)== '0:00:00':
                self.Equity.append(capital*k)
                self.FixedIncome.append(capital*(1-k))
                self.Net.append(capital)
                equity=capital*k
                fixedincome=capital*(1-k)
                self.AnnualReturn.append('NA')
                divi=0
                self.investment.append(capital)
            else:
                equity=self.Equity[count-1]*float(nifty[0])/float(prevnifty[0])
                divi=self.Equity[count-1]*(1+divy[0]/100)**float(float(delta.days)/365)-self.Equity[count-1]
                fixedincome=self.FixedIncome[count-1]*(1+self.interest*0.01)**float(float(delta.days)/365)
                tot=equity+fixedincome+divi+self.regular
                self.Net.append(tot)
                self.Equity.append((tot)*k)
                self.FixedIncome.append((tot)*(1-k))
                self.AnnualReturn.append(float(100*(self.Net[count]/self.Net[count-1]-1)))
                tax=0
          #      print '%s\t%s\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.1f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f' \
          #        %(str(m), str(prevDate), nifty[0], prevnifty[0], dy1[0], pe1[0], dy2[0], pe2[0], k, equity, fixedincome, divi, self.Net[count], self.Equity[count], self.FixedIncome[count], self.AnnualReturn[count])         
            prevDate=m
            count=count+1
        delta=self.TradingDays[count-1]-self.TradingDays[0]
        self.returns=((self.Net[count-1]/self.Net[0])**(1/(float(delta.days)/365.25)) -1 )*100 
        self.stddev=self.std_dev(self.AnnualReturn[1::])
        return [self.returns, self.avreturn, self.stddevreturn]
