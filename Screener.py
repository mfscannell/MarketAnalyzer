from py_finance import YahooFinanceClient
from py_finance import TechnicalAnalysis
import Statistics
import csv
from statistics import mean

obvBestFitNumPeriods = 5

adBestFitNumPeriods = 5

bestFitNumPeriods = [3, 4, 5]

slowStochasticNumPeriods = 39
slowStochasticBestFitNumPeriods = 5
    
# Start of program
print("S & P 500: ^GSPC")
print("NYSE: ^NYA")
print("Nasdaq: ^IXIC")
print("Russell 2000: ^RUT")
print("VIX: ^VIX")
stockSymbol = input("Enter stock symbol:")
startDate = input("Start date (yyyy-mm-dd):")
endDate = input("End date (yyyy-mm-dd):")

stockClient = YahooFinanceClient.YahooFinanceClient(stockSymbol)
tradingDays = stockClient.getHistory(startDate, endDate)

vixTradingDays = []

vixStockClient = YahooFinanceClient.YahooFinanceClient("^VIX")

if stockSymbol != "^VIX":
    vixTradingDays = vixStockClient.getHistory(startDate, endDate)

for i, tradingDay in enumerate(tradingDays):
    tradingDays[i]['OBV'] = TechnicalAnalysis.calcOBV(tradingDays, i)
        
    # calc OBV best fit slopes
    for numPeriods in bestFitNumPeriods:
        if i >= numPeriods:
            tradingDays[i]['OBV' + str(numPeriods) + 'DaySlope'] = Statistics.findBestFitSlope(tradingDays, i - (numPeriods - 1), i, 'Period', 'OBV')
        else:
            tradingDays[i]['OBV' + str(numPeriods) + 'DaySlope'] = 0

    tradingDays[i]['AD'] = TechnicalAnalysis.calcAccumDist(tradingDays, i)

    # calc A/D best fit
    for numPeriods in bestFitNumPeriods:
        if i >= numPeriods:
            tradingDays[i]['AD' + str(numPeriods) + 'DaySlope'] = Statistics.findBestFitSlope(tradingDays, i - (numPeriods - 1), i, 'Period', 'AD')
        else:
            tradingDays[i]['AD' + str(numPeriods) + 'DaySlope'] = 0

    # calc slow stochastic
    if i >= slowStochasticNumPeriods:
        tradingDays[i]['SlowStochastic'] = TechnicalAnalysis.calcSlowStochastic(tradingDays, i - (slowStochasticNumPeriods - 1), i)
    else:
        tradingDays[i]['SlowStochastic'] = 0
        
    # calc slow stochastic 1 day slope
    if i >= 1:
        tradingDays[i]['SlowSto1DaySlope'] = tradingDays[i]['SlowStochastic'] - tradingDays[i - 1]['SlowStochastic']
    else:
        tradingDays[i]['SlowSto1DaySlope'] = 0
        
    # calc slow stochastic best fit
    if i >= slowStochasticBestFitNumPeriods:
        tradingDays[i]['SlowStoSlope'] = Statistics.findBestFitSlope(
        tradingDays, i - (slowStochasticBestFitNumPeriods - 1), i, 'Period', 'SlowStochastic')
    else:
        tradingDays[i]['SlowStoSlope'] = 0

    #VIX stuff
    if stockSymbol != "^VIX":
        tradingDays[i]["VIXOpen"] = vixTradingDays[i]["Open"]
        tradingDays[i]["VIXHigh"] = vixTradingDays[i]["High"]
        tradingDays[i]["VIXLow"] = vixTradingDays[i]["Low"]
        tradingDays[i]["VIXClose"] = vixTradingDays[i]["Close"]
        
        # calc VIX slope
        if i >= 1:
            tradingDays[i]['VIX1DaySlope'] = tradingDays[i]['VIXClose'] - tradingDays[i - 1]['VIXClose']
            tradingDays[i]['VIX1DayPercentSlope'] = 100 * tradingDays[i]['VIX1DaySlope'] / tradingDays[i - 1]['VIXClose']
        else:
            tradingDays[i]['VIX1DaySlope'] = 0
            tradingDays[i]['VIX1DayPercentSlope'] = 0
        
        # calc slow stochastic
        if i >= slowStochasticNumPeriods:
            tradingDays[i]['VIXSlowStochastic'] = TechnicalAnalysis.calcSlowStochastic(vixTradingDays, i - (slowStochasticNumPeriods - 1), i)
        else:
            tradingDays[i]['VIXSlowStochastic'] = 0
            
        # calc slow stochastic 1 day slope
        if i >= 1:
            tradingDays[i]['VIXSlowSto1DaySlope'] = tradingDays[i]['VIXSlowStochastic'] - tradingDays[i - 1]['VIXSlowStochastic']
        else:
            tradingDays[i]['VIXSlowSto1DaySlope'] = 0


numTrades = 0
totalReturn = 1
lastAction = 'SELL'
firstBuyEncountered = False
firstBuyDate = ''
lastSellDate = ''
lastBuyPrice = 1
lastSellPrice = 1
numTransactions = 0
numPositiveTransactions = 0

#determine buy and sell signals
for m, tradingDay in enumerate(tradingDays):
    actionToPerform = 'HOLD'
    
    '''
    ### DECISION TREE ###
    #1250 samples
    if '2007' in tradingDay['Date'] or '2008' in tradingDay['Date'] or '2009' in tradingDay['Date'] or '2010' in tradingDay['Date'] or '2011' in tradingDay['Date'] or '2012' in tradingDay['Date'] or '2013' in tradingDay['Date'] or '2014' in tradingDay['Date'] or '2015' in tradingDay['Date'] or '2016' in tradingDay['Date'] or '2017' in tradingDay['Date'] or '2018' in tradingDay['Date']:
    #if True:
        #1250 samples
        if tradingDay['SlowSto1DaySlope'] <= 1.543:
            #727 samples
            if tradingDay['SlowStochastic'] <= 82.074:
                #402 samples
                if tradingDay['VIX1DaySlope'] <= 0.905:
                    #209 samples
                    if tradingDay['AD3DaySlope'] <= -213516656:
                        #112 samples
                        if tradingDay['OBV3DaySlope'] <= -3445032448:
                            actionToPerform = 'SELL'
                        else:
                            #69 samples
                            if tradingDay['SlowStochastic'] <= 38.238:
                                actionToPerform = 'BUY'
                            else:
                                actionToPerform = 'SELL'
                    else:
                        if tradingDay['VIX1DayPercentSlope'] <= -0.271:
                            actionToPerform = 'BUY'
                        else:
                            if tradingDay['SlowStoSlope'] <= 7.548:
                                actionToPerform = 'HOLD'
                            else:
                                actionToPerform = 'SELL'
                else:
                    #193 samples
                    actionToPerform = 'SELL'
            else:
                #325 samples
                if tradingDay['SlowStochastic'] <= 92.823:
                    #175 samples
                    if tradingDay['AD5DaySlope'] <= -244146440:
                        #27 samples
                        actionToPerform = 'HOLD'
                    else:
                        #148 samples
                        if tradingDay['AD4DaySlope'] <= 728944448:
                            #78 samples
                            if tradingDay['VIXClose'] <= 10.73:
                                actionToPerform = 'HOLD'
                            else:
                                #72 samples
                                if tradingDay['AD3DaySlope'] <= -883062816:
                                    actionToPerform = 'HOLD'
                                else:
                                    #54 samples
                                    if tradingDay['OBV4DaySlope'] <= -683154976:
                                        actionToPerform = 'SELL'
                                    else:
                                        actionToPerform = 'SELL'
                        else:
                            #70 samples
                            if tradingDay['SlowStochastic'] <= 83.525:
                                actionToPerform = 'SELL'
                            else:
                                #66 samples
                                if tradingDay['SlowSto1DaySlope'] <= -1.767:
                                    #56 samples
                                    if tradingDay['OBV5DaySlope'] <= -1485398976:
                                        actionToPerform = 'SELL'
                                    else:
                                        actionToPerform = 'HOLD'
                                else:
                                    actionToPerform = 'HOLD'
                else:
                    #150 samples DONE
                    if tradingDay['OBV3DaySlope'] <= 278290000:
                        #71 samples
                        if tradingDay['VIXClose'] <= 10.92:
                            actionToPerform = 'BUY'
                        else:
                            actionToPerform = 'HOLD'
                    else:
                        #79 samples
                        if tradingDay['SlowStoSlope'] <= 2.108:
                            actionToPerform = 'HOLD'
                        else:
                            actionToPerform = 'BUY'
        else:
            #507 samples
            if tradingDay['SlowStochastic'] <= 83.911:
                #299 samples
                if tradingDay['AD3DaySlope'] <= -1375264832:
                    #24 samples
                    actionToPerform = 'HOLD'
                else:
                    #275 samples
                    actionToPerform = 'BUY'
            else:
                #208 samples
                if tradingDay['SlowStoSlope'] <= 3.314:
                    #149 samples
                    if tradingDay['SlowSto1DaySlope'] <= 8.093:
                        #88 samples
                        if tradingDay['SlowStochastic'] <= 99.488:
                            #75 samples
                            if tradingDay['OBV4DaySlope'] <= -1350478528:
                                actionToPerform = 'SELL'
                            else:
                                actionToPerform = 'HOLD'
                        else:
                            actionToPerform = 'BUY'
                    else:
                        #61 samples
                        if tradingDay['VIX1DayPercentSlope'] <= -7.211:
                            actionToPerform = 'BUY'
                        else:
                            #33 samples
                            if tradingDay['SlowSto1DaySlope'] <= 13.663:
                                actionToPerform = 'BUY'
                            else:
                                actionToPerform = 'HOLD'
                else:
                    #59 samples
                    actionToPerform = 'BUY'
    '''
    
    
    ### ORIGINAL ###
    if (m > 0 and 
        tradingDays[m]['SlowSto1DaySlope'] > 0 and 
        tradingDays[m]['VIX1DaySlope'] < 0 and
        tradingDays[m]['AD3DaySlope'] > 0
       ):
        actionToPerform = 'BUY'
        
    if (m > 0 and 
        tradingDays[m]['SlowSto1DaySlope'] < 0 and 
        tradingDays[m]['VIX1DaySlope'] > 0 and
        #tradingDays[m]['AD4DaySlope'] < 0
        (tradingDays[m]['AD4DaySlope'] < 0 or tradingDays[m]['OBV4DaySlope'] < 0)
       ):
        actionToPerform = 'SELL'
    

    '''
    ### HOPEFULLY BETTER ###
    if m > slowStochasticNumPeriods:
        if tradingDay['AD3DaySlope'] > 0 and tradingDay['OBV3DaySlope'] > 0:
            actionToPerform = 'BUY'
        elif tradingDay['AD3DaySlope'] < 0 and tradingDay['OBV3DaySlope'] < 0:
            actionToPerform = 'SELL'
        elif tradingDay['AD3DaySlope'] > 0 and tradingDay['OBV3DaySlope'] < 0:
            if tradingDay['SlowSto1DaySlope'] > 0 or tradingDay['VIX1DaySlope'] > 0:
                actionToPerform = 'BUY'
            elif tradingDay['SlowSto1DaySlope'] < 0 and tradingDay['VIX1DaySlope'] < 0:
                actionToPerform = 'SELL'
        elif tradingDay['AD3DaySlope'] < 0 and tradingDay['OBV3DaySlope'] > 0:
            if tradingDay['SlowSto1DaySlope'] > 0 and tradingDay['VIX1DaySlope'] > 0:
                actionToPerform = 'BUY'
            elif tradingDay['SlowSto1DaySlope'] < 0 and tradingDay['VIX1DaySlope'] < 0:
                actionToPerform = 'SELL'
    '''
    
    if lastAction == 'SELL' and actionToPerform == 'BUY':
        if not firstBuyEncountered:
            firstBuyEncountered = True
            firstBuyDate = tradingDay['Date']
            
        #lastBuyPrice = tradingDay['Close']
        lastBuyPrice = (tradingDay['High'] + tradingDay['Low']) / 2
        lastAction = 'BUY'
        numTransactions = numTransactions + 1
    elif lastAction == 'BUY' and actionToPerform == 'SELL':
        #lastSellPrice = tradingDay['Close']
        lastSellPrice = (tradingDay['High'] + tradingDay['Low']) / 2
        totalReturn = totalReturn * lastSellPrice / lastBuyPrice
        lastAction = 'SELL'
        numTransactions = numTransactions + 1
        lastSellDate = tradingDay['Date']
        
        if lastSellPrice > lastBuyPrice:
            numPositiveTransactions = numPositiveTransactions + 1
        
    tradingDays[m]['Buy/Sell'] = actionToPerform
    
    if m % 10 == 0:
        print("      Date      Last       Vol    VIX  Stoch  Stoch5DaySlope        OBV  OBV3DaySlope  OBV4DaySlope         AD  AD3DaySlope  AD4DaySlope  Buy/Sell")

    print(f"{tradingDay['Date']}  {'%8.2f' % tradingDay['Close']}  {'%.2e' % tradingDay['Volume']}  {'%5.2f' % tradingDay['VIXClose']}  {'%5.1f' % tradingDay['SlowStochastic']}  {'%14.1f' % tradingDay['SlowStoSlope']}  {'%9.2e' % tradingDay['OBV']}  {'%12.2e' % tradingDay['OBV3DaySlope']}  {'%12.2e' % tradingDay['OBV4DaySlope']}  {'%9.2e' % tradingDay['AD']}  {'%11.2e' % tradingDay['AD3DaySlope']}  {'%11.2e' % tradingDay['AD4DaySlope']}  {tradingDay['Buy/Sell'].rjust(8)}")

'''
print('First Buy Date:' + firstBuyDate)
print('Last Sell Date:' + lastSellDate)
print('Total Return:' + str(totalReturn))
print('Annual Return:' + str(totalReturn ** (1 / 12)))
print('Num transactions:' + str(numTransactions))
print('Num sells:' + str(numTransactions / 2))
print('Num positive sells:' + str(numPositiveTransactions))
print('Percent positive sells:' + str(100 * numPositiveTransactions / (numTransactions / 2)))
'''



'''
keys = tradingDays[0].keys()
with open('C:/temp/flashBackup/_stocks/WithVix.csv', 'w', newline = '') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(tradingDays)
'''

