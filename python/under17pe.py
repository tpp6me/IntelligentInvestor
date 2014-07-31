
from Data import *
from PlotDynamicAllocation import *
from pygraph import *

my_nifty=Data("../python/NIFTYdata.csv");
my_bse=Data("../python/BSE30data.csv");
my_bank=Data("../python/BANKNIFTYdata.csv")
my_finance=Data("../python/CNXFINANCEdata.csv")
my_nifty.createEarningsArray()
my_nifty.createDividendArray()
my_bse.createEarningsArray()
my_bse.createDividendArray()

#my_bse.plotVsDate('dividend')

print my_nifty.DynamicAllocationVer2(my_bse, 1)
#print my_bse.DynamicAllocationVer2(my_nifty, 1)
#for i in range(15,20):
#    my_nifty.investUnderPe(i);

#print percentile(my_bank.pe, 13)
#print percentile(my_bank.pe, 17)
#my_bse.plotVsDate('index');
#plotDynamicAllocation(my_nifty, my_bse)
#print my_finance.DynamicAllocation(13, 22, 1, 'pe')

#plotDiffBetweenFinanceNiftyPe(my_nifty, my_bank, my_finance)
#my_nifty.plotIndexWithPeHighlight(20, 15, 17, "NiftyWithPEHighlight.png")
