import numpy as np
from scipy import special, optimize
from pylab import plot, show
from Data import *


my_bse=Data("BSE30data.csv")
my_nifty=Data("NIFTYdata.csv")
print percentile(my_bse.pe, 20)
print percentile(my_bse.pe, 15)
print percentile(my_nifty.pe, 20)
print percentile(my_nifty.pe, 15)
my_nifty.regular=0
print 1-percentile(my_bse.dy, 1.1)
print 1-percentile(my_bse.dy, 1.6)
print 1-percentile(my_nifty.dy, 1.1)
print 1-percentile(my_nifty.dy, 1.6)
my_bse.regular=0
"""print my_nifty.DynamicAllocation(1.1, 1.6, 1, 'none')
print my_nifty.CalculateEffectiveReturn()
print my_nifty.DynamicAllocation(1.1, 1.6, 1, 'dy')
print my_nifty.CalculateEffectiveReturn()
print my_nifty.DynamicAllocation(15, 20, 1, 'pe')
print my_nifty.CalculateEffectiveReturn()
"""
#print my_nifty.DynamicAllocationVer2(my_bse, 1)
"""print my_nifty.CalculateEffectiveReturn()
print my_bse.DynamicAllocation(15, 20, 1, 'none')
print my_bse.CalculateEffectiveReturn()
print my_bse.DynamicAllocation(1.1, 1.6, 1, 'dy')
print my_bse.CalculateEffectiveReturn()
print my_bse.DynamicAllocation(15, 20, 1, 'pe')
print my_bse.CalculateEffectiveReturn()
print my_bse.DynamicAllocationVer2(my_nifty, 1)
print my_bse.CalculateEffectiveReturn()
"""
"""
from numpy import arange,array,ones#,random,linalg
from pylab import plot,show
from scipy import stats

xi = arange(0,9)
xi = my_nifty.date
#A = array([ xi, ones(9)])
# linearly generated sequence
y = [ 1, 2,3,4,5,6,7,9, 10]
y = my_nifty.dy
print len(xi)
print len(y)

plot(xi, y, 'ro')
slope, intercept, r_value, p_value, std_err = stats.linregress(xi,y)

print 'r value', r_value
print  'p_value', p_value
print 'standard deviation', std_err

"""
