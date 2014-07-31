
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.figure as fig


def plotDiffBetweenFinanceNiftyPe(my_nifty, my_bank, my_finance):
    plt.subplot(2,1,1)
    plt.plot(my_nifty.date, my_nifty.pe, 'blue', label="nifty")
    plt.plot(my_bank.date, my_bank.pe, 'green', label="bank")
    plt.plot(my_finance.date, my_finance.pe, 'orange', label="finance")
    plt.plot(my_nifty.date, [15]*len(my_nifty.date), 'red')
    plt.plot(my_nifty.date, [20]*len(my_nifty.date), 'red')
    plt.legend(loc='upper left')
    diffBetweenFinNiftyPe=[]
    datearr=[]
    for m in range(len(my_finance.date)):
        pelist=[my_nifty.pe[i] for i,j in enumerate(my_nifty.date) if j==my_finance.date[m]]
        if len(pelist):
            diffBetweenFinNiftyPe.append(my_finance.pe[m]-pelist[0])
            datearr.append(my_finance.date[m])
    plt.subplot(2,1,2)
    plt.plot(datearr, diffBetweenFinNiftyPe, label="financePE-niftyPE")
    plt.plot(datearr, [0]*len(datearr), 'red')
    plt.legend(loc='upper left')
    plt.savefig("diffBetweenFinNiftyPe.png", format="png")

def plotDynamicAllocation(my_nifty, my_bse):
    plt.figure(figsize=(16,12), dpi=80, facecolor=(1,1,1,1))
    fig1=plt.subplot(421)
    plt.plot(my_nifty.date, my_nifty.nifty)
    plt.ylabel('Nifty')

#fig1.set_yscale('log')

    fig2=plt.subplot(422)
    plt.plot(my_bse.date, my_bse.nifty)
    plt.ylabel('Sensex')
    #fig2.set_yscale('log')

    plt.subplot(423)
    plt.plot(my_nifty.date, my_nifty.pe)
    plt.plot(my_nifty.date, [15]*len(my_nifty.date), 'red')
    plt.plot(my_nifty.date, [20]*len(my_nifty.date), 'red')
    plt.plot(my_nifty.date, [17]*len(my_nifty.date), 'green')
    plt.ylabel('PE')

    plt.subplot(424)
    plt.plot(my_bse.date, my_bse.pe)
    plt.plot(my_bse.date, [13]*len(my_bse.date), 'red')
    plt.plot(my_bse.date, [22]*len(my_bse.date), 'red')
    plt.plot(my_bse.date, [17]*len(my_bse.date), 'green')
    plt.ylabel('PE')

    plt.subplot(425)
    plt.plot(my_nifty.date, my_nifty.dy)
    plt.plot(my_nifty.date, [1.1]*len(my_nifty.date), 'red')
    plt.plot(my_nifty.date, [1.6]*len(my_nifty.date), 'red')
    plt.ylabel('DY')

    plt.subplot(426)
    plt.plot(my_bse.date, my_bse.dy)
    plt.plot(my_bse.date, [1.1]*len(my_bse.date), 'red')
    plt.plot(my_bse.date, [1.6]*len(my_bse.date), 'red')
    plt.ylabel('DY')

    plt.subplot(427)
    plt.plot(my_nifty.pe, map(lambda x:1/x, my_nifty.dy), 'ro')
    plt.ylabel('1/DY');
    plt.xlabel('PE');

    plt.subplot(428)
    plt.plot(my_bse.pe, map(lambda x:1/x, my_bse.dy), 'ro')
    plt.ylabel('1/DY');
    plt.xlabel('PE');
#    plt.show()
    plt.savefig("NiftyandSensex.png", format="png")